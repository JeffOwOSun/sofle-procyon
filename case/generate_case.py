"""
Sofle Procyon case generator.

Modifies the Tempest Sofle Case (by kb-elmo/GarrettFaucher) to add
a Procyon 57x80mm touchpad cutout on the right half.

Base design: https://github.com/GarrettFaucher/Tempest-Sofle-Case
Reference STEP files are in ./reference/

Requirements:
    conda install -c conda-forge cadquery
    # OR use Fusion360 with the STEP files directly

Usage:
    python generate_case.py
"""

import cadquery as cq
import os

# =============================================================================
# Procyon Touchpad Dimensions (from george-norton/procyon 57x80 variant)
# =============================================================================

TOUCHPAD_WIDTH = 57.0       # mm (X direction)
TOUCHPAD_HEIGHT = 80.0      # mm (Y direction)
TOUCHPAD_THICKNESS = 1.6    # mm (PCB thickness)
TOUCHPAD_CORNER_RADIUS = 2.0
TOUCHPAD_CLEARANCE = 0.5    # extra mm on each side for fit

# Cutout dimensions (touchpad + clearance)
CUTOUT_WIDTH = TOUCHPAD_WIDTH + 2 * TOUCHPAD_CLEARANCE
CUTOUT_HEIGHT = TOUCHPAD_HEIGHT + 2 * TOUCHPAD_CLEARANCE

# Position of touchpad center relative to the right half case center
# ADJUST THESE after scanning PCB — these are estimates
TOUCHPAD_OFFSET_X = 0.0     # mm from case center (positive = right)
TOUCHPAD_OFFSET_Y = -5.0    # mm from case center (positive = up)

# Lip to hold touchpad (sits on a ledge inside the cutout)
LIP_WIDTH = 1.5             # mm ledge around cutout
LIP_DEPTH = 1.0             # mm below top surface


def modify_right_top():
    """Load the Tempest Top and add a touchpad cutout for the right half."""
    top = cq.importers.importStep("reference/Tempest Top.step")
    bb = top.val().BoundingBox()

    # Center of the case
    cx = (bb.xmin + bb.xmax) / 2 + TOUCHPAD_OFFSET_X
    cy = (bb.ymin + bb.ymax) / 2 + TOUCHPAD_OFFSET_Y

    # Cut the touchpad opening through the top
    top = (
        top.workplane(origin=(cx, cy, bb.zmax), normal=(0, 0, 1))
        .rect(CUTOUT_WIDTH, CUTOUT_HEIGHT)
        .cutThruAll()
    )

    # Add a lip/ledge for the touchpad to sit on
    top = (
        top.workplane(origin=(cx, cy, bb.zmax - LIP_DEPTH), normal=(0, 0, 1))
        .rect(CUTOUT_WIDTH + 2 * LIP_WIDTH, CUTOUT_HEIGHT + 2 * LIP_WIDTH)
        .rect(CUTOUT_WIDTH, CUTOUT_HEIGHT, forConstruction=True)
        .cutBlind(-LIP_DEPTH)
    )

    return top


def mirror_for_right(shape):
    """Mirror the left-half case to create a right half."""
    return shape.mirror("YZ")


if __name__ == "__main__":
    os.makedirs("releases", exist_ok=True)

    print("Loading Tempest Top...")
    print("NOTE: Adjust TOUCHPAD_OFFSET_X/Y after scanning the PCB")
    print()

    try:
        right_top = modify_right_top()
        cq.exporters.export(right_top, "releases/procyon_right_top.step")
        cq.exporters.export(right_top, "releases/procyon_right_top.stl")
        print("-> releases/procyon_right_top.step")
        print("-> releases/procyon_right_top.stl")
    except Exception as e:
        print(f"CadQuery error: {e}")
        print()
        print("If CadQuery/OCP is not installed, modify the STEP files")
        print("directly in Fusion360. See MODIFICATION_GUIDE.md")

    print()
    print("Left half: use Tempest Top/Bottom unchanged (reference/)")
    print("Right half bottom: use Tempest Bottom unchanged (reference/)")
