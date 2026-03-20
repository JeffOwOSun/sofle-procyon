"""
Sofle Procyon case generator.

Left half: Tempest Sofle Case (unchanged) — use reference/Tempest Top.step
Right half: Tempest case mirrored + widened 21mm on split side for touchpad

Base design: https://github.com/GarrettFaucher/Tempest-Sofle-Case
Measurements from 300 DPI PCB scan.

Requirements:
    conda install -c conda-forge cadquery
    # OR manually modify STEP files in Fusion360 (see MODIFICATION_GUIDE.md)
"""

# =============================================================================
# Measured dimensions (from 300 DPI scan)
# =============================================================================

# PCB sizes
LEFT_PCB_WIDTH = 139.9      # mm
LEFT_PCB_HEIGHT = 111.3     # mm
RIGHT_PCB_WIDTH = 160.9     # mm — 21mm wider than left
RIGHT_PCB_HEIGHT = 112.8    # mm

# The extra width on the right half is on the SPLIT side (inner edge)
# This is where the touchpad stacks on top of the PCB
EXTRA_WIDTH = RIGHT_PCB_WIDTH - LEFT_PCB_WIDTH  # ~21mm

# Procyon touchpad (57x80 variant, measured 56.7x79.5 from scan)
TOUCHPAD_WIDTH = 57.0       # mm (along split edge direction)
TOUCHPAD_HEIGHT = 80.0      # mm (along key column direction)
TOUCHPAD_THICKNESS = 1.6    # mm (PCB)
TOUCHPAD_CLEARANCE = 0.5    # mm extra per side for fit

# Touchpad cutout position on right half case
# X: centered in the extra-width zone on the split (inner) side
# Y: centered vertically on the case
CUTOUT_WIDTH = TOUCHPAD_WIDTH + 2 * TOUCHPAD_CLEARANCE   # 58mm
CUTOUT_HEIGHT = TOUCHPAD_HEIGHT + 2 * TOUCHPAD_CLEARANCE  # 81mm

# Cutout center relative to the right half case
# X = 0 is the split (inner) edge of the right half
# The extra 21mm zone spans X=[0, 21]. Touchpad (57mm) is wider than
# the extra zone, so it extends partly over the main PCB area.
# Center it on the split edge:
CUTOUT_CENTER_X_FROM_SPLIT = TOUCHPAD_WIDTH / 2  # 28.5mm from split edge
CUTOUT_CENTER_Y = RIGHT_PCB_HEIGHT / 2           # centered vertically

# Lip to hold touchpad
LIP_WIDTH = 1.5    # mm ledge around cutout
LIP_DEPTH = 1.0    # mm below top surface

# =============================================================================
# Case parameters
# =============================================================================

WALL_THICKNESS = 2.0
BOTTOM_THICKNESS = 2.0
CASE_INTERNAL_HEIGHT = 10.0
PCB_STANDOFF_HEIGHT = 3.0


def print_dimensions():
    """Print all key dimensions for reference."""
    print("=" * 60)
    print("SOFLE PROCYON CASE DIMENSIONS")
    print("=" * 60)
    print(f"Left PCB:       {LEFT_PCB_WIDTH:.1f} x {LEFT_PCB_HEIGHT:.1f} mm")
    print(f"Right PCB:      {RIGHT_PCB_WIDTH:.1f} x {RIGHT_PCB_HEIGHT:.1f} mm")
    print(f"Extra width:    {EXTRA_WIDTH:.1f} mm (split side)")
    print(f"Touchpad:       {TOUCHPAD_WIDTH:.1f} x {TOUCHPAD_HEIGHT:.1f} mm")
    print(f"Touchpad cutout:{CUTOUT_WIDTH:.1f} x {CUTOUT_HEIGHT:.1f} mm")
    print(f"Cutout center:  {CUTOUT_CENTER_X_FROM_SPLIT:.1f}mm from split edge, "
          f"{CUTOUT_CENTER_Y:.1f}mm from top")
    print()
    print("LEFT HALF: Use Tempest case unchanged (reference/Tempest Top.step)")
    print("RIGHT HALF: Mirror Tempest + extend split side 21mm + add touchpad cutout")
    print()
    print("Fusion360 steps:")
    print(f"  1. Import & mirror Tempest Top.step")
    print(f"  2. Extend the split (inner) edge by {EXTRA_WIDTH:.0f}mm")
    print(f"  3. Cut a {CUTOUT_WIDTH:.0f}x{CUTOUT_HEIGHT:.0f}mm rectangle through the top")
    print(f"     positioned {CUTOUT_CENTER_X_FROM_SPLIT:.1f}mm from split edge, centered vertically")
    print(f"  4. Add {LIP_WIDTH}mm lip at {LIP_DEPTH}mm depth for touchpad to rest on")
    print(f"  5. Repeat for the bottom piece")
    print("=" * 60)


