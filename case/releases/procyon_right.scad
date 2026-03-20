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
					cube(center = true, size = [158.9, 110.8, 6.0]);
					cylinder($fn = 32, center = true, h = 6.0, r = 3.0);
				}
			}
			up(z = 7.5) {
				minkowski() {
					cube(center = true, size = [156.9, 108.8, 5.5]);
					cylinder($fn = 32, center = true, h = 5.5, r = 2.0);
				}
			}
		}
		translate(v = [-70.45, -46.4, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [70.55, -46.4, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [-70.45, 46.6, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [70.55, 46.6, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
		translate(v = [-0.45000000000000284, -1.3999999999999986, 2.0]) {
			cylinder($fn = 24, d = 5.0, h = 3.0);
		}
	}
	union() {
		translate(v = [-70.45, -46.4, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [70.55, -46.4, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [-70.45, 46.6, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [70.55, 46.6, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
		translate(v = [-0.45000000000000284, -1.3999999999999986, 0]) {
			cylinder($fn = 16, d = 2.5, h = 6.0);
		}
	}
	translate(v = [-51.95, 0, 0]) {
		union() {
			translate(v = [0, 0, 11.0]) {
				cube(center = true, size = [58.0, 81.0, 4.0]);
			}
			difference() {
				translate(v = [0, 0, 9.06]) {
					cube(center = true, size = [61.0, 84.0, 1.9000000000000001]);
				}
				translate(v = [0, 0, 9.05]) {
					cube(center = true, size = [58.0, 81.0, 2.9000000000000004]);
				}
			}
		}
	}
}
