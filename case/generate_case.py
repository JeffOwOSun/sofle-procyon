#!/usr/bin/env python3
"""
Sofle Procyon case generator.

Generates OpenSCAD files for:
- Left bottom (PCB tray with standoffs)
- Left top plate (4.8mm with 14mm switch cutouts)
- Right bottom (PCB tray with standoffs)
- Right top plate (4.8mm with switch cutouts + trackpad cutout)

Usage:
    python generate_case.py
    # Open .scad files in OpenSCAD to preview (F5) and render (F6)
"""

from solid2 import *
import json, os

# Load PCB data
with open(os.path.join(os.path.dirname(__file__), 'pcb_data.json')) as f:
    D = json.load(f)

# =============================================================================
# Parameters
# =============================================================================

PLATE_THICKNESS = 4.8       # top plate thickness
SWITCH_CUTOUT = 14.0        # MX switch hole size
SWITCH_CORNER_R = 0.5       # slight corner radius on cutouts

# MX clip notches (top and bottom of each switch cutout)
CLIP_WIDTH = 5.0            # width of clip notch
CLIP_DEPTH = 1.0            # how far notch extends beyond the 14mm cutout
CLIP_HEIGHT = 3.8           # height of notch (from bottom of plate)
# With 4.8mm plate, this leaves a 1mm ledge at the top

BOTTOM_WALL = 2.0           # bottom case wall thickness
BOTTOM_FLOOR = 2.0          # floor thickness
BOTTOM_HEIGHT = 10.5        # internal height (7.5mm plate-to-PCB gap + 3mm standoff)
PCB_STANDOFF_H = 3.0        # PCB sits this high
STANDOFF_OD = 5.0           # standoff outer diameter
SCREW_D_THROUGH = 2.25      # through-hole diameter (plate, matches PCB holes)
SCREW_D_TAP = 1.6           # tap hole diameter for M2 friction fit (in standoffs)
SCREW_CSINK_D = 4.0         # countersink diameter on top plate
SCREW_CSINK_DEPTH = 2.0     # countersink depth (M2 flat head)

CORNER_R = 2.0              # corner rounding radius for outline vertices

# Trackpad tower
TP_TOWER_H = 12.5           # tower height above plate top surface
TP_EXPAND = 1.2             # tower larger than touchpad on each side
TP_CORNER_R = 2.0           # tower corner rounding
TP_THICKNESS = 1.7          # touchpad PCB thickness
TP_LIP = 0.6               # lip depth from top (touchpad sits this far below tower top)
TP_CABLE_SHRINK_X = 15.0     # cable cutout shrink from touchpad edge (left/right)
TP_CABLE_SHRINK_Y = 22.0     # cable cutout shrink from touchpad edge (top/bottom)

USB_CUTOUT_W = 9.0          # USB-C port cutout width (along port direction)
USB_CUTOUT_H = 0.5          # USB-C port cutout height (tiny protrusion above PCB)
USB_CUTOUT_D = 6.5          # USB-C port cutout depth (into the plate from bottom)


def flip_y(data):
    """Flip Y coordinates (scan Y-down to OpenSCAD Y-up)."""
    h = data.get('pcb_h_mm', max(p[1] for p in data['outline_mm']))
    flipped = dict(data)
    flipped['outline_mm'] = [(x, h - y) for x, y in data['outline_mm']]
    flipped['switches'] = [{'x': s['x'], 'y': round(h - s['y'], 2), 'rotation': -s.get('rotation', 0)} for s in data['switches']]
    flipped['holes'] = [{'x': ho['x'], 'y': round(h - ho['y'], 2), 'd': ho.get('d', SCREW_D_THROUGH)} for ho in data.get('holes', [])]
    flipped['usbc'] = [{'x': u['x'], 'y': round(h - u['y'], 2), 'w': u.get('w', 9), 'h': u.get('h', 3.5), 'rotation': u.get('rotation', 0)} for u in data.get('usbc', [])]
    flipped['resets'] = [{'x': r['x'], 'y': round(h - r['y'], 2)} for r in data.get('resets', [])]
    if data.get('encoder'):
        e = data['encoder']
        flipped['encoder'] = {'x': e['x'], 'y': round(h - e['y'], 2), 'r': e.get('r', 6)}
    if data.get('trackpad'):
        t = data['trackpad']
        flipped['trackpad'] = {'x': t['x'], 'y': round(h - t['y'], 2), 'w': t['w'], 'h': t['h']}
    return flipped

