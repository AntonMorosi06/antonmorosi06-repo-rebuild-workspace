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
kernel += b"\x00" * (target - len(kernel))
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
