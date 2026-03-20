# Sofle Procyon

Split keyboard with integrated Procyon touchpad. Based on the Lucky Studio Sofle 4x6 PCB with a George Norton Procyon 57x80mm trackpad module.

## Structure

```
firmware/     QMK keyboard definition and keymap
case/         Case design (CadQuery/Build123d)
scans/        PCB and touchpad scans for dimensional reference
docs/         Documentation and notes
```

## Firmware

Built on [george-norton/qmk_firmware](https://github.com/george-norton/qmk_firmware/tree/multitouch_experiment) `multitouch_experiment` branch (provides maxtouch digitizer driver).

Full firmware source is in [JeffOwOSun/qmk_firmware](https://github.com/JeffOwOSun/qmk_firmware) on the `sofle-procyon` branch.

### Compile

```bash
export PATH="$HOME/.local/toolchains/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi/bin:$PATH"
cd ~/code/qmk_firmware
git checkout sofle-procyon
QMK_HOME=~/code/qmk_firmware qmk compile -kb lucky_studio/sofle_4x6 -km default
```

### Flash

Enter bootloader (Q+Z+P+/ held 1 second), then:
```bash
cp ~/code/qmk_firmware/lucky_studio_sofle_4x6_default.uf2 /Volumes/RPI-RP2/
```
Flash each half separately. Right half is USB master.

## Hardware

- MCU: RP2040
- Layout: 5 rows x 6 cols per side (60 keys)
- Encoder: left side only
- Touchpad: Procyon 57x80mm (Microchip mXT336UD)
- RGB: WS2812, 29 LEDs per side
