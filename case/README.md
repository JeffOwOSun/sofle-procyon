# Sofle Procyon Case Design

Parametric, programmatically generated case for the Sofle Procyon split keyboard. The case is defined entirely in Python using SolidPython2, which outputs OpenSCAD files that can be previewed, rendered to STL, and 3D printed.

The right half includes a print-in-place touchpad tower that holds the Procyon 57x80mm trackpad module level with the key tops.

## Table of Contents

- [Quick Start](#quick-start)
- [Case Components](#case-components)
- [Dimensions and Parameters](#dimensions-and-parameters)
- [Touchpad Tower](#touchpad-tower)
- [Printing](#printing)
- [PCB Data Pipeline](#pcb-data-pipeline)
- [Interactive Annotator](#interactive-annotator)
- [Modifying the Case](#modifying-the-case)
- [File Reference](#file-reference)
- [Dependencies](#dependencies)

---

## Quick Start

### Generate the case files

```bash
pip install solidpython2
cd case/
python generate_case.py
```

This produces four `.scad` files and (if OpenSCAD is installed) corresponding `.stl` files in `releases/`:

```
releases/
├── procyon_left_top.scad       Left top plate
├── procyon_left_top.stl
├── procyon_left_bottom.scad    Left bottom shell
├── procyon_left_bottom.stl
├── procyon_right_top.scad      Right top plate + touchpad tower
├── procyon_right_top.stl
├── procyon_right_bottom.scad   Right bottom shell
├── procyon_right_bottom.stl
└── procyon_left.3mf            Combined left half (for slicing)
```

### Preview in OpenSCAD

Open any `.scad` file in OpenSCAD:
- **F5** -- Preview (fast, approximate)
- **F6** -- Render (slow, exact -- required before exporting STL)
- **File > Export > STL** to save the rendered mesh

### Use pre-built files

If you just want to print, the `releases/` directory contains ready-to-slice STL and 3MF files.

---

## Case Components

The case consists of **four printed pieces** (two per half):

### Left Top Plate (4.8mm)

- 14mm square switch cutouts with MX clip notches (5mm wide, 1mm deep, 3.8mm tall from bottom -- leaves a 1mm retaining ledge at top)
- 14mm encoder cutout with additional side notches (7mm wide, 2mm deep, 2.5mm tall) for the EC11 encoder tabs
- Countersunk M2 screw holes (2.25mm through-hole, 4mm countersink, 2mm countersink depth)
- USB-C blind recesses on the bottom face (9mm x 6.5mm x 0.5mm) -- shallow relief so the plate sits flush over the port housings

### Left Bottom Shell (12.5mm total)

- 2mm floor thickness
- 10.5mm wall height (2mm wall thickness outset from the PCB outline)
- M2 standoffs at each mounting hole (5mm diameter, 3mm tall, 1.6mm tap hole for friction-fit M2 screws)
- Reset switch through-holes in the floor (4mm x 3mm rectangular, accessible with a paperclip)
- USB-C wall cutouts (12mm x 6mm through the side walls)
- 0.4mm chamfer on top edges

### Right Top Plate (4.8mm + touchpad tower)

Same as the left top plate (mirrored), plus the touchpad tower on the split (inner) side. No encoder cutout on the right half.

### Right Bottom Shell

Same as the left bottom shell (mirrored). The touchpad sits above the top plate, so the bottom shell is identical in structure.

---

## Dimensions and Parameters

All parameters are defined as constants at the top of `generate_case.py` and can be freely modified:

### Top Plate

| Parameter | Value | Description |
|-----------|-------|-------------|
| `PLATE_THICKNESS` | 4.8mm | Top plate height |
| `SWITCH_CUTOUT` | 14.0mm | MX switch hole (square) |
| `SWITCH_CORNER_R` | 0.5mm | Switch cutout corner radius |
| `CLIP_WIDTH` | 5.0mm | MX clip notch width |
| `CLIP_DEPTH` | 1.0mm | Clip notch depth beyond 14mm hole |
| `CLIP_HEIGHT` | 3.8mm | Clip notch height from plate bottom |

### Bottom Shell

| Parameter | Value | Description |
|-----------|-------|-------------|
| `BOTTOM_WALL` | 2.0mm | Wall thickness |
| `BOTTOM_FLOOR` | 2.0mm | Floor thickness |
| `BOTTOM_HEIGHT` | 10.5mm | Internal cavity height |
| `PCB_STANDOFF_H` | 3.0mm | Standoff height above floor |
| `STANDOFF_OD` | 5.0mm | Standoff outer diameter |

### Screws (M2)

| Parameter | Value | Description |
|-----------|-------|-------------|
| `SCREW_D_THROUGH` | 2.25mm | Through-hole diameter (plate + PCB) |
| `SCREW_D_TAP` | 1.6mm | Tap hole diameter in standoffs (friction fit) |
| `SCREW_CSINK_D` | 4.0mm | Countersink diameter |
| `SCREW_CSINK_DEPTH` | 2.0mm | Countersink depth |

### Outline

| Parameter | Value | Description |
|-----------|-------|-------------|
| `CORNER_R` | 2.0mm | Corner rounding radius |
| `CHAMFER` | 0.4mm | Top edge chamfer (45 degrees) |

### USB-C Port Relief

| Parameter | Value | Description |
|-----------|-------|-------------|
| `USB_CUTOUT_W` | 9.0mm | Port width |
| `USB_CUTOUT_H` | 0.5mm | Relief depth into plate bottom |
| `USB_CUTOUT_D` | 6.5mm | Relief reach into plate |

---

## Touchpad Tower

The right top plate includes a tower that holds the Procyon touchpad at the same height as the key tops. It is designed for **print-in-place** assembly -- the touchpad is inserted during printing.

### Tower Geometry

| Parameter | Value | Description |
|-----------|-------|-------------|
| `TP_TOWER_H` | 12.5mm | Tower height above plate surface |
| `TP_EXPAND` | 1.2mm | Tower wall beyond touchpad edge (each side) |
| `TP_CORNER_R` | 2.0mm | Tower corner rounding |
| `TP_THICKNESS` | 1.7mm | Touchpad PCB thickness |
| `TP_LIP` | 0.6mm | Depth of lip above touchpad (retains it) |

The tower is constructed as follows:

1. Start with the touchpad rectangle (57.2 x 80mm)
2. Expand by 1.2mm on all sides (wall thickness)
3. Round corners with 2mm radius
4. Extrude to 12.5mm with a 0.4mm chamfer on top
5. Subtract the touchpad pocket: touchpad-sized rectangle, 1.7mm deep, starting 0.6mm below the tower top
6. Subtract the cable channel: touchpad rectangle shrunk by 15mm on left/right and 22mm on top/bottom, cut from the pocket floor through to the bottom of the tower

### Print-in-Place Procedure

1. Slice the right top plate STL with your normal settings (see [Printing](#printing))
2. Add a **pause at layer 83-84** (approximately 16.7mm from the build plate, which is the top of the pocket floor). The exact layer depends on your layer height; at 0.2mm layers, this is layer 83-84.
3. Print up to the pause
4. When the printer pauses, place the **Procyon touchpad face-down** into the pocket. The sensing surface faces down (toward the build plate). The FPC connector tail should route through the cable channel.
5. Resume printing. The remaining layers print the 0.6mm retaining lip over the touchpad edges, locking it in place.

The touchpad is permanently captured. The cable channel provides clearance for the FPC cable to route down through the plate to the PCB connector below.

---

## Printing

### Recommended Settings

| Setting | Value |
|---------|-------|
| Material | PLA or PETG |
| Layer height | 0.2mm |
| Infill | 20% |
| Supports | None needed |
| Wall count | 3-4 |
| Top/bottom layers | 4-5 |

### Print Orientation

All pieces print in their natural orientation (flat side down):

- **Top plates:** Print upside-down (top surface on the bed) for best surface quality on the visible face. The switch cutouts and screw countersinks face up during printing.
- **Bottom shells:** Print right-side-up (floor on the bed).

### Hardware

- **Screws:** M2 x 8mm flat head (countersunk). The screws pass through the top plate and thread into the standoffs in the bottom shell.
- **No inserts needed.** The standoffs have 1.6mm holes that accept M2 screws via friction fit in printed plastic. If you prefer threaded inserts, increase `SCREW_D_TAP` to match your insert's pilot hole diameter and shorten the standoffs accordingly.

---

## PCB Data Pipeline

The case geometry is derived from physical measurements of the PCBs, stored in `pcb_data.json`. This section describes how those measurements were obtained -- useful if you need to adapt the process for a different keyboard.

### Overview

1. **Scan** both PCB halves and the touchpad on a flatbed scanner at 300 DPI
2. **Normalize** the scan images: rotate to align with axes, flip to consistent top-down orientation
3. **Detect switch positions** using OpenCV circle detection (HoughCircles on the MX pin holes)
4. **Snap to grid**: switch positions are snapped to the known 19mm grid with the Sofle column stagger pattern, using the [Sofle KiCad source](https://github.com/josefadamcik/SofleKeyboard) as reference
5. **Triangulate** mounting holes and thumb key positions using caliper measurements between known points
6. **Refine** positions interactively using the web-based annotator tool

### Column Stagger Reference

These stagger values (vertical offset from the middle column) are taken from the original Sofle KiCad files:

| Column | Stagger (mm) |
|--------|--------------|
| Pinky (outer) | 11.4 |
| Ring | 2.5 |
| Middle | 0 (reference) |
| Index | 2.5 |
| Inner | 5.0 |

### pcb_data.json Format

The data file contains measurements for both halves:

```json
{
  "dimensions": {
    "left_w": 140,
    "right_w": 160.5,
    "extra_w": 20.5,
    "touchpad_w": 57.2,
    "touchpad_h": 80
  },
  "left": {
    "switches": [{"x": 9.1, "y": 20.7, "rotation": 0}, ...],
    "holes": [{"x": 95.4, "y": 23.8, "d": 2.25}, ...],
    "usbc": [{"x": 125.7, "y": 6.7, "w": 9, "h": 3.5, "rotation": 0}, ...],
    "resets": [{"x": 136.4, "y": 65.2}, ...],
    "encoder": {"x": 126, "y": 71.1, "r": 6},
    "trackpad": null,
    "outline_mm": [[x, y], ...],
    "scale": 0.0847,
    "bbox": [123, 118, 1646, 1321],
    "pcb_h_mm": 111.89
  },
  "right": {
    "...same structure...",
    "encoder": null,
    "trackpad": {"x": 16.7, "y": 44.6, "w": 57.2, "h": 80}
  }
}
```

All coordinates are in millimeters, measured from the top-left corner of each PCB in scan orientation (Y increases downward). The generator script flips Y to match OpenSCAD's convention (Y increases upward) via the `flip_y()` function.

Key fields:

- **switches**: Center position of each MX switch cutout, with optional rotation (degrees, for thumb cluster keys)
- **holes**: Mounting hole centers and diameters
- **usbc**: USB-C port center positions, dimensions, and rotation (0 = port faces top edge, 90 = port faces side edge)
- **resets**: Reset button positions (rectangular through-holes in the bottom shell)
- **encoder**: Encoder position and shaft radius (left half only)
- **trackpad**: Touchpad center position and dimensions (right half only)
- **outline_mm**: Ordered vertices of the PCB outline polygon
- **scale**: Pixels-to-mm conversion factor from the scan
- **bbox**: Bounding box in scan pixel coordinates

---

## Interactive Annotator

The annotator (`annotator.html`) is a web-based tool for visually placing and adjusting PCB features on top of the normalized scan images. It can be useful for this project or adapted for any keyboard PCB measurement task.

### Running the Annotator

```bash
cd case/
python server.py
# Open http://localhost:8765/case/annotator.html
```

The server (`server.py`) serves the annotator HTML, PCB scan images from `scans/`, and handles loading/saving `pcb_data.json`.

### Annotator Features

The tool displays both PCB halves side by side with the scan images as backgrounds. Features are overlaid as interactive objects:

| Mode | Shortcut | Description |
|------|----------|-------------|
| Switch | S | Place or drag MX switch positions. Scroll to rotate (Shift for fine adjustment). |
| USB-C | U | Place USB-C port markers |
| Hole | H | Place mounting holes |
| Encoder | E | Place encoder position |
| Trackpad | P | Place touchpad rectangle |
| Reset | R | Place reset button positions |
| Outline | O | Edit PCB outline vertices. Alt+click to add a point. Shift+drag to snap to axis. |
| Measure | M | Click two points to measure the distance between them |
| Delete | D | Click a feature to remove it |

### Keyboard Shortcuts

- **S / U / H / E / P / R / O / D** -- Switch placement mode
- **M** -- Measurement mode
- **N** -- Snap all outline points to the nearest grid
- **Del** -- Delete selected feature
- **Ctrl+S** -- Save to `pcb_data.json`
- **Scroll** -- Rotate selected switch (hold Shift for fine rotation)

### Alignment Tools

Select multiple features (of the same type), then:
- **Align V** -- Align all selected features to the same X coordinate (vertical alignment)
- **Align H** -- Align all selected features to the same Y coordinate (horizontal alignment)

### Saving

Click **Save (Ctrl+S)** to write the current state back to `case/pcb_data.json` via the local server. The **Export JSON** button downloads the data as a standalone file.

### Using the Annotator for Other Keyboards

The annotator is general-purpose. To use it with a different keyboard PCB:

1. Scan your PCBs at 300 DPI
2. Normalize the images (rotate so keys are axis-aligned, crop to PCB bounds)
3. Place the images in `scans/` as `left_half_top.png` and `right_half_top.png`
4. Edit `pcb_data.json` to clear the existing features and set the correct `scale` factor (mm per pixel, calculated from your DPI: `25.4 / DPI`)
5. Run `server.py` and open the annotator
6. Place features by clicking on the scan images
7. Use caliper measurements and the Measure tool to verify accuracy

---

## Modifying the Case

### Changing Dimensions

All case geometry is controlled by the constants at the top of `generate_case.py`. Common modifications:

| Goal | Parameter(s) to change |
|------|----------------------|
| Thicker/thinner plate | `PLATE_THICKNESS` (also adjust `CLIP_HEIGHT` to maintain the retaining ledge) |
| Tighter/looser switch fit | `SWITCH_CUTOUT` (14.0mm is MX spec; try 13.9 for tighter, 14.1 for looser) |
| Different screw size | `SCREW_D_THROUGH`, `SCREW_D_TAP`, `SCREW_CSINK_D` |
| Taller/shorter bottom | `BOTTOM_HEIGHT` (currently sized for PCB + components + clearance) |
| Thicker walls | `BOTTOM_WALL` |
| Touchpad tower height | `TP_TOWER_H` (12.5mm matches SA-profile keycap tops; adjust for other profiles) |
| Larger touchpad tolerance | `TP_EXPAND` (increases wall around touchpad) |

After changing parameters, re-run `python generate_case.py` and open the new `.scad` files in OpenSCAD.

### Changing PCB Layout

If your PCB has different switch positions, mounting holes, or outline:

1. Edit `pcb_data.json` directly, or use the interactive annotator
2. Re-run `generate_case.py`

The generator reads all geometry from `pcb_data.json` -- it has no hardcoded positions.

### Adding Features

The generator is structured as two functions:

- `make_top_plate(side)` -- Returns an OpenSCAD solid for the top plate
- `make_bottom(side)` -- Returns an OpenSCAD solid for the bottom shell

Both use SolidPython2's CSG operations (union `+`, difference `-`). To add a feature, modify the relevant function. For example, to add a display cutout to the top plate, subtract a rectangle at the desired position before the function returns.

### Exporting to Other Formats

The `.scad` files can be opened in OpenSCAD and exported to STL, AMF, or 3MF. For STEP export (useful for further CAD work in Fusion 360 or FreeCAD), convert the STL using a mesh-to-BREP tool or recreate the geometry in your CAD package using the dimensions from `pcb_data.json`.

---

## File Reference

| File | Purpose |
|------|---------|
| `generate_case.py` | Main case generator. Run with `python generate_case.py` to produce SCAD files. |
| `pcb_data.json` | All PCB measurements: switch positions, mounting holes, USB-C ports, outline vertices, encoder, trackpad, reset buttons. |
| `annotator.html` | Interactive web tool for placing and adjusting PCB features on scan images. |
| `server.py` | Simple HTTP server that serves the annotator and handles save/load of `pcb_data.json`. |
| `MODIFICATION_GUIDE.md` | Legacy guide for manual Fusion 360 modifications (superseded by the parametric generator). |
| `reference/` | Tempest case STEP files by GarrettFaucher, used as dimensional reference for the original Sofle case geometry. |
| `releases/` | Generated output: SCAD source, STL meshes, and 3MF files ready for slicing. |

---

## Dependencies

### Required

- **Python 3** (3.8+)
- **SolidPython2** -- `pip install solidpython2`
- **OpenSCAD** -- [openscad.org](https://openscad.org/) (for previewing SCAD files and rendering to STL)

### Optional (for PCB scan analysis)

These are only needed if you want to run the scan-to-measurements pipeline on new PCB images:

- **OpenCV** -- `pip install opencv-python`
- **NumPy** -- `pip install numpy`
- **SciPy** -- `pip install scipy`
- **Pillow** -- `pip install Pillow`

---

## Credits

- **josefadamcik** -- [Original Sofle keyboard](https://github.com/josefadamcik/SofleKeyboard) design
- **GarrettFaucher / kb-elmo** -- [Tempest case](https://github.com/GarrettFaucher/Tempest-Keyboard-Case) for the original Sofle, included in `reference/` as a dimensional starting point
- **george-norton** -- Procyon trackpad module and maxtouch driver
- **LXF-YZP / yuezp (Lucky Studio)** -- Sofle 4x6 PCB design

## License

GPL-2.0. See the repository root for full license terms.

The Tempest case reference files in `reference/` are original work by GarrettFaucher and are included for dimensional reference only. See the [Tempest repository](https://github.com/GarrettFaucher/Tempest-Keyboard-Case) for their license terms.
