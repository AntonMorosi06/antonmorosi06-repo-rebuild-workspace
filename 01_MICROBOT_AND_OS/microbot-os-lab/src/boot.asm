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
