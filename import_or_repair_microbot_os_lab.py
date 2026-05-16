from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import textwrap

ROOT = Path.home() / "Desktop" / "ANTONMOROSI06_REPO_REBUILD_WORKSPACE"
TARGET = ROOT / "01_MICROBOT_AND_OS" / "microbot-os-lab"
TMP = ROOT / "_TEMP_IMPORTS" / "codiceMicrobotOs"
SOURCE_URL = "https://github.com/AntonMorosi2234/codiceMicrobotOs.git"

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def run(cmd, cwd=None):
    print("[CMD]", " ".join(cmd))
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)

def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    print("[OK] wrote", path.relative_to(ROOT))

def copy_file(src: Path, dst: Path):
    if src.exists() and src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print("[OK] copied", src.name, "->", dst.relative_to(ROOT))
        return True
    print("[WARN] missing file:", src)
    return False

def copy_tree_clean(src: Path, dst: Path):
    if dst.exists():
        shutil.rmtree(dst)

    def ignore_func(directory, names):
        ignored = set()
        for name in names:
            if name in {".git", "__pycache__", ".DS_Store", ".venv", "venv", "node_modules", "build"}:
                ignored.add(name)
            if name.endswith((".bin", ".img", ".o", ".pyc")):
                ignored.add(name)
        return ignored

    shutil.copytree(src, dst, ignore=ignore_func)
    print("[OK] archived source snapshot ->", dst.relative_to(ROOT))

def find_first(base: Path, patterns):
    found = []
    for pattern in patterns:
        found.extend(base.rglob(pattern))
    found = [p for p in found if p.is_file() and ".git" not in p.parts]
    found = sorted(found, key=lambda p: (len(p.parts), str(p).lower()))
    return found[0] if found else None

def detect_sources(base: Path):
    files = []
    patterns = ["*.asm", "*.s", "*.inc", "*.h", "*.c", "*.cpp", "*.txt", "*.md", "Makefile"]
    for pattern in patterns:
        files.extend(base.rglob(pattern))
    files = [p for p in files if p.is_file() and ".git" not in p.parts]
    return sorted(set(files), key=lambda p: str(p).lower())

print("")
print("=== MICROBOT OS LAB SOURCE IMPORT / REPAIR ===")
print("Root:", ROOT)
print("Target:", TARGET)
print("Source:", SOURCE_URL)
print("")

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

if TMP.exists():
    print("[INFO] Removing old temporary clone:", TMP)
    shutil.rmtree(TMP)

TMP.parent.mkdir(parents=True, exist_ok=True)

clone = run(["git", "clone", SOURCE_URL, str(TMP)])
clone_ok = clone.returncode == 0

if not clone_ok:
    print("[WARN] Clone failed. Continuing with repaired documented baseline.")
    print(clone.stdout)
    print(clone.stderr)

    write(
        TARGET / "docs" / "source_import_status.md",
        f"""
# Source Import Status

Date:
{now}

Attempted source:
AntonMorosi2234/codiceMicrobotOs

Result:
Clone failed from terminal.

Git output:

{clone.stdout}

{clone.stderr}

Interpretation:
The local workspace is not broken. The source repository may be private, renamed, deleted, or inaccessible from the current Git credentials.

Action:
The existing cleaned MicroBot OS Lab baseline remains active. Original source can be imported later manually if needed.
"""
    )

else:
    print("[OK] Source repository cloned.")

    copy_tree_clean(TMP, TARGET / "archive" / "original_repository_snapshot")

    boot_source = find_first(TMP, ["*boot*.asm", "boot.asm"])
    kernel_source = find_first(TMP, ["*kernel*.asm", "kernel.asm"])
    makefile_source = find_first(TMP, ["Makefile"])
    readme_source = find_first(TMP, ["README.md", "readme.md"])

    if readme_source:
        copy_file(readme_source, TARGET / "archive" / "original_detected_sources" / "README.original.md")
    if makefile_source:
        copy_file(makefile_source, TARGET / "archive" / "original_detected_sources" / "Makefile.original")
    if boot_source:
        copy_file(boot_source, TARGET / "archive" / "original_detected_sources" / "boot.original.asm")
        copy_file(boot_source, TARGET / "src" / "boot.imported_from_original.asm")
    if kernel_source:
        copy_file(kernel_source, TARGET / "archive" / "original_detected_sources" / "kernel.original.asm")
        copy_file(kernel_source, TARGET / "src" / "kernel.imported_from_original.asm")

    detected_lines = []
    for p in detect_sources(TMP):
        rel = p.relative_to(TMP)
        detected_lines.append(f"- {rel} | {p.stat().st_size} bytes")

    write(
        TARGET / "archive" / "original_detected_sources" / "DETECTED_SOURCE_FILES.md",
        "# Detected Source Files\n\n"
        f"Source repository: AntonMorosi2234/codiceMicrobotOs\n\n"
        f"Imported at: {now}\n\n"
        + ("\n".join(detected_lines) if detected_lines else "No source files detected.")
    )

    write(
        TARGET / "docs" / "source_import_status.md",
        f"""
# Source Import Status

Date:
{now}

Attempted source:
AntonMorosi2234/codiceMicrobotOs

Result:
Clone succeeded.

Detected files:

- Boot source: {boot_source.relative_to(TMP) if boot_source else "not found"}
- Kernel source: {kernel_source.relative_to(TMP) if kernel_source else "not found"}
- Makefile: {makefile_source.relative_to(TMP) if makefile_source else "not found"}
- README: {readme_source.relative_to(TMP) if readme_source else "not found"}

Import policy:
The original repository has been archived under archive/original_repository_snapshot.

Detected source files have been preserved under archive/original_detected_sources.

If boot and kernel files were found, they were copied as comparison files under src.

The current cleaned baseline remains canonical until manual comparison and QEMU validation confirm that imported source should be merged.
"""
    )

