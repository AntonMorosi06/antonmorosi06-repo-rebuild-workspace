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
