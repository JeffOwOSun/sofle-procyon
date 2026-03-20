#!/usr/bin/env python3
"""
Sofle Procyon case generator.

Generates OpenSCAD files for left and right halves.
Right half includes a cutout for the Procyon 57x80 touchpad.

Usage:
    python generate_case.py
    # Then open the .scad files in OpenSCAD to preview and export STL

Dependencies:
    pip install solidpython2
    OpenSCAD (for rendering): /Applications/OpenSCAD.app or brew install openscad
"""

from solid2 import *
from solid2.extensions.bosl2 import *
import subprocess, os, sys

# =============================================================================
# PCB Dimensions (measured from 300 DPI scan)
# =============================================================================

LEFT_PCB_W = 139.9    # mm
LEFT_PCB_H = 111.3    # mm
RIGHT_PCB_W = 160.9   # mm (21mm wider on split side for touchpad)
RIGHT_PCB_H = 112.8   # mm
PCB_THICKNESS = 1.6    # mm

# The right half is wider on the split (inner) side
EXTRA_WIDTH = RIGHT_PCB_W - LEFT_PCB_W  # ~21mm

# =============================================================================
# Touchpad (Procyon 57x80)
# =============================================================================

TP_W = 57.0           # mm
TP_H = 80.0           # mm
TP_THICKNESS = 1.6    # mm
TP_CLEARANCE = 0.5    # mm per side
TP_CUTOUT_W = TP_W + 2 * TP_CLEARANCE   # 58mm
TP_CUTOUT_H = TP_H + 2 * TP_CLEARANCE   # 81mm

# Position: inner (split) side of right half, centered vertically
# X measured from the inner edge of the right half
TP_CENTER_X = TP_W / 2   # 28.5mm from split edge
TP_CENTER_Y = 0           # centered vertically

# =============================================================================
# Case Parameters — TWEAK THESE
# =============================================================================

WALL = 2.0              # wall thickness
FLOOR = 2.0             # bottom thickness
FILLET_R = 3.0           # corner radius
CASE_H = 10.0           # internal height (above floor)
STANDOFF_H = 3.0        # PCB sits this high above floor
STANDOFF_OD = 5.0       # standoff outer diameter
SCREW_D = 2.5           # M2.5 screw hole

# Lip to hold touchpad from above
LIP_W = 1.5             # lip ledge width
LIP_DEPTH = TP_THICKNESS + 0.3  # how deep the lip pocket is

# USB-C cutout
USB_W = 12.0
USB_H = 7.0
USB_Z_OFFSET = STANDOFF_H + PCB_THICKNESS / 2  # center on PCB edge

# =============================================================================
# Mounting holes — PLACEHOLDER positions, adjust after test fit
# Measured from bottom-left corner of each PCB
# =============================================================================

LEFT_MOUNT_HOLES = [
    (10, 10),
    (130, 10),
    (10, 101),
    (130, 101),
    (70, 55),
]

RIGHT_MOUNT_HOLES = [
    (10, 10),
    (151, 10),
    (10, 103),
    (151, 103),
    (80, 55),
]


# =============================================================================
# Generator functions
# =============================================================================

def rounded_box(w, h, z, r):
    """Box with rounded vertical edges."""
    return minkowski()(
        cube([w - 2*r, h - 2*r, z/2], center=True),
        cylinder(r=r, h=z/2, center=True, _fn=32)
    )


def case_shell(pcb_w, pcb_h):
    """Hollow case shell for one half."""
    outer_w = pcb_w + 2 * WALL
    outer_h = pcb_h + 2 * WALL
    total_h = CASE_H + FLOOR

    outer = rounded_box(outer_w, outer_h, total_h, FILLET_R)
    outer = up(total_h / 2)(outer)

    # Hollow interior
    inner = rounded_box(pcb_w, pcb_h, CASE_H + 1, FILLET_R - WALL/2)
    inner = up(FLOOR + CASE_H / 2 + 0.5)(inner)

    return outer - inner


def standoffs(mount_holes, pcb_w, pcb_h):
    """PCB mounting standoffs with screw holes."""
    posts = None
    holes = None
    for (x, y) in mount_holes:
        # Convert from PCB coords (bottom-left origin) to centered coords
        cx = x - pcb_w / 2
        cy = y - pcb_h / 2
        post = translate([cx, cy, FLOOR])(
            cylinder(d=STANDOFF_OD, h=STANDOFF_H, _fn=24)
        )
        hole = translate([cx, cy, 0])(
            cylinder(d=SCREW_D, h=FLOOR + STANDOFF_H + 1, _fn=16)
        )
        posts = post if posts is None else posts + post
        holes = hole if holes is None else holes + hole
    return posts, holes