write(
    TARGET / "docs" / "manual_merge_plan.md",
    """
# Manual Merge Plan

This repository may contain both a cleaned baseline and imported original source files.

Canonical baseline files:

- src/boot.asm
- src/kernel.asm
- Makefile

Imported comparison files, if available:

- src/boot.imported_from_original.asm
- src/kernel.imported_from_original.asm

The imported files must not automatically replace the canonical baseline. Merge only after comparison and build validation.

## Step 1: compare bootloader

Check:

- kernel load address;
- number of sectors loaded;
- boot drive preservation;
- disk error handling;
- boot signature;
- comments and clarity.

## Step 2: compare kernel

Check:

- screen system;
- keyboard input;
- MicroBot state;
- diagnostics;
- shell logic;
- size and compatibility with the bootloader.

## Step 3: merge one feature at a time

Suggested order:

1. better screen layout;
2. MicroBot state panel;
3. diagnostics;
4. event log;
5. shell placeholder;
6. shell parser.

## Step 4: validate after every merge

Run:

make clean
make
make run

Then update docs and screenshots.
"""
)

write(
    TARGET / "docs" / "release_notes_v0_1_0.md",
    """
# MicroBot OS Lab v0.1.0 Release Notes Draft

Status:
Draft.

Purpose:
Create a clean, reproducible baseline for MicroBot OS Lab.

Included:

- bootloader baseline;
- kernel baseline;
- NASM/QEMU Makefile;
- source import or source import status report;
- architecture documentation;
- boot process documentation;
- kernel design notes;
- shell command plan;
- QEMU validation checklist;
- issue backlog;
- labels.

Not included:

- protected mode;
- filesystem;
- multitasking;
- real ESP32 communication;
- physical MicroBot hardware control;
- production safety guarantees.

Release condition:
This draft becomes final only after QEMU boot is validated and screenshot evidence is added.
"""
)

write(
    TARGET / "issues" / "ISSUES_BACKLOG.md",
    """
# Issues Backlog for microbot-os-lab

## Issue 01: Verify canonical bootloader

Goal:
Confirm that src/boot.asm is the correct canonical bootloader.

Tasks:
- [ ] Check boot signature.
- [ ] Check load address.
- [ ] Check kernel sector count.
- [ ] Check disk error handling.
- [ ] Compare imported original if available.

Acceptance criteria:
- Bootloader is documented and buildable.

## Issue 02: Verify canonical kernel

Goal:
Confirm that src/kernel.asm is the correct canonical kernel baseline.

Tasks:
- [ ] Check text output.
- [ ] Check keyboard navigation.
- [ ] Check MicroBot panel.
- [ ] Check diagnostics screen.
- [ ] Compare imported original if available.

Acceptance criteria:
- Kernel builds and boots in QEMU.

## Issue 03: Validate build

Goal:
Run make clean and make.

Tasks:
- [ ] Run make clean.
- [ ] Run make.
- [ ] Save output in demos/logs.
- [ ] Fix build errors if present.

Acceptance criteria:
- build/microbot_os.img is created.

## Issue 04: Validate QEMU boot

Goal:
Run the generated image in QEMU.

Tasks:
- [ ] Run make run.
- [ ] Confirm boot screen.
- [ ] Confirm keyboard screen switching.
- [ ] Add screenshot evidence.

Acceptance criteria:
- Screenshot exists under demos/screenshots.

## Issue 05: Finalize v0.1.0 release notes

Goal:
Convert docs/release_notes_v0_1_0.md from draft to final.

Tasks:
- [ ] Confirm build status.
- [ ] Confirm boot status.
- [ ] Add screenshot.
- [ ] Update README.
- [ ] Update CHANGELOG.

Acceptance criteria:
- Release notes match actual validated behavior.
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
  description: "Boot sector and disk-loading logic"
- name: kernel
  color: "6f42c1"
  description: "Kernel code and screen/input behavior"
- name: assembly
  color: "d4c5f9"
  description: "NASM/x86 assembly"
- name: qemu
  color: "1d76db"
  description: "QEMU build/run validation"
- name: source-import
  color: "38bdf8"
  description: "Imported original repository material"
- name: manual-merge
  color: "fef2c0"
  description: "Requires manual comparison before merging"
- name: documentation
  color: "0366d6"
  description: "README and docs"
- name: testing
  color: "fbca04"
  description: "Manual or automated validation"
- name: demo
  color: "0e8a16"
  description: "Screenshots and run evidence"
- name: cleanup
  color: "c5def5"
  description: "Naming, structure and formatting cleanup"
- name: microbot-alignment
  color: "0052cc"
  description: "Relation to MicroBot ecosystem and microbot-labs"
- name: portfolio-ready
  color: "0e8a16"
  description: "Required before public presentation"
"""
)

