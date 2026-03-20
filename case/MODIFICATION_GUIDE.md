# Sofle Procyon Case Design

## Measured Dimensions (from 300 DPI scan)

| Part | Width | Height |
|------|-------|--------|
| Left PCB | 139.9mm | 111.3mm |
| Right PCB | 160.9mm | 112.8mm |
| Procyon touchpad | 57mm | 80mm |

The right half is **21mm wider** than the left. The extra width is on the **split (inner) side** — this is where the Procyon touchpad stacks on top of the PCB.

## Case Strategy

- **Left half**: Tempest Sofle Case unchanged (`reference/Tempest Top.step` + `Tempest Bottom.step`)
- **Right half**: Mirrored Tempest + extended 21mm on split side + touchpad cutout

## Fusion360 Modification Steps

### Right Half Top

1. **Import** `reference/Tempest Top.step`
2. **Mirror** across YZ plane (Edit > Mirror) to get right half orientation
3. **Extend the split edge** (the inner edge, closest to where the left half would be):
   - Sketch on the split-side face
   - Extrude outward by **21mm**
   - Match the wall height and fillet to the existing case
4. **Add touchpad cutout** on the top surface:
   - Sketch a **58mm x 81mm** rectangle (57mm touchpad + 0.5mm clearance each side)
   - Position: **28.5mm from split edge**, **centered vertically**
   - Fillet corners: 2mm
   - **Extrude cut** through the top
5. **Add retention lip** (optional):
   - Offset the cutout outline outward by 1.5mm
   - Cut a 1mm deep pocket from the inside surface
   - The touchpad PCB rests on this ledge

### Right Half Bottom

1. **Import** `reference/Tempest Bottom.step`
2. **Mirror** across YZ plane
3. **Extend the split edge** by 21mm (same as top)
4. No touchpad cutout needed on bottom

## Printing

- Material: PLA or PETG
- Layer height: 0.2mm
- Infill: 20%
- No supports needed (Tempest design)
- Hardware: M2 x 4mm heat-set threaded inserts

## Automated Generation

If you have CadQuery installed (`conda install -c conda-forge cadquery`):
```bash
cd case/
python generate_case.py
```

This generates STEP and STL files in `case/releases/`.
