include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/version.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/constants.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/transforms.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/distributors.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/miscellaneous.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/color.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/attachments.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/beziers.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/shapes3d.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/shapes2d.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/drawing.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/masks3d.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/masks2d.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/math.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/paths.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/lists.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/comparisons.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/linalg.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/trigonometry.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/vectors.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/affine.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/coords.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/geometry.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/regions.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/strings.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/vnf.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/structs.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/rounding.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/skin.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/utility.scad>;
include </opt/homebrew/lib/python3.14/site-packages/solid2/extensions/bosl2/BOSL2/partitions.scad>;

difference() {
	union() {
		difference() {
			up(z = 6.0) {
				minkowski() {
					cube(center = true, size = [137.9, 109.3, 6.0]);
					cylinder($fn = 32, center = true, h = 6.0, r = 3.0);
				}
			}
			up(z = 7.5) {
				minkowski() {
					cube(center = true, size = [135.9, 107.3, 5.5]);
					cylinder($fn = 32, center = true, h = 5.5, r = 2.0);
				}
			}
		}
		translate(v = [-59.95, -45.65, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [60.05, -45.65, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [-59.95, 45.35, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [60.05, 45.35, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [0.04999999999999716, -0.6499999999999986, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
	}
	union() {
		translate(v = [-59.95, -45.65, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [60.05, -45.65, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [-59.95, 45.35, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [60.05, 45.35, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [0.04999999999999716, -0.6499999999999986, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
	}
}