def usb_cutout(pcb_w, side="top"):
    """USB-C port cutout on the PCB edge."""
    # USB is typically on the top edge, centered
    y_pos = pcb_w / 2 + WALL  # outer wall position... actually on the narrow edge
    # For split keyboards, USB is often on the inner or outer edge
    # Adjust based on actual PCB — placeholder at top center
    return translate([0, pcb_w / 2, FLOOR + USB_Z_OFFSET])(
        rotate([90, 0, 0])(
            cube([USB_W, USB_H, WALL * 3], center=True)
        )
    )


def touchpad_cutout():
    """Rectangular cutout for the Procyon touchpad with retention lip."""
    total_h = CASE_H + FLOOR

    # Through-cut for touchpad surface
    cut = cube([TP_CUTOUT_W, TP_CUTOUT_H, WALL + 2], center=True)
    cut = translate([0, 0, total_h - WALL/2])(cut)

    # Lip pocket (wider than cutout, shallower)
    lip_w = TP_CUTOUT_W + 2 * LIP_W
    lip_h = TP_CUTOUT_H + 2 * LIP_W
    lip = cube([lip_w, lip_h, LIP_DEPTH], center=True)
    lip = translate([0, 0, total_h - WALL - LIP_DEPTH/2 + 0.01])(lip)

    # Subtract the cutout shape so only the lip ledge remains
    lip_cut = cube([TP_CUTOUT_W, TP_CUTOUT_H, LIP_DEPTH + 1], center=True)
    lip_cut = translate([0, 0, total_h - WALL - LIP_DEPTH/2])(lip_cut)

    return cut + (lip - lip_cut)


def make_left():
    """Generate left half case."""
    shell = case_shell(LEFT_PCB_W, LEFT_PCB_H)
    posts, holes = standoffs(LEFT_MOUNT_HOLES, LEFT_PCB_W, LEFT_PCB_H)
    return shell + posts - holes


def make_right():
    """Generate right half case with touchpad cutout."""
    shell = case_shell(RIGHT_PCB_W, RIGHT_PCB_H)
    posts, holes = standoffs(RIGHT_MOUNT_HOLES, RIGHT_PCB_W, RIGHT_PCB_H)

    # Position touchpad cutout on the split (inner) side
    # Inner edge is at x = -RIGHT_PCB_W/2 (leftmost in centered coords)
    # Touchpad center is TP_CENTER_X from that edge
    tp_x = -RIGHT_PCB_W / 2 + TP_CENTER_X
    tp_y = TP_CENTER_Y

    tp_cut = translate([tp_x, tp_y, 0])(touchpad_cutout())

    return shell + posts - holes - tp_cut


def render_scad(obj, filename):
    """Save as .scad file."""
    scad_path = os.path.join("releases", filename)
    obj.save_as_scad(scad_path)
    print(f"  -> {scad_path}")
    return scad_path


def render_stl(scad_path):
    """Render .scad to .stl using OpenSCAD CLI."""
    stl_path = scad_path.replace(".scad", ".stl")
    openscad = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
    if not os.path.exists(openscad):
        openscad = "openscad"
    try:
        subprocess.run([openscad, "-o", stl_path, scad_path],
                      check=True, capture_output=True, timeout=120)
        print(f"  -> {stl_path}")
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  STL render skipped ({e}). Open .scad in OpenSCAD to export.")


if __name__ == "__main__":
    os.makedirs("releases", exist_ok=True)

    print("Generating Sofle Procyon case...")
    print(f"  Left:  {LEFT_PCB_W}x{LEFT_PCB_H}mm")
    print(f"  Right: {RIGHT_PCB_W}x{RIGHT_PCB_H}mm (touchpad: {TP_W}x{TP_H}mm)")
    print()

    print("Left half:")
    left_scad = render_scad(make_left(), "procyon_left.scad")
    render_stl(left_scad)

    print("Right half:")
    right_scad = render_scad(make_right(), "procyon_right.scad")
    render_stl(right_scad)

    print("\nDone! Open .scad files in OpenSCAD to preview.")
    print("Adjust parameters at the top of generate_case.py and re-run.")