def outline_to_polygon(outline_pts):
    """Convert outline points [(x,y),...] to an OpenSCAD polygon."""
    # Remove zero-length edges
    cleaned = [outline_pts[0]]
    for p in outline_pts[1:]:
        if p != cleaned[-1]:
            cleaned.append(p)
    return polygon(cleaned)


def rounded_outline(outline_pts, corner_r=CORNER_R):
    """Create outline with 2mm rounded corners using shrink-expand trick."""
    return offset(r=corner_r)(offset(delta=-corner_r)(outline_to_polygon(outline_pts)))


def make_top_plate(side):
    """Generate a top plate with switch cutouts.
    Flow: 1. contour -> 2. round 2mm -> 3. extrude 4.8mm -> 4. punch holes
          5. blind USB-C -> 6. blind clip notches -> 7. blind encoder side notches
    """
    data = flip_y(D[side])
    outline = data['outline_mm']
    switches = data['switches']

    # Step 1-3: Create contour, round corners, extrude
    plate = linear_extrude(PLATE_THICKNESS)(
        rounded_outline(outline)
    )

    # Cut switch holes with clip notches
    for sw in switches:
        # Main 14mm through-hole
        cut = cube([SWITCH_CUTOUT, SWITCH_CUTOUT, PLATE_THICKNESS + 2], center=True)

        # Clip notches: top and bottom of the cutout, centered on X
        # They extend CLIP_DEPTH beyond the 14mm hole on the Y axis
        # Height is CLIP_HEIGHT from the bottom, leaving a ledge at the top
        notch_y_offset = SWITCH_CUTOUT / 2 + CLIP_DEPTH / 2
        notch = cube([CLIP_WIDTH, CLIP_DEPTH, CLIP_HEIGHT], center=True)
        # Position notch: bottom-aligned (center at CLIP_HEIGHT/2 from z=0)
        notch_z = -PLATE_THICKNESS / 2 + CLIP_HEIGHT / 2
        top_notch = translate([0, notch_y_offset, notch_z])(notch)
        bottom_notch = translate([0, -notch_y_offset, notch_z])(notch)

        switch_cut = cut + top_notch + bottom_notch

        if sw.get('rotation', 0):
            switch_cut = rotate([0, 0, sw['rotation']])(switch_cut)
        switch_cut = translate([sw['x'], sw['y'], PLATE_THICKNESS / 2])(switch_cut)
        plate -= switch_cut

    # Cut mounting holes through plate with countersink
    for h in data.get('holes', []):
        # Through hole
        plate -= translate([h['x'], h['y'], -1])(
            cylinder(d=SCREW_D_THROUGH, h=PLATE_THICKNESS + 2, _fn=16)
        )
        # Countersink from top
        plate -= translate([h['x'], h['y'], PLATE_THICKNESS - SCREW_CSINK_DEPTH])(
            cylinder(d=SCREW_CSINK_D, h=SCREW_CSINK_DEPTH + 1, _fn=24)
        )

    # Cut encoder hole (same as switch cutout + side notches)
    if data.get('encoder'):
        enc = data['encoder']
        # Main 14mm square through-hole
        enc_cut = cube([SWITCH_CUTOUT, SWITCH_CUTOUT, PLATE_THICKNESS + 2], center=True)

        # Top/bottom clip notches (same as switch)
        notch_y_offset = SWITCH_CUTOUT / 2 + CLIP_DEPTH / 2
        notch = cube([CLIP_WIDTH, CLIP_DEPTH, CLIP_HEIGHT], center=True)
        notch_z = -PLATE_THICKNESS / 2 + CLIP_HEIGHT / 2
        enc_cut += translate([0, notch_y_offset, notch_z])(notch)
        enc_cut += translate([0, -notch_y_offset, notch_z])(notch)

        # Left/right side notches: 7mm wide, 2mm deep, 2.5mm height from bottom
        ENC_SIDE_W = 7.0
        ENC_SIDE_DEPTH = 2.0
        ENC_SIDE_H = 2.5
        side_notch = cube([ENC_SIDE_DEPTH, ENC_SIDE_W, ENC_SIDE_H], center=True)
        side_x_offset = SWITCH_CUTOUT / 2 + ENC_SIDE_DEPTH / 2
        side_z = -PLATE_THICKNESS / 2 + ENC_SIDE_H / 2
        enc_cut += translate([side_x_offset, 0, side_z])(side_notch)
        enc_cut += translate([-side_x_offset, 0, side_z])(side_notch)

        enc_cut = translate([enc['x'], enc['y'], PLATE_THICKNESS / 2])(enc_cut)
        plate -= enc_cut

    # Trackpad tower (print-in-place, right half)
    if data.get('trackpad'):
        tp = data['trackpad']
        tp_w = tp['w']   # 57.2
        tp_h = tp['h']   # 80.0

        # Step 1: Touchpad contour (rectangle)
        tp_rect = square([tp_w, tp_h], center=True)

        # Step 2: Expand by 1.2mm on all sides
        tower_2d = offset(delta=TP_EXPAND)(tp_rect)

        # Step 3: Round corners by 2mm
        tower_2d = offset(r=TP_CORNER_R)(offset(delta=-TP_CORNER_R)(tower_2d))

        # Step 4: Extrude tower 12.5mm from plate top surface
        tower = linear_extrude(TP_TOWER_H)(tower_2d)

        # Step 5 (subtracted later): Touchpad pocket
        # From 0.6mm below top of tower, depth = TP_THICKNESS (1.7mm)
        # So pocket starts at z = TP_TOWER_H - TP_LIP - TP_THICKNESS
        pocket_z = TP_TOWER_H - TP_LIP - TP_THICKNESS
        pocket = translate([0, 0, pocket_z])(
            linear_extrude(TP_THICKNESS + 0.01)(tp_rect)
        )

        # Step 6: Cable cutout — shrink touchpad contour asymmetrically, through-cut from pocket bottom to tower bottom
        cable_w = tp_w - 2 * TP_CABLE_SHRINK_X
        cable_h = tp_h - 2 * TP_CABLE_SHRINK_Y
        cable_2d = square([cable_w, cable_h], center=True)
        cable = translate([0, 0, -1])(
            linear_extrude(pocket_z + 1.01)(cable_2d)
        )

        # Combine: tower - pocket - cable
        tower_assembly = tower - pocket - cable

        # Position: top edge of tower at y=108 (aligned with top plate edge)
        tower_outer_h = tp_h + 2 * TP_EXPAND
        tower_top_y = 109.0 + TP_EXPAND
        tower_y = tower_top_y - tower_outer_h / 2
        tower_x = tp['x'] - TP_EXPAND

        tower_assembly = translate([tower_x, tower_y, PLATE_THICKNESS])(tower_assembly)
        plate += tower_assembly

        # Cut cable routing hole through the plate under the tower
        plate -= translate([tower_x, tower_y, PLATE_THICKNESS / 2])(
            cube([cable_w, cable_h, PLATE_THICKNESS + 2], center=True)
        )

    # Cut USB-C port recesses (blind cut from bottom, not through)
    for port in data.get('usbc', []):
        usb_cut = cube([USB_CUTOUT_W, USB_CUTOUT_D, USB_CUTOUT_H], center=True)
        if port.get('rotation', 0):
            usb_cut = rotate([0, 0, port['rotation']])(usb_cut)
        # Position at bottom of plate (z = USB_CUTOUT_H/2 from z=0)
        usb_cut = translate([port['x'], port['y'], USB_CUTOUT_H / 2])(usb_cut)
        plate -= usb_cut

    return plate