try:
    import cadquery as cq
    CADQUERY_AVAILABLE = True
except ImportError:
    CADQUERY_AVAILABLE = False


def generate_with_cadquery():
    """Generate case using CadQuery (requires conda install)."""
    import os
    os.makedirs("releases", exist_ok=True)

    print("Loading Tempest Top...")
    top = cq.importers.importStep("reference/Tempest Top.step")
    bb = top.val().BoundingBox()
    print(f"  Tempest bounds: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm")

    # Mirror for right half
    right_top = top.mirror("YZ")
    bb_r = right_top.val().BoundingBox()

    # The split edge is now at x_max (rightmost edge after mirror)
    split_edge_x = bb_r.xmax

    # Extend the split side by EXTRA_WIDTH
    # Add a box on the split edge
    extension = (
        cq.Workplane("XY")
        .transformed(offset=(split_edge_x + EXTRA_WIDTH / 2,
                             (bb_r.ymin + bb_r.ymax) / 2,
                             (bb_r.zmin + bb_r.zmax) / 2))
        .box(EXTRA_WIDTH, bb_r.ylen, bb_r.zlen)
    )
    right_top = right_top.union(extension)

    # Cut touchpad opening
    cutout_x = split_edge_x + CUTOUT_CENTER_X_FROM_SPLIT
    cutout_y = (bb_r.ymin + bb_r.ymax) / 2
    right_top = (
        right_top
        .workplane(origin=(cutout_x, cutout_y, bb_r.zmax), normal=(0, 0, 1))
        .rect(CUTOUT_WIDTH, CUTOUT_HEIGHT)
        .cutThruAll()
    )

    cq.exporters.export(right_top, "releases/procyon_right_top.step")
    cq.exporters.export(right_top, "releases/procyon_right_top.stl")
    print("-> releases/procyon_right_top.step")
    print("-> releases/procyon_right_top.stl")

    # Bottom piece
    print("Loading Tempest Bottom...")
    bottom = cq.importers.importStep("reference/Tempest Bottom.step")
    right_bottom = bottom.mirror("YZ")
    bb_rb = right_bottom.val().BoundingBox()

    extension_b = (
        cq.Workplane("XY")
        .transformed(offset=(bb_rb.xmax + EXTRA_WIDTH / 2,
                             (bb_rb.ymin + bb_rb.ymax) / 2,
                             (bb_rb.zmin + bb_rb.zmax) / 2))
        .box(EXTRA_WIDTH, bb_rb.ylen, bb_rb.zlen)
    )
    right_bottom = right_bottom.union(extension_b)

    cq.exporters.export(right_bottom, "releases/procyon_right_bottom.step")
    cq.exporters.export(right_bottom, "releases/procyon_right_bottom.stl")
    print("-> releases/procyon_right_bottom.step")
    print("-> releases/procyon_right_bottom.stl")


if __name__ == "__main__":
    print_dimensions()

    if CADQUERY_AVAILABLE:
        print("\nCadQuery found. Generating...")
        generate_with_cadquery()
    else:
        print("\nCadQuery not available (needs: conda install -c conda-forge cadquery)")
        print("Use Fusion360 with the STEP files and dimensions above.")
