# Modifying the Tempest Case for Procyon Touchpad

## Base Design
[Tempest Sofle Case](https://github.com/GarrettFaucher/Tempest-Sofle-Case) by kb-elmo/GarrettFaucher. STEP files in `reference/`.

## What Needs Changing
Only the **right half top** needs modification — add a rectangular cutout for the Procyon 57x80mm touchpad.

## Procyon Touchpad Dimensions
- Active area: 57mm x 80mm
- PCB thickness: ~1.6mm
- Corner radius: ~2mm
- FPC connector protrudes from one edge (bottom)

Full KiCad source: https://github.com/george-norton/procyon (57x80 variant)

## Fusion360 Steps

1. **Import** `reference/Tempest Top.step`
2. The Tempest is designed for the LEFT half. **Mirror** it (Edit > Mirror) across YZ plane to get the right half shape
3. **Sketch** on the top face:
   - Rectangle 58mm x 81mm (touchpad + 0.5mm clearance each side)
   - Position: center it where the touchpad sits on your PCB (measure from scan)
   - Fillet corners: 2mm radius
4. **Extrude cut** through the top shell
5. **Add lip/ledge** (optional but recommended):
   - Offset the cutout outline outward by 1.5mm
   - Extrude a 1mm deep pocket from the inside
   - This creates a shelf for the touchpad PCB to rest on
6. **Export** as STL for printing

## Measurement Workflow
1. Scan the right PCB half at 300 DPI
2. In any image editor, measure:
   - Distance from PCB edge to touchpad center (X and Y)
   - Mounting hole positions
3. Update the offsets in `generate_case.py` or position the sketch in Fusion360

## Printing Notes
- Material: PLA or PETG
- Layer height: 0.2mm
- No supports needed (Tempest design)
- Heat-set inserts: M2 x 4mm
