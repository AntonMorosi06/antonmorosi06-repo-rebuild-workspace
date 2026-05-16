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
