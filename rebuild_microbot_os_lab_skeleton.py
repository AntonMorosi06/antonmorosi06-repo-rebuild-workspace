from pathlib import Path
from datetime import datetime
import subprocess
import textwrap

ROOT = Path.home() / "Desktop" / "ANTONMOROSI06_REPO_REBUILD_WORKSPACE"
TARGET = ROOT / "01_MICROBOT_AND_OS" / "microbot-os-lab"
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print("[OK] wrote", path.relative_to(ROOT))

def touch(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

def run(cmd, cwd=None):
    print("[CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)

for folder in [
    "src",
    "docs",
    "build",
    "demos/screenshots",
    "demos/logs",
    "tests",
    "issues",
    "labels",
    "archive/original_repository_snapshot",
    "archive/original_detected_sources",
    "archive/generated_baseline_before_import"
]:
    path = TARGET / folder
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")

write(
    TARGET / "README.md",
    """
# MicroBot OS Lab

MicroBot OS Lab is a reconstructed low-level operating-system laboratory connected to the wider MicroBot ecosystem.

This folder is not an automatic clone of the old AntonMorosi2234 repository. The terminal could not access the original source repository, so this version is intentionally built as a clean skeleton based on the known project direction: bootloader, kernel, QEMU, text-mode interface, diagnostics, shell planning and MicroBot-oriented state.

The goal is to create a reliable baseline that can later receive the original code manually if it becomes available.

## Current status

Status: reconstructed skeleton.

This folder contains:

- a minimal bootloader skeleton in `src/boot.asm`;
- a minimal kernel skeleton in `src/kernel.asm`;
- a NASM/QEMU `Makefile`;
- documentation for architecture, boot process, build, validation and limitations;
- issue backlog;
- labels;
- source import status.

## What this project is

MicroBot OS Lab is an educational low-level systems project. It explores how a minimal bootable environment can become a specialized diagnostic and control interface for MicroBot concepts.

It is useful for:

- bootloader study;
- kernel basics;
- BIOS interrupt usage;
- text-mode screen systems;
- keyboard input;
- MicroBot diagnostics concepts;
- future shell design.

## What this project is not

This project is not a production operating system.

It does not currently include:

- protected mode;
- multitasking;
- memory management;
- filesystem support;
- networking;
- ESP32 communication;
- real MicroBot hardware control;
- physical validation.

## Build

Install dependencies on macOS:

    brew install nasm qemu make

Build:

    make

Run:

    make run

Clean:

    make clean

## Relationship to microbot-labs

`microbot-labs` remains the clean public baseline for MicroBot documentation, validation, protocol planning, dashboard evidence and release history.

`microbot-os-lab` is a connected experimental branch focused on low-level OS thinking.
"""
)

write(
    TARGET / "Makefile",
    """
ASM=nasm
QEMU=qemu-system-x86_64

BUILD_DIR=build
SRC_DIR=src

BOOT_SRC=$(SRC_DIR)/boot.asm
KERNEL_SRC=$(SRC_DIR)/kernel.asm

BOOT_BIN=$(BUILD_DIR)/boot.bin
KERNEL_BIN=$(BUILD_DIR)/kernel.bin
KERNEL_PADDED=$(BUILD_DIR)/kernel_padded.bin
IMAGE=$(BUILD_DIR)/microbot_os.img

KERNEL_SECTORS=20

.PHONY: all run clean info

all: $(IMAGE)

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BOOT_BIN): $(BOOT_SRC) | $(BUILD_DIR)
	$(ASM) -f bin $(BOOT_SRC) -o $(BOOT_BIN)

$(KERNEL_BIN): $(KERNEL_SRC) | $(BUILD_DIR)
	$(ASM) -f bin $(KERNEL_SRC) -o $(KERNEL_BIN)

$(KERNEL_PADDED): $(KERNEL_BIN)
	python3 - <<'INNERPY'
from pathlib import Path
kernel = Path("$(KERNEL_BIN)").read_bytes()
sector_size = 512
target = $(KERNEL_SECTORS) * sector_size
if len(kernel) > target:
    raise SystemExit(f"Kernel too large: {len(kernel)} bytes > {target} bytes")
kernel += b"\\x00" * (target - len(kernel))
Path("$(KERNEL_PADDED)").write_bytes(kernel)
print(f"[OK] padded kernel to {target} bytes")
INNERPY

$(IMAGE): $(BOOT_BIN) $(KERNEL_PADDED)
	cat $(BOOT_BIN) $(KERNEL_PADDED) > $(IMAGE)
	@echo "[OK] Created $(IMAGE)"

run: $(IMAGE)
	$(QEMU) -fda $(IMAGE) -boot a -m 16M

info:
	@echo "Boot source:    $(BOOT_SRC)"
	@echo "Kernel source:  $(KERNEL_SRC)"
	@echo "Image:          $(IMAGE)"
	@echo "Kernel sectors: $(KERNEL_SECTORS)"

clean:
	rm -rf $(BUILD_DIR)/*
	touch $(BUILD_DIR)/.gitkeep
"""
)

write(
    TARGET / "src" / "boot.asm",
    """
; MicroBot OS Lab - boot.asm
; Reconstructed minimal 16-bit bootloader skeleton.

BITS 16
ORG 0x7C00

KERNEL_LOAD_SEGMENT equ 0x0000
KERNEL_LOAD_OFFSET  equ 0x1000
KERNEL_SECTORS      equ 20

start:
    cli

    xor ax, ax
    mov ds, ax
    mov es, ax
    mov ss, ax
    mov sp, 0x7C00

    sti

    mov [boot_drive], dl

    mov si, boot_message
    call print_string

    call load_kernel

    mov si, jump_message
    call print_string

    jmp KERNEL_LOAD_SEGMENT:KERNEL_LOAD_OFFSET

load_kernel:
    mov ah, 0x02
    mov al, KERNEL_SECTORS
    mov ch, 0x00
    mov cl, 0x02
    mov dh, 0x00
    mov dl, [boot_drive]
    mov bx, KERNEL_LOAD_OFFSET
    mov ax, KERNEL_LOAD_SEGMENT
    mov es, ax

    int 0x13
    jc disk_error

    ret

disk_error:
    mov si, disk_error_message
    call print_string
    cli

.hang:
    hlt
    jmp .hang

print_string:
    pusha

.next:
    lodsb
    cmp al, 0
    je .done

    mov ah, 0x0E
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    jmp .next

.done:
    popa
    ret

boot_drive db 0

boot_message db 13, 10, "MicroBot OS Lab bootloader", 13, 10, 0
jump_message db "Kernel loaded. Jumping to 0000:1000...", 13, 10, 0
disk_error_message db "Disk read error. Kernel not loaded.", 13, 10, 0

times 510 - ($ - $$) db 0
dw 0xAA55
"""
)

write(
    TARGET / "src" / "kernel.asm",
    """
; MicroBot OS Lab - kernel.asm
; Reconstructed minimal 16-bit real-mode kernel skeleton.

BITS 16
ORG 0x1000

start:
    cli
    xor ax, ax
    mov ds, ax
    mov es, ax
    sti

    call clear_screen
    call draw_home

main_loop:
    mov ah, 0x00
    int 0x16

    cmp al, '1'
    je show_home

    cmp al, '2'
    je show_microbot_panel

    cmp al, '3'
    je show_diagnostics

    cmp al, '4'
    je show_help

    cmp al, '5'
    je show_shell_placeholder

    jmp main_loop

show_home:
    call clear_screen
    call draw_home
    jmp main_loop

show_microbot_panel:
    call clear_screen
    mov si, microbot_screen
    call print_string
    jmp main_loop

show_diagnostics:
    call clear_screen
    mov si, diagnostics_screen
    call print_string
    jmp main_loop

show_help:
    call clear_screen
    mov si, help_screen
    call print_string
    jmp main_loop

show_shell_placeholder:
    call clear_screen
    mov si, shell_screen
    call print_string
    jmp main_loop

draw_home:
    mov si, home_screen
    call print_string
    ret

clear_screen:
    mov ah, 0x00
    mov al, 0x03
    int 0x10
    ret

print_string:
    pusha

.next:
    lodsb
    cmp al, 0
    je .done

    mov ah, 0x0E
    mov bh, 0x00
    mov bl, 0x07
    int 0x10
    jmp .next

.done:
    popa
    ret

home_screen:
    db "==============================================",13,10
    db "             MICROBOT OS LAB v0.1             ",13,10
    db "==============================================",13,10
    db 13,10
    db "Status: reconstructed kernel baseline.",13,10
    db "Mode:   16-bit BIOS real mode.",13,10
    db 13,10
    db "Screens:",13,10
    db "  1 - Home",13,10
    db "  2 - MicroBot Panel",13,10
    db "  3 - Diagnostics",13,10
    db "  4 - Help",13,10
    db "  5 - Shell placeholder",13,10
    db 0

microbot_screen:
    db "==============================================",13,10
    db "              MICROBOT PANEL                  ",13,10
    db "==============================================",13,10
    db 13,10
    db "Controller link:  MOCK / PREPARED",13,10
    db "Bot count:        06 simulated nodes",13,10
    db "Selected bot:     01",13,10
    db "Node state:       IDLE",13,10
    db 13,10
    db "This is not hardware validation.",13,10
    db "Press 1 for Home.",13,10
    db 0

diagnostics_screen:
    db "==============================================",13,10
    db "               DIAGNOSTICS                    ",13,10
    db "==============================================",13,10
    db 13,10
    db "Bootloader:       reconstructed baseline",13,10
    db "Kernel address:   0000:1000",13,10
    db "Video mode:       BIOS text mode 03h",13,10
    db "Keyboard input:   BIOS int 16h",13,10
    db "Disk loading:     BIOS int 13h",13,10
    db 13,10
    db "Press 1 for Home.",13,10
    db 0

help_screen:
    db "==============================================",13,10
    db "                  HELP                        ",13,10
    db "==============================================",13,10
    db 13,10
    db "1 Home",13,10
    db "2 MicroBot Panel",13,10
    db "3 Diagnostics",13,10
    db "4 Help",13,10
    db "5 Shell placeholder",13,10
    db 13,10
    db "Future versions may add command parsing.",13,10
    db 0

shell_screen:
    db "==============================================",13,10
    db "             SHELL PLACEHOLDER                ",13,10
    db "==============================================",13,10
    db 13,10
    db "Planned commands:",13,10
    db "  help",13,10
    db "  status",13,10
    db "  bots",13,10
    db "  link on",13,10
    db "  link off",13,10
    db 13,10
    db "Command parser not implemented yet.",13,10
    db "Press 1 for Home.",13,10
    db 0
"""
)

write(
    TARGET / "docs" / "source_import_status.md",
    f"""
# Source Import Status

Date:
{now}

Original source:
AntonMorosi2234/codiceMicrobotOs

Current decision:
Do not clone from AntonMorosi2234 automatically.

Reason:
The terminal cannot access AntonMorosi2234 repositories reliably and returns `Repository not found`.

Current strategy:
Use a reconstructed clean skeleton based on the already analyzed project direction.

Status:
Skeleton created manually.

Canonical files:

- src/boot.asm
- src/kernel.asm
- Makefile

If the original source becomes available later, copy it manually into:

archive/original_detected_sources

Then compare manually before merging.
"""
)

write(
    TARGET / "docs" / "build_and_run.md",
    """
# Build and Run

Install dependencies:

    brew install nasm qemu make

Build:

    make

Run:

    make run

Clean:

    make clean

Expected generated image:

    build/microbot_os.img

This skeleton is designed for QEMU and BIOS real mode.
"""
)

write(
    TARGET / "docs" / "architecture.md",
    """
# Architecture

MicroBot OS Lab is divided into two minimal executable layers.

Bootloader layer:

- assembled from `src/boot.asm`;
- loaded by BIOS at address 0x7C00;
- reads kernel sectors from disk;
- jumps to the kernel at 0000:1000.

Kernel layer:

- assembled from `src/kernel.asm`;
- runs in 16-bit real mode;
- uses BIOS text output;
- uses BIOS keyboard input;
- displays a MicroBot-oriented text interface.

This is an educational skeleton, not a production OS.
"""
)

write(
    TARGET / "docs" / "known_limitations.md",
    """
# Known Limitations

- Reconstructed skeleton, not cloned original source.
- No protected mode.
- No filesystem.
- No multitasking.
- No networking.
- No ESP32 communication.
- No physical MicroBot control.
- No hardware validation.
- QEMU validation still needs screenshot evidence.
"""
)

write(
    TARGET / "docs" / "qemu_validation_checklist.md",
    """
# QEMU Validation Checklist

- [ ] Run `make clean`.
- [ ] Run `make`.
- [ ] Confirm `build/microbot_os.img` exists.
- [ ] Run `make run`.
- [ ] Confirm QEMU boots.
- [ ] Confirm home screen appears.
- [ ] Press 1, 2, 3, 4, 5.
- [ ] Confirm screen switching.
- [ ] Save screenshot in `demos/screenshots`.
- [ ] Save terminal output in `demos/logs`.
"""
)

write(
    TARGET / "issues" / "ISSUES_BACKLOG.md",
    """
# Issues Backlog for microbot-os-lab

## Issue 01: Validate build

Goal:
Confirm the reconstructed skeleton builds.

Tasks:
- [ ] Run make clean.
- [ ] Run make.
- [ ] Confirm build/microbot_os.img exists.

Acceptance criteria:
- Build succeeds or error log is saved.

## Issue 02: Validate QEMU boot

Goal:
Confirm the generated image boots in QEMU.

Tasks:
- [ ] Run make run.
- [ ] Confirm MicroBot OS screen appears.
- [ ] Confirm keyboard navigation.

Acceptance criteria:
- Screenshot added to demos/screenshots.

## Issue 03: Improve kernel screen layout

Goal:
Make the text UI cleaner.

Tasks:
- [ ] Improve spacing.
- [ ] Add version line.
- [ ] Add state table.
- [ ] Keep text within screen width.

Acceptance criteria:
- QEMU screen is readable.

## Issue 04: Add shell parser plan

Goal:
Prepare next version.

Tasks:
- [ ] Define command buffer.
- [ ] Define supported commands.
- [ ] Define unknown command behavior.

Acceptance criteria:
- docs/shell_commands.md is updated.
"""
)

write(
    TARGET / "labels" / "labels.yml",
    """
- name: os
  color: "5319e7"
  description: "Operating-system layer work"
- name: bootloader
  color: "fbca04"
  description: "Bootloader and boot sector"
- name: kernel
  color: "6f42c1"
  description: "Kernel and text UI"
- name: qemu
  color: "1d76db"
  description: "QEMU validation"
- name: assembly
  color: "d4c5f9"
  description: "NASM assembly"
- name: reconstructed-skeleton
  color: "fef2c0"
  description: "Created manually because source clone is unavailable"
- name: documentation
  color: "0366d6"
  description: "README and docs"
- name: microbot-alignment
  color: "0052cc"
  description: "Relation to MicroBot ecosystem"
- name: portfolio-ready
  color: "0e8a16"
  description: "Needed before public presentation"
"""
)

write(
    TARGET / "CHANGELOG.md",
    f"""
# Changelog

## Reconstructed skeleton batch - {now}

- Created reconstructed MicroBot OS Lab skeleton.
- Added Makefile.
- Added src/boot.asm.
- Added src/kernel.asm.
- Added build and run documentation.
- Added architecture documentation.
- Added source import status.
- Added QEMU validation checklist.
- Added known limitations.
- Added issue backlog.
- Added labels YAML.
"""
)

population_log = ROOT / "05_POPULATION_LOG.md"
old_log = population_log.read_text(encoding="utf-8") if population_log.exists() else "# Population Log\n\n"

write(
    population_log,
    old_log + f"""

## {now}

Rebuilt microbot-os-lab as a reconstructed skeleton.

Decision:
Do not clone AntonMorosi2234 repositories automatically from now on.

Reason:
Terminal access returns repository not found.

Action:
Created source skeleton manually based on project analysis:

- Makefile
- src/boot.asm
- src/kernel.asm
- docs
- issues
- labels
"""
)

run(["git", "add", "-A"], cwd=ROOT)

commit = run(["git", "commit", "-m", "Rebuild MicroBot OS Lab as reconstructed skeleton"], cwd=ROOT)

if commit.returncode == 0:
    print("[OK] Commit created.")
else:
    print("[WARN] Commit not created. Maybe no changes.")
    print(commit.stdout)
    print(commit.stderr)

push = run(["git", "push", "origin", "main"], cwd=ROOT)

if push.returncode == 0:
    print("[OK] Pushed to origin main.")
else:
    print("[WARN] Push failed.")
    print(push.stdout)
    print(push.stderr)

print("[OK] MicroBot OS skeleton rebuild complete.")
