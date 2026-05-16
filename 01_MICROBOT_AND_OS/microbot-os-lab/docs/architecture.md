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
