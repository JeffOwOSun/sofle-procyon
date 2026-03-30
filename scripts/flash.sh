#!/bin/bash
# Flash one half of the Sofle Procyon keyboard.
# Enter bootloader via Q+Z+P+/ combo (hold 1 second).

UF2=~/code/qmk_firmware/lucky_studio_sofle_4x6_default.uf2

if [ ! -f "$UF2" ]; then
    echo "Firmware not found: $UF2"
    echo "Run ./compile.sh first."
    exit 1
fi

echo "Waiting for bootloader... (enter bootloader now)"
while true; do
    if ls /Volumes/RPI-RP2/ >/dev/null 2>&1; then
        cp "$UF2" /Volumes/RPI-RP2/
        echo "Flashed!"
        exit 0
    fi
    sleep 0.5
done
