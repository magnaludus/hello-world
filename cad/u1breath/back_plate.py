"""Back plate: 3 mm plate on the printer's rear wall (Y 0..3).

Carries the rear-wall mounting pattern, the M3 clearance holes for the three
section bodies, the blower's M4 holes and the standoff bosses for the
electronics.  The full 273 mm plate does not fit the 256 mm build volume, so
`back_plate_lower()` and `back_plate_upper()` split it with a lap joint.
"""
import cadquery as cq

from . import params as P
from .geom import box, cyl_y, cone_y, union_all


def attach_points():
    """(x, z) centres of the M3 bosses that fix each section body to the plate."""
    return [pt for pts in P.ATTACH_POINTS.values() for pt in pts]


def blower_mount_points():
    s = P.BLOWER_MOUNT_SQ / 2.0
    return [(P.BLOWER_CX + dx, P.BLOWER_CZ + dz) for dx in (-s, s) for dz in (-s, s)]


def standoff_points():
    pts = []
    for (_n, x0, z0, w, h, _d) in P.ELEC_KEEPOUTS:
        i = P.STANDOFF_INSET
        pts += [(x0 + i, z0 + i), (x0 + w - i, z0 + i), (x0 + i, z0 + h - i), (x0 + w - i, z0 + h - i)]
    return pts


def _plate_features(plate, z0=0.0, z1=P.BACK_PLATE_H):
    t = P.BACK_PLATE_T
    inside = lambda z: z0 + P.STANDOFF_D / 2.0 <= z <= z1 - P.STANDOFF_D / 2.0
    standoffs = [(x, z) for (x, z) in standoff_points() if inside(z)]
    # rear-wall mounting grid (4.5 mm) and countersunk M4 holes
    for (x, z) in P.MOUNT_HOLES:
        plate = plate.cut(cyl_y(x, z, -1, t + 1, P.M4_CLEAR_D))
    for (x, z) in P.MOUNT_CSK_HOLES:
        plate = plate.cut(cyl_y(x, z, -1, t + 1, P.M4_CLEAR_D))
        plate = plate.cut(cone_y(x, z, -0.01, (P.M4_CSK_D - P.M4_CLEAR_D) / 2.0, P.M4_CSK_D, P.M4_CLEAR_D))
    # section bodies: M3 clearance, screwed from behind into bosses on the bodies
    for (x, z) in attach_points():
        plate = plate.cut(cyl_y(x, z, -1, t + 1, P.M3_CLEAR_D))
    # blower M4 holes, screwed from behind into the blower frame
    for (x, z) in blower_mount_points():
        plate = plate.cut(cyl_y(x, z, -1, t + 1, P.BLOWER_MOUNT_D))
    # electronics standoff bosses on the front face
    bosses = [cyl_y(x, z, t - 0.01, t + P.STANDOFF_H, P.STANDOFF_D) for (x, z) in standoffs]
    if bosses:
        plate = plate.union(union_all(bosses))
    for (x, z) in standoffs:
        plate = plate.cut(cyl_y(x, z, t - 2.0, t + P.STANDOFF_H + 1, P.STANDOFF_HOLE_D))
    return plate


def back_plate():
    """The full one-piece back plate (reference; too tall for a 256 mm bed)."""
    plate = box(0, P.BACK_PLATE_W, 0, P.BACK_PLATE_T, 0, P.BACK_PLATE_H)
    return _plate_features(plate)


def _lap_cut_lower():
    """Material removed from the lower half: front half-thickness above the split."""
    zs = P.BACK_PLATE_SPLIT_Z
    return box(-1, P.BACK_PLATE_W + 1, P.BACK_PLATE_T / 2.0, P.BACK_PLATE_T + 10,
               zs, zs + P.BACK_PLATE_LAP + 1)


def _lap_cut_upper():
    zs = P.BACK_PLATE_SPLIT_Z
    return box(-1, P.BACK_PLATE_W + 1, -10, P.BACK_PLATE_T / 2.0,
               zs - 1, zs + P.BACK_PLATE_LAP)


def back_plate_lower():
    """Lower half, Z 0..SPLIT+LAP, with the rear half of the lap joint."""
    zs = P.BACK_PLATE_SPLIT_Z
    plate = box(0, P.BACK_PLATE_W, 0, P.BACK_PLATE_T, 0, zs + P.BACK_PLATE_LAP)
    plate = plate.cut(_lap_cut_lower())
    return _plate_features(plate, 0.0, zs)


def back_plate_upper():
    """Upper half, Z SPLIT..273, with the front half of the lap joint."""
    zs = P.BACK_PLATE_SPLIT_Z
    plate = box(0, P.BACK_PLATE_W, 0, P.BACK_PLATE_T, zs, P.BACK_PLATE_H)
    plate = plate.cut(_lap_cut_upper())
    return _plate_features(plate, zs, P.BACK_PLATE_H)
