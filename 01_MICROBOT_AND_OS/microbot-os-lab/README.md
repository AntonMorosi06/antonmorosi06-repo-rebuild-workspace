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
