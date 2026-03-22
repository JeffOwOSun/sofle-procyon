# Sofle Procyon

A complete firmware and case design for the **Sofle Procyon** split keyboard -- a 5x6 column-staggered layout built on the Lucky Studio (LXF-YZP) PCB with a George Norton Procyon 57x80mm touchpad integrated into the right half.

## Features

- **RP2040** processor on each half
- **Procyon 57x80mm touchpad** (Microchip mXT336UD maxtouch) on the right half, with firmware-level gesture emulation for macOS
- **Rotary encoder** on the left half
- **WS2812 RGB LEDs** -- 29 per side
- **Hot-swap MX switches** -- 29 keys per side (58 total, 5 rows x 6 columns + 2 thumb keys)
- **USB-C** for host connection and split interconnect (no TRRS)
- **Programmatically generated case** -- Python (SolidPython2) to OpenSCAD to STL, with print-in-place touchpad tower

## Repository Structure

```
sofle-procyon/
├── README.md               This file
├── firmware/
│   └── README.md           Pointer to QMK firmware repo
├── case/
│   ├── README.md           Case design documentation
│   ├── generate_case.py    Parametric case generator (SolidPython2)
│   ├── pcb_data.json       PCB feature positions and dimensions
│   ├── annotator.html      Interactive web-based PCB annotator
│   ├── server.py           Local server for the annotator
│   ├── reference/          Tempest case STEP files (for reference)
│   └── releases/           Generated SCAD, STL, and 3MF files
├── scans/
│   ├── pcb-scans.jpg       Original 300 DPI flatbed scan
│   ├── left_half_top.png   Normalized left PCB (top-down view)
│   ├── right_half_top.png  Normalized right PCB (top-down view)
│   └── touchpad_top.png    Normalized touchpad module
└── docs/                   Additional notes and documentation
```

---

## Hardware

| Component | Specification |
|-----------|---------------|
| MCU | RP2040 (each half) |
| Layout | 5 rows x 6 columns + 2 thumb keys per side |
| Switches | MX hot-swap |
| Encoder | Left half only (EC11 compatible) |
| Touchpad | Procyon 57x80mm (Microchip mXT336UD) |
| LEDs | WS2812, 29 per side |
| Host connection | USB-C (right half is master) |
| Split interconnect | USB-C (no TRRS) |
| PCB designer | Lucky Studio (LXF-YZP / yuezp) |

### PCB Dimensions

| Measurement | Value |
|-------------|-------|
| Left PCB width | 140mm |
| Right PCB width | 160.5mm |
| Extra width (right, split side) | 20.5mm (touchpad area) |
| Touchpad module | 57.2 x 80mm |
| Switch spacing | 19mm column, 19mm row |
| Mounting holes | 5 per half, M2 (2.25mm) |

### Column Stagger (from middle column)

| Column | Stagger |
|--------|---------|
| Pinky (outer) | 11.4mm |
| Ring | 2.5mm |
| Middle | 0mm (reference) |
| Index | 2.5mm |
| Inner | 5.0mm |

---

## Firmware

The firmware lives in a separate QMK fork:

