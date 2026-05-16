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
