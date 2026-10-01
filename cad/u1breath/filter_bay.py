"""Section 1, filter bay (Z 0..110): body, intake grille, carbon cartridge
(+ lid) and HEPA retainer frame.

Each bay, from the front going back (-Y): grille | carbon cartridge | two
80 x 40 x 15 HEPA cells (stacked in Z) | retainer frame | 12 mm plenum.
Both plenums share the cavity behind the bay tunnels and rise to the roof,
where a 85 x 30 mm opening (DUCT_*) feeds the blower cavity above.
"""
import cadquery as cq

from . import params as P
from .geom import box, cyl_y, union_all


def _bore(bx, y0, y1):
    c = P.SLIDE_CLEAR / 2.0
    return box(bx - c, bx + P.BAY_OPEN + c, y0, y1, P.BAY_Z0 - c, P.BAY_Z0 + P.BAY_OPEN + c)


def attach_bosses(section, y0, y1, z_size=P.BOSS_SIZE, x_size=P.BOSS_SIZE):
    """Boss blocks (with M3 insert holes along -Y, opened at the back face y0)
    that fix a section body to the back plate."""
    blocks = []
    for (x, z) in P.ATTACH_POINTS[section]:
        blocks.append(box(x - x_size / 2.0, x + x_size / 2.0, y0, y1, z - z_size / 2.0, z + z_size / 2.0))
    return union_all(blocks)


def attach_holes(section, y0):
    holes = [cyl_y(x, z, y0 - 1, y0 + P.INSERT_DEPTH, P.INSERT_HOLE_D) for (x, z) in P.ATTACH_POINTS[section]]
    return union_all(holes)


def filter_bay_body():
    y_back = P.BACK_PLATE_T
    body = box(0, P.UNIT_W, y_back, P.FILTER_Y1, P.FILTER_Z0, P.FILTER_Z1)
    # main cavity (plenum + tunnel region), open at the back toward the back plate
    body = body.cut(box(P.WALL, P.UNIT_W - P.WALL, y_back - 1, P.FILTER_FRONT_Y0,
                        P.FILTER_Z0 + P.WALL, P.FILTER_Z1 - P.WALL))
    # tunnel block that carries the two bay bores
    tb = box(max(0.0, P.BAY_X0 - P.WALL), min(P.UNIT_W, P.BAY_X[-1] + P.BAY_OPEN + P.WALL),
             P.FILTER_RETAINER_Y0, P.FILTER_FRONT_Y0 + 0.01,
             P.BAY_Z0 - P.WALL, P.BAY_Z0 + P.BAY_OPEN + P.WALL)
    body = body.union(tb)
    # retainer stop lip ring at the back of each bore (the retainer frame rests on it)
    lip = P.RETAINER_STOP_LIP
    for bx in P.BAY_X:
        ring = box(bx - lip, bx + P.BAY_OPEN + lip, P.FILTER_RETAINER_Y0 - 2.0, P.FILTER_RETAINER_Y0 + 0.01,
                   P.BAY_Z0 - lip, P.BAY_Z0 + P.BAY_OPEN + lip)
        ring = ring.cut(box(bx + lip, bx + P.BAY_OPEN - lip, 0, 100, P.BAY_Z0 + lip, P.BAY_Z0 + P.BAY_OPEN - lip))
        body = body.union(ring)
    # bores through the tunnel block and the front wall
    for bx in P.BAY_X:
        body = body.cut(_bore(bx, P.FILTER_RETAINER_Y0, P.FILTER_Y1 + 1))
        # grille snap recesses in the left/right bore walls
        zc = P.BAY_Z0 + P.BAY_OPEN / 2.0
        d = P.GRILLE_NUB + P.PRESS_CLEAR
        for (x0, x1) in ((bx - P.SLIDE_CLEAR / 2 - d, bx), (bx + P.BAY_OPEN, bx + P.BAY_OPEN + P.SLIDE_CLEAR / 2 + d)):
            body = body.cut(box(x0, x1, P.FILTER_GRILLE_Y0 - P.SLIDE_CLEAR, P.FILTER_GRILLE_Y0 + P.GRILLE_T + P.SLIDE_CLEAR,
                                zc - P.GRILLE_NUB_L / 2 - P.SLIDE_CLEAR, zc + P.GRILLE_NUB_L / 2 + P.SLIDE_CLEAR))
    # crossover duct opening in the roof, into the blower cavity of section 2
    body = body.cut(box(P.DUCT_X0, P.DUCT_X1, P.DUCT_Y0, P.DUCT_Y1, P.FILTER_Z1 - P.WALL - 1, P.FILTER_Z1 + 1))
    # bosses to the back plate: blocks in the strips below / above the tunnel block
    zs = 9.0  # strip height (Z 3..12 and 98..107)
    body = body.union(attach_bosses("filter", y_back, P.FILTER_FRONT_Y0 + 0.01, z_size=zs))
    body = body.cut(attach_holes("filter", y_back))
    return body