readme_path = TARGET / "README.md"
existing_readme = readme_path.read_text(encoding="utf-8", errors="replace") if readme_path.exists() else "# MicroBot OS Lab\n"

if "## Source import status" not in existing_readme:
    existing_readme += """

## Source import status

The source import process has been attempted for the original AntonMorosi2234/codiceMicrobotOs repository.

If the clone succeeded, the original repository snapshot is archived under:

archive/original_repository_snapshot

Detected original source files are archived under:

archive/original_detected_sources

If the clone failed, the reason is documented in:

docs/source_import_status.md

The cleaned baseline remains:

src/boot.asm
src/kernel.asm
Makefile

Imported original files, if present, are comparison material only until manually merged and validated.
"""
    write(readme_path, existing_readme)

build_log_path = TARGET / "demos" / "logs" / "build_attempt_after_os_import.txt"

has_make = shutil.which("make") is not None
has_nasm = shutil.which("nasm") is not None

if has_make and has_nasm and (TARGET / "Makefile").exists():
    print("[INFO] make and nasm detected. Attempting build.")
    clean = run(["make", "clean"], cwd=TARGET)
    build = run(["make"], cwd=TARGET)
    write(
        build_log_path,
        f"""
# Build Attempt After OS Import

Date:
{now}

Command:
make clean

Return code:
{clean.returncode}

STDOUT:
{clean.stdout}

STDERR:
{clean.stderr}

Command:
make

Return code:
{build.returncode}

STDOUT:
{build.stdout}

STDERR:
{build.stderr}
"""
    )
else:
    write(
        build_log_path,
        f"""
# Build Attempt After OS Import

Date:
{now}

Build was not executed.

Reason:

- make available: {has_make}
- nasm available: {has_nasm}
- Makefile exists: {(TARGET / "Makefile").exists()}

Install dependencies and run manually:

brew install nasm qemu make

Then:

cd 01_MICROBOT_AND_OS/microbot-os-lab
make clean
make
make run
"""
    )

changelog_path = TARGET / "CHANGELOG.md"
old_changelog = changelog_path.read_text(encoding="utf-8", errors="replace") if changelog_path.exists() else "# Changelog\n\n"

write(
    changelog_path,
    old_changelog + f"""

## OS import or repair batch - {now}

- Attempted import from AntonMorosi2234/codiceMicrobotOs.
- Preserved or documented original source import status.
- Added manual merge plan.
- Added v0.1.0 release notes draft.
- Updated issue backlog.
- Updated labels.
- Added build attempt log.
"""
)

population_log = ROOT / "05_POPULATION_LOG.md"
old_log = population_log.read_text(encoding="utf-8") if population_log.exists() else "# Population Log\n\n"

write(
    population_log,
    old_log + f"""

## {now}

Processed third AntonMorosi2234 repository:

- Source attempted: AntonMorosi2234/codiceMicrobotOs
- Target: 01_MICROBOT_AND_OS/microbot-os-lab

The script attempted to clone the original repository. If clone succeeded, it archived the original and preserved detected boot/kernel sources. If clone failed, it documented the failure and preserved the cleaned baseline.

A build attempt log was generated when make and nasm were available.
"""
)

print("")
print("=== GIT COMMIT AND PUSH ===")

run(["git", "add", "."], cwd=ROOT)

commit = run(["git", "commit", "-m", "Process MicroBot OS source import"], cwd=ROOT)

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

print("")
print("[OK] MicroBot OS import/repair batch complete.")
print("Target folder:", TARGET)