- **Repo:** [JeffOwOSun/qmk_firmware](https://github.com/JeffOwOSun/qmk_firmware)
- **Branch:** `sofle-procyon`
- **QMK path:** `keyboards/lucky_studio/sofle_4x6/`

This fork is based on [george-norton/qmk_firmware](https://github.com/george-norton/qmk_firmware/tree/multitouch_experiment) (`multitouch_experiment` branch), which provides the maxtouch digitizer driver needed for the Procyon touchpad.

### Keymap Overview

The default keymap has **four layers:**

| Layer | Name | Purpose |
|-------|------|---------|
| 0 | QWERTY | Base typing layer |
| 1 | Colemak | Alternative base (toggled) |
| 2 | F-keys | Function keys (hold Del) |
| 3 | Nav+Numbers | Navigation, numbers, settings (hold Space) |

### Key Behaviors

| Key | Tap | Hold |
|-----|-----|------|
| Left Shift | `(` | Left Shift (Space Cadet: `SC_LSPO`) |
| Right Shift | `)` | Right Shift (Space Cadet: `SC_RSPC`) |
| Left Ctrl position | Esc | Left Ctrl (`MT(MOD_LCTL, KC_ESC)`) |
| Space | Space | Layer 3 (`LT(3, KC_SPC)`) |
| Delete | Delete | Layer 2 (`LT(2, KC_DEL)`) |
| Caps Word | `CW_TOGG` | -- |

### Encoder Functions

| Layer | Rotate | Press |
|-------|--------|-------|
| 0 (QWERTY) | Workspace switching (Ctrl+Left / Ctrl+Right) | Mission Control (Ctrl+Up) |
| 1 (Colemak) | Same as layer 0 | Same as layer 0 |
| 3 (Nav) | Cycle cursor speed (5 levels) | -- |

### Touchpad

The Procyon touchpad provides multitouch input, but macOS does not honor standard HID multitouch descriptors from third-party devices (Apple uses a fully proprietary protocol for trackpad gesture recognition). The firmware works around this by emulating mouse events from raw touch data:

| Gesture | Action |
|---------|--------|
| 1-finger move | Cursor movement (adjustable speed, 5 levels) |
| 2-finger move | Scroll (natural scrolling, adjustable speed) |
| 3-finger swipe up | Mission Control |
| 3-finger swipe down | App Expose |
| 3-finger swipe left/right | Workspace switching |
| 1-finger tap | Left click |
| 2-finger tap | Right click |
| 3-finger tap | Middle click |

Cursor speed is adjustable across 5 levels using the encoder on layer 3.

### Compiling

You need the ARM GCC toolchain for RP2040. On macOS with Apple Silicon:

```bash
# Set up toolchain path
export PATH="$HOME/.local/toolchains/arm-gnu-toolchain-13.3.rel1-darwin-arm64-arm-none-eabi/bin:$PATH"

# Navigate to QMK firmware directory
cd ~/code/qmk_firmware
git checkout sofle-procyon

# Compile
QMK_HOME=~/code/qmk_firmware qmk compile -kb lucky_studio/sofle_4x6 -km default
```

This produces `lucky_studio_sofle_4x6_default.uf2` in the QMK root directory.

### Flashing

Each half must be flashed separately. The right half is the USB master (host cable plugs into the right side).

**Enter bootloader** using one of these methods:

1. **Reset combo:** Hold Q + Z + P + / simultaneously for 1 second
2. **Bootmagic:** Hold the top-left key while plugging in USB
3. **VIA trick:** Use Python `hidapi` to send `id_dynamic_keymap_set_keycode` to remap any key to `QK_BOOT`, then press it

**Flash the firmware:**

```bash
cp ~/code/qmk_firmware/lucky_studio_sofle_4x6_default.uf2 /Volumes/RPI-RP2/
```

The RP2040 will unmount and reboot with the new firmware. Repeat for the other half.

---

## Case Design

The case is generated programmatically using Python and SolidPython2. See [`case/README.md`](case/README.md) for full documentation, including:

- Parametric case generator with all dimensions exposed as constants
- Print-in-place touchpad tower (pause at layer 83-84, insert touchpad, resume)
- Interactive web-based PCB annotator for measuring and positioning features
- Pre-built STL files in `case/releases/`

### Quick Start

```bash
pip install solidpython2
cd case/
python generate_case.py
# Open .scad files in OpenSCAD -> F5 to preview, F6 to render STL
```

---

## Build Guide (Summary)

1. **Obtain the PCB** from Lucky Studio (LXF-YZP). This is the Sofle 4x6 variant with RP2040 and touchpad connector.
2. **Obtain a Procyon touchpad module** (57x80mm, Microchip mXT336UD). These are designed by George Norton.
3. **Print the case** -- four pieces total (left top, left bottom, right top with touchpad tower, right bottom). See `case/README.md` for print settings.
4. **Print-in-place touchpad:** When printing the right top plate, pause at layer 83-84 (approximately 16.7mm height), place the touchpad module face-down in the pocket, and resume printing.
5. **Populate switches** -- hot-swap MX switches press into the top plate.
6. **Install encoder** on the left half.
7. **Assemble** with M2 screws through the top plate into the bottom shell standoffs.
8. **Flash firmware** to both halves (right half first, since it is the master).
9. **Connect** USB-C from host to the right half; USB-C interconnect between halves.

---

## Credits

- **josefadamcik** -- [Original Sofle keyboard](https://github.com/josefadamcik/SofleKeyboard) design
- **LXF-YZP / yuezp (Lucky Studio)** -- Sofle 4x6 PCB design with RP2040 and touchpad connector
- **george-norton** -- [Procyon trackpad module](https://github.com/george-norton/qmk_firmware/tree/multitouch_experiment), maxtouch digitizer driver for QMK
- **GarrettFaucher / kb-elmo** -- [Tempest case](https://github.com/GarrettFaucher/Tempest-Keyboard-Case) for original Sofle, used as dimensional reference
- **JeffOwOSun** -- Firmware keymap, gesture emulation, case generator, and PCB measurement pipeline

## License

- **Firmware** (QMK keymap and configuration): [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html), consistent with the QMK project license.
- **Case design** (generator scripts, PCB data, annotator tool): [GPL-2.0](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).
- **Tempest case reference files** (`case/reference/`): Original work by GarrettFaucher, included for dimensional reference only. See the [Tempest repository](https://github.com/GarrettFaucher/Tempest-Keyboard-Case) for its license terms.
