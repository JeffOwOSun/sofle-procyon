#!/bin/bash
# Flash both halves of the Sofle Procyon keyboard.
# Enter bootloader on each half via Q+Z+P+/ combo (hold 1 second).

UF2=~/code/qmk_firmware/lucky_studio_sofle_4x6_default.uf2

if [ ! -f "$UF2" ]; then
    echo "Firmware not found: $UF2"
    echo "Run ./compile.sh first."
    exit 1
fi

flash_half() {
    local label=$1
    echo "Waiting for $label half... (enter bootloader now)"
    while true; do
        if ls /Volumes/RPI-RP2/ >/dev/null 2>&1; then
            cp "$UF2" /Volumes/RPI-RP2/
            echo "$label half flashed!"
            sleep 2
            return
        fi
        sleep 0.5
    done
}

flash_half "First"
flash_half "Second"
echo "Both halves flashed."