def intake_grille():
    """Snap-on slotted grille, sits in the bay bore at Y 48..51 (modelled in bay 0)."""
    bx = P.BAY_X[0]
    c = P.SLIDE_CLEAR / 2.0
    y0, y1 = P.FILTER_GRILLE_Y0, P.FILTER_GRILLE_Y0 + P.GRILLE_T
    g = box(bx + c, bx + P.BAY_OPEN - c, y0, y1, P.BAY_Z0 + c, P.BAY_Z0 + P.BAY_OPEN - c)
    # horizontal slots, 5 mm wide, 2 mm bars, 4 mm rim all round
    rim = 4.0
    pitch = P.GRILLE_SLOT_W + P.GRILLE_SLOT_BAR
    z = P.BAY_Z0 + rim
    slots = []
    while z + P.GRILLE_SLOT_W <= P.BAY_Z0 + P.BAY_OPEN - rim:
        slots.append(box(bx + rim, bx + P.BAY_OPEN - rim, y0 - 1, y1 + 1, z, z + P.GRILLE_SLOT_W))
        z += pitch
    g = g.cut(union_all(slots))
    # centre bar for stiffness
    g = g.union(box(bx + P.BAY_OPEN / 2 - 1.0, bx + P.BAY_OPEN / 2 + 1.0, y0, y1, P.BAY_Z0 + c, P.BAY_Z0 + P.BAY_OPEN - c))
    # snap nubs on the left/right edges
    zc = P.BAY_Z0 + P.BAY_OPEN / 2.0
    nub_l = box(bx + c - P.GRILLE_NUB, bx + c + 0.01, y0 + 0.5, y1 - 0.5, zc - P.GRILLE_NUB_L / 2, zc + P.GRILLE_NUB_L / 2)
    nub_r = box(bx + P.BAY_OPEN - c - 0.01, bx + P.BAY_OPEN - c + P.GRILLE_NUB, y0 + 0.5, y1 - 0.5, zc - P.GRILLE_NUB_L / 2, zc + P.GRILLE_NUB_L / 2)
    return g.union(nub_l).union(nub_r)