def make_bottom(side):
    """Generate a bottom case with walls and PCB standoffs."""
    data = flip_y(D[side])
    outline = data['outline_mm']
    total_h = BOTTOM_FLOOR + BOTTOM_HEIGHT

    # Outer shell (outline + wall thickness)
    outer = linear_extrude(total_h)(
        offset(delta=BOTTOM_WALL)(rounded_outline(outline))
    )

    # Inner cavity (same as outline)
    inner = translate([0, 0, BOTTOM_FLOOR])(
        linear_extrude(BOTTOM_HEIGHT + 1)(
            rounded_outline(outline)
        )
    )

    shell = outer - inner

    # Standoffs at mounting holes
    for h in data.get('holes', []):
        # Standoff cylinder
        post = translate([h['x'], h['y'], BOTTOM_FLOOR])(
            cylinder(d=STANDOFF_OD, h=PCB_STANDOFF_H, _fn=24)
        )
        # Screw hole through standoff (tap diameter for M2 friction fit)
        hole = translate([h['x'], h['y'], -1])(
            cylinder(d=SCREW_D_TAP, h=BOTTOM_FLOOR + PCB_STANDOFF_H + 2, _fn=16)
        )
        shell = shell + post - hole

    # Reset switch cutouts through the floor
    total_h = BOTTOM_FLOOR + BOTTOM_HEIGHT
    for rst in data.get('resets', []):
        shell -= translate([rst['x'] - 2, rst['y'] - 1.5, -1])(
            cube([4, 3, total_h + 2])
        )

    # USB-C cutouts through the walls
    BOTTOM_USB_W = 12.0     # cutout width
    BOTTOM_USB_H = 6.0      # cutout height (fits within wall above floor)
    z_center = BOTTOM_FLOOR + PCB_STANDOFF_H  # center at standoff height from top
    wall_depth = BOTTOM_WALL * 4  # enough to cut through wall
    for port in data.get('usbc', []):
        rot = port.get('rotation', 0)
        if rot == 0:
            # Top USB-C: cutout in x-z plane, extruded along y
            usb_cut = translate([port['x'], port['y'], z_center])(
                cube([BOTTOM_USB_W, wall_depth, BOTTOM_USB_H], center=True)
            )
        else:
            # Side USB-C: cutout in y-z plane, extruded along x
            usb_cut = translate([port['x'], port['y'], z_center])(
                cube([wall_depth, BOTTOM_USB_W, BOTTOM_USB_H], center=True)
            )
        shell -= usb_cut

    return shell


if __name__ == "__main__":
    os.makedirs("releases", exist_ok=True)

    for side in ['left', 'right']:
        print(f"Generating {side} half...")

        top = make_top_plate(side)
        top_path = f"releases/procyon_{side}_top.scad"
        top.save_as_scad(top_path)
        print(f"  -> {top_path}")

        bottom = make_bottom(side)
        bot_path = f"releases/procyon_{side}_bottom.scad"
        bottom.save_as_scad(bot_path)
        print(f"  -> {bot_path}")

    print("\nDone! Open .scad files in OpenSCAD to preview.")
    print("Parameters at the top of generate_case.py:")
    print(f"  PLATE_THICKNESS = {PLATE_THICKNESS}mm")
    print(f"  SWITCH_CUTOUT = {SWITCH_CUTOUT}mm")
    print(f"  BOTTOM_HEIGHT = {BOTTOM_HEIGHT}mm")
    print(f"  PCB_STANDOFF_H = {PCB_STANDOFF_H}mm")
