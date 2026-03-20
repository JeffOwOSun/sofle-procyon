"""
Sofle Procyon case generator.

Usage:
    python generate_case.py

Generates STL files for left and right halves.
Dimensions are derived from PCB scans in ../scans/

Dependencies:
    pip install cadquery
    # For visualization: pip install jupyter-cadquery
"""

import cadquery as cq

# =============================================================================
# PCB Dimensions — UPDATE THESE FROM SCANS
# All measurements in mm
# =============================================================================

# PCB outline points (x, y) — trace from scan
# Placeholder: rough rectangle. Replace with actual traced outline.
PCB_WIDTH = 130.0      # left-right extent of one half
PCB_HEIGHT = 110.0     # top-bottom extent of one half
PCB_THICKNESS = 1.6    # standard PCB thickness
PCB_CORNER_RADIUS = 3.0

# Mounting hole positions (x, y) relative to PCB bottom-left — measure from scan
MOUNT_HOLES = [
    # (x, y) — placeholder positions, replace with actual
    (5, 5),
    (125, 5),
    (5, 105),
    (125, 105),
    (65, 55),
]
MOUNT_HOLE_DIAMETER = 2.5  # M2.5

# Touchpad cutout (right half only) — position relative to PCB origin
TOUCHPAD_X = 40.0       # left edge of cutout
TOUCHPAD_Y = 20.0       # bottom edge of cutout
TOUCHPAD_WIDTH = 57.0   # Procyon 57x80
TOUCHPAD_HEIGHT = 80.0
TOUCHPAD_CORNER_RADIUS = 2.0

# Encoder cutout (left half only)
ENCODER_X = 10.0
ENCODER_Y = 50.0
ENCODER_DIAMETER = 7.0

# USB-C cutout
USB_WIDTH = 12.0
USB_HEIGHT = 7.0

# =============================================================================
# Case Parameters
# =============================================================================

WALL_THICKNESS = 2.0
BOTTOM_THICKNESS = 2.0
CASE_HEIGHT = 10.0       # total internal height above PCB bottom
PCB_STANDOFF_HEIGHT = 3.0  # PCB sits this high above case floor
STANDOFF_OUTER_DIAMETER = 5.0


def make_base_shell(width, height):
    """Create the basic case shell."""
    case = (
        cq.Workplane("XY")
        .rect(width + 2 * WALL_THICKNESS, height + 2 * WALL_THICKNESS)
        .extrude(CASE_HEIGHT + BOTTOM_THICKNESS)
        .edges("|Z").fillet(PCB_CORNER_RADIUS + WALL_THICKNESS)
    )

    # Hollow out
    case = (
        case.faces(">Z").workplane()
        .rect(width, height)
        .cutBlind(-(CASE_HEIGHT))
        .edges("|Z and (not <Z)").fillet(PCB_CORNER_RADIUS)
    )

    return case


def add_standoffs(case, mount_holes, width, height):
    """Add PCB mounting standoffs."""
    # Offset mount holes to case coordinate system (centered)
    offset_holes = [(x - width / 2, y - height / 2) for x, y in mount_holes]

    case = (
        case.faces("<Z").workplane(offset=BOTTOM_THICKNESS)
        .pushPoints(offset_holes)
        .circle(STANDOFF_OUTER_DIAMETER / 2)
        .extrude(PCB_STANDOFF_HEIGHT)
    )

    # Drill screw holes through standoffs
    case = (
        case.faces("<Z").workplane()
        .pushPoints(offset_holes)
        .hole(MOUNT_HOLE_DIAMETER, BOTTOM_THICKNESS + PCB_STANDOFF_HEIGHT)
    )

    return case


def make_left_half():
    """Generate the left half case."""
    case = make_base_shell(PCB_WIDTH, PCB_HEIGHT)
    case = add_standoffs(case, MOUNT_HOLES, PCB_WIDTH, PCB_HEIGHT)
    # TODO: Add encoder cutout, USB-C cutout
    return case


def make_right_half():
    """Generate the right half case (with touchpad cutout)."""
    case = make_base_shell(PCB_WIDTH, PCB_HEIGHT)
    case = add_standoffs(case, MOUNT_HOLES, PCB_WIDTH, PCB_HEIGHT)
    # TODO: Add touchpad cutout, USB-C cutout
    return case


if __name__ == "__main__":
    import os

    os.makedirs("releases", exist_ok=True)

    print("Generating left half...")
    left = make_left_half()
    cq.exporters.export(left, "releases/sofle_procyon_left.stl")
    print("  -> releases/sofle_procyon_left.stl")

    print("Generating right half...")
    right = make_right_half()
    cq.exporters.export(right, "releases/sofle_procyon_right.stl")
    print("  -> releases/sofle_procyon_right.stl")

    print("Done! Update dimensions in this file after scanning the PCB.")