def _mesh_cut(x0, x1, z0, z1, y0, y1):
    """Grid of square openings (CARBON_MESH_PITCH) separated by CARBON_MESH_BAR."""
    o, b = P.CARBON_MESH_PITCH, P.CARBON_MESH_BAR
    pitch = o + b
    nx = int((x1 - x0 - b) // pitch)
    nz = int((z1 - z0 - b) // pitch)
    cx = (x0 + x1) / 2.0
    cz = (z0 + z1) / 2.0
    # workplane normal +Y so rect lies in XZ; cut a box of height y1-y0 starting at y0
    wp = cq.Workplane("XZ", origin=(cx, y0, cz)).rarray(pitch, pitch, nx, nz).rect(o, o).extrude(-(y1 - y0))
    return wp


def carbon_cartridge():
    """Tray part of the carbon cartridge: 79.5 x 79.5 x 13 (one mesh face), the
    lid makes up the remaining 2 mm.  Sits in the carbon slot of bay 0."""
    s = P.CARBON_BOX
    x0 = P.BAY_X[0] + (P.BAY_OPEN - s) / 2.0
    z0 = P.BAY_Z0 + (P.BAY_OPEN - s) / 2.0
    y0 = P.FILTER_CARBON_Y0
    y1 = y0 + P.CARBON_T - P.CARBON_LID_T    # lid goes in front (toward the grille)
    tray = box(x0, x0 + s, y0, y1, z0, z0 + s)
    w, t = P.CARBON_WALL, P.CARBON_MESH_T
    tray = tray.cut(box(x0 + w, x0 + s - w, y0 + t, y1 + 1, z0 + w, z0 + s - w))
    # M2 insert bosses in two opposite corners
    b = P.CARBON_BOSS
    for (bx, bz) in ((x0 + w, z0 + w), (x0 + s - w - b, z0 + s - w - b)):
        tray = tray.union(box(bx, bx + b, y0 + t - 0.01, y1, bz, bz + b))
        tray = tray.cut(cyl_y(bx + b / 2, bz + b / 2, y1 - P.INSERT_DEPTH, y1 + 1, P.M2_INSERT_HOLE_D))
    # mesh in the back face
    tray = tray.cut(_mesh_cut(x0 + w + 1, x0 + s - w - 1, z0 + w + 1, z0 + s - w - 1, y0 - 1, y0 + t + 1))
    return tray


def carbon_cartridge_lid():
    s = P.CARBON_BOX
    x0 = P.BAY_X[0] + (P.BAY_OPEN - s) / 2.0
    z0 = P.BAY_Z0 + (P.BAY_OPEN - s) / 2.0
    y1 = P.FILTER_CARBON_Y0 + P.CARBON_T
    y0 = y1 - P.CARBON_LID_T
    lid = box(x0, x0 + s, y0, y1, z0, z0 + s)
    w, b = P.CARBON_WALL, P.CARBON_BOSS
    for (bx, bz) in ((x0 + w, z0 + w), (x0 + s - w - b, z0 + s - w - b)):
        lid = lid.cut(cyl_y(bx + b / 2, bz + b / 2, y0 - 1, y1 + 1, P.M2_CLEAR_D))
    lid = lid.cut(_mesh_cut(x0 + w + 1, x0 + s - w - 1, z0 + w + 1, z0 + s - w - 1, y0 - 1, y1 + 1))
    return lid


def hepa_retainer():
    """Open frame behind the two HEPA cells: rim, centre bar between the cells,
    two vertical ribs.  Drops into the bore first and rests on the stop lip."""
    bx = P.BAY_X[0]
    c = P.SLIDE_CLEAR / 2.0
    y0, y1 = P.FILTER_RETAINER_Y0, P.FILTER_RETAINER_Y0 + P.HEPA_RETAINER_T
    x0, x1 = bx + c, bx + P.BAY_OPEN - c
    z0, z1 = P.BAY_Z0 + c, P.BAY_Z0 + P.BAY_OPEN - c
    f = box(x0, x1, y0, y1, z0, z1)
    rim = P.WALL
    f = f.cut(box(x0 + rim, x1 - rim, y0 - 1, y1 + 1, z0 + rim, z1 - rim))
    zm = P.BAY_Z0 + P.HEPA_H
    f = f.union(box(x0, x1, y0, y1, zm - rim / 2, zm + rim / 2))
    for xr in (bx + P.BAY_OPEN / 3.0, bx + 2 * P.BAY_OPEN / 3.0):
        f = f.union(box(xr - 1.0, xr + 1.0, y0, y1, z0, z1))
    return f
