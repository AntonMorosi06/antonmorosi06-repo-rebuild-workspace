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
