"""Section 3 (Z 195..273): ASA heater shell, folded aluminium liner (STEP
reference) and the liner flat pattern (DXF).

The liner is a five-sided folded box (back wall + top/bottom/left/right walls)
whose top and bottom walls end in outward 16 mm lips; a separate flat, slotted
front plate (172 x 78) closes the box and forms the front face of the unit.
Four M3 screws pass through plate + lips into bosses on the shell.  The shell
cavity around the liner is the cold-side plenum: the blower discharges through
the shell floor, air fills the 8 mm jacket around the liner and enters the
liner plenum through a slot in its bottom wall, passes the PTC fins toward +Y
and leaves through the slotted plate.
"""
import cadquery as cq
from cadquery import Vector

from . import params as P
from .geom import box, cyl_y, cyl_x, cyl_z, union_all
from .filter_bay import attach_bosses, attach_holes


# --- liner box extents in the assembled frame --------------------------------
LX0, LX1 = P.LINER_IN_X0 - P.LINER_T, P.LINER_IN_X1 + P.LINER_T   # outer X 9..163
LY0, LY1 = P.LINER_IN_Y0 - P.LINER_T, P.LINER_IN_Y1               # outer Y 11..52 (front open)
LZ0, LZ1 = P.LINER_IN_Z0 - P.LINER_T, P.LINER_IN_Z1 + P.LINER_T   # outer Z 215..245


def liner_screw_points():
    return [(x, z) for z in P.LINER_SCREW_Z for x in P.LINER_SCREW_X]


def liner_inner_box():
    """The liner's inner (hot) volume as a solid, used by the clearance test."""
    return box(P.LINER_IN_X0, P.LINER_IN_X1, P.LINER_IN_Y0, P.LINER_IN_Y1, P.LINER_IN_Z0, P.LINER_IN_Z1)


def heater_shell():
    y_back = P.BACK_PLATE_T
    sw = P.HEATER_SIDE_WALL
    shell = box(0, P.UNIT_W, y_back, P.SHELL_FRONT_Y1, P.HEATER_Z0, P.HEATER_Z1)
    # cavity, open at the back
    shell = shell.cut(box(sw, P.UNIT_W - sw, y_back - 1, P.SHELL_FRONT_Y0, P.HEATER_Z0 + P.WALL, P.HEATER_Z1 - P.WALL))
    # front window: inner volume grown by HOT_GAP, through the front frame
    g = P.HOT_GAP
    shell = shell.cut(box(P.LINER_IN_X0 - g, P.LINER_IN_X1 + g, P.SHELL_FRONT_Y0 - 1, P.SHELL_FRONT_Y1 + 1,
                          P.LINER_IN_Z0 - g, P.LINER_IN_Z1 + g))
    # floor opening above the blower outlet
    shell = shell.cut(box(P.BLOWER_OUTLET_X0, P.BLOWER_OUTLET_X0 + P.BLOWER_OUTLET_W,
                          P.BLOWER_OUTLET_Y0, P.BLOWER_OUTLET_Y0 + P.BLOWER_OUTLET_D,
                          P.HEATER_Z0 - 1, P.HEATER_Z0 + P.WALL + 1))
    # bosses behind the front frame for the liner plate / lip screws
    b = P.BOSS_SIZE
    for (x, z) in liner_screw_points():
        shell = shell.union(box(x - b / 2, x + b / 2, P.SHELL_FRONT_Y0 - P.INSERT_DEPTH, P.SHELL_FRONT_Y0 + 0.01, z - b / 2, z + b / 2))
        shell = shell.cut(cyl_y(x, z, P.SHELL_FRONT_Y0 - P.INSERT_DEPTH, P.SHELL_FRONT_Y1 + 1, P.INSERT_HOLE_D))
    # bosses to the back plate (full-depth columns on the thin side walls)
    shell = shell.union(attach_bosses("heater", y_back, P.SHELL_FRONT_Y0 + 0.01))
    shell = shell.cut(attach_holes("heater", y_back))
    return shell


def heater_liner():
    """Folded liner box + lips + slotted front plate, as one reference solid."""
    t = P.LINER_T
    outer = box(LX0, LX1, LY0, LY1, LZ0, LZ1)
    inner = box(LX0 + t, LX1 - t, LY0 + t, LY1 + 1, LZ0 + t, LZ1 - t)
    liner = outer.cut(inner)
    # inlet slot in the bottom wall over the plenum
    liner = liner.cut(box(P.LINER_INLET_X0, P.LINER_INLET_X1, P.LINER_IN_Y0, P.LINER_IN_Y0 + P.HEATER_PLENUM_T,
                          LZ0 - 1, LZ0 + t + 1))
    # outward lips on the top and bottom walls (Y 52..53)
    lip_y0, lip_y1 = LY1, LY1 + t
    liner = liner.union(box(LX0, LX1, lip_y0, lip_y1, LZ1 - t, LZ1 + P.LINER_LIP))
    liner = liner.union(box(LX0, LX1, lip_y0, lip_y1, LZ0 - P.LINER_LIP, LZ0 + t))
    # thermal protector hole (top), NTC hole (right side), lead grommet (left side)
    liner = liner.cut(cyl_z(P.PROTECTOR_HOLE[0], P.PROTECTOR_HOLE[1], LZ1 - t - 1, LZ1 + 1, P.M3_CLEAR_D))
    liner = liner.cut(cyl_x(P.NTC_HOLE_Y, (LZ0 + LZ1) / 2, LX1 - t - 1, LX1 + 1, P.M3_CLEAR_D))
    liner = liner.cut(cyl_x(P.PTC_LEAD_HOLE_Y, (LZ0 + LZ1) / 2, LX0 - 1, LX0 + t + 1, P.PTC_LEAD_HOLE_D))
    # slotted front plate
    plate = heater_liner_plate()
    liner = liner.union(plate)
    # screw holes through lips + plate
    for (x, z) in liner_screw_points():
        liner = liner.cut(cyl_y(x, z, lip_y0 - 1, P.HEATER_Y1 + 1, P.LINER_SCREW_D))
    return liner


def _slot_rows():
    z = P.LINER_IN_Z0 + 3.5
    rows = []
    while z + P.LINER_SLOT_W <= P.LINER_IN_Z1 - 3.0:
        rows.append(z)
        z += P.LINER_SLOT_PITCH
    return rows


def heater_liner_plate():
    y0 = LY1 + P.LINER_T
    y1 = y0 + P.LINER_PLATE_T
    plate = box(0, P.UNIT_W, y0, y1, P.HEATER_Z0, P.HEATER_Z1)
    slots = [box(P.LINER_SLOT_X0, P.LINER_SLOT_X1, y0 - 1, y1 + 1, z, z + P.LINER_SLOT_W) for z in _slot_rows()]
    plate = plate.cut(union_all(slots))
    return plate


def ptc_keepout():
    return box(P.LINER_IN_X0 + P.PTC_CLEAR, P.LINER_IN_X1 - P.PTC_CLEAR,
               P.LINER_IN_Y0 + P.HEATER_PLENUM_T, P.LINER_IN_Y1,
               P.LINER_IN_Z0 + P.PTC_CLEAR, P.LINER_IN_Z1 - P.PTC_CLEAR)


# --- flat pattern ---------------------------------------------------------------
def liner_flat_pattern():
    """Returns dict of layer name -> list of cq.Wire / cq.Edge in the XY plane
    (sheet coordinates in mm): OUTLINE, HOLES, BEND for the box and the plate.

    Cross layout: back wall at the centre, top wall up (+v), bottom wall down,
    side walls left/right, lips beyond the top/bottom walls, 10 mm tabs on the
    side walls.  Plain outline, no bend allowance (1 mm sheet, fold by hand).
    """
    t = P.LINER_T
    W = LX1 - LX0               # 154, back wall width (u)
    H = LZ1 - LZ0               # 30, back wall height (v)
    D = LY1 - LY0               # 41, wall depth
    lip, tab = P.LINER_LIP, P.LINER_TAB
    hu, hv = W / 2.0, H / 2.0
    # outline polygon (counter-clockwise), starting at bottom-left of the back wall
    pts = [
        # bottom wall + lip
        (-hu, -hv), (-hu, -hv - D), (-hu, -hv - D - lip), (hu, -hv - D - lip), (hu, -hv - D), (hu, -hv),
        # right wall with tabs
        (hu + 1.0, -hv), (hu + 1.0, -hv - tab), (hu + D, -hv - tab), (hu + D, hv + tab), (hu + 1.0, hv + tab), (hu + 1.0, hv),
        # top wall + lip
        (hu, hv), (hu, hv + D), (hu, hv + D + lip), (-hu, hv + D + lip), (-hu, hv + D), (-hu, hv),
        # left wall with tabs
        (-hu - 1.0, hv), (-hu - 1.0, hv + tab), (-hu - D, hv + tab), (-hu - D, -hv - tab), (-hu - 1.0, -hv - tab), (-hu - 1.0, -hv),
    ]
    outline = cq.Workplane("XY").polyline(pts).close()
    layers = {"OUTLINE": [], "HOLES": [], "BEND": []}
    layers["OUTLINE"].append(outline.val())

    def circle(u, v, d):
        return cq.Workplane("XY").center(u, v).circle(d / 2.0).val()

    def rect(u0, u1, v0, v1):
        return cq.Workplane("XY").polyline([(u0, v0), (u1, v0), (u1, v1), (u0, v1)]).close().val()

    xc = (LX0 + LX1) / 2.0
    # inlet slot in the bottom wall: Y 12..20 -> v = -hv - (Y - LY0)
    layers["HOLES"].append(rect(P.LINER_INLET_X0 - xc, P.LINER_INLET_X1 - xc,
                                -hv - (P.LINER_IN_Y0 + P.HEATER_PLENUM_T - LY0), -hv - (P.LINER_IN_Y0 - LY0)))
    # thermal protector hole in the top wall
    layers["HOLES"].append(circle(P.PROTECTOR_HOLE[0] - xc, hv + (P.PROTECTOR_HOLE[1] - LY0), P.M3_CLEAR_D))
    # NTC ring-lug hole, right wall;  lead grommet hole, left wall
    layers["HOLES"].append(circle(hu + (P.NTC_HOLE_Y - LY0), 0.0, P.M3_CLEAR_D))
    layers["HOLES"].append(circle(-hu - (P.PTC_LEAD_HOLE_Y - LY0), 0.0, P.PTC_LEAD_HOLE_D))
    # screw holes in the lips
    for x in P.LINER_SCREW_X:
        layers["HOLES"].append(circle(x - xc, hv + D + (P.LINER_SCREW_Z[1] - LZ1), P.LINER_SCREW_D))
        layers["HOLES"].append(circle(x - xc, -hv - D - (LZ0 - P.LINER_SCREW_Z[0]), P.LINER_SCREW_D))
    # bend lines
    def line(a, b):
        return cq.Edge.makeLine(Vector(a[0], a[1], 0), Vector(b[0], b[1], 0))
    for (a, b) in (((-hu, hv), (hu, hv)), ((-hu, -hv), (hu, -hv)), ((hu, -hv), (hu, hv)), ((-hu, -hv), (-hu, hv)),
                   ((-hu, hv + D), (hu, hv + D)), ((-hu, -hv - D), (hu, -hv - D)),
                   ((hu + 1.0, -hv), (hu + D, -hv)), ((hu + 1.0, hv), (hu + D, hv)),
                   ((-hu - 1.0, -hv), (-hu - D, -hv)), ((-hu - 1.0, hv), (-hu - D, hv))):
        layers["BEND"].append(line(a, b))

    # slotted front plate, placed to the right of the box pattern
    pu = hu + D + tab + 20.0          # left edge of the plate in sheet coords
    pv = -(P.HEATER_Z1 - P.HEATER_Z0) / 2.0
    layers["OUTLINE"].append(rect(pu, pu + P.UNIT_W, pv, pv + (P.HEATER_Z1 - P.HEATER_Z0)))
    for z in _slot_rows():
        layers["HOLES"].append(rect(pu + P.LINER_SLOT_X0, pu + P.LINER_SLOT_X1,
                                    pv + (z - P.HEATER_Z0), pv + (z - P.HEATER_Z0) + P.LINER_SLOT_W))
    for (x, z) in liner_screw_points():
        layers["HOLES"].append(circle(pu + x, pv + (z - P.HEATER_Z0), P.LINER_SCREW_D))
    return layers


def export_liner_dxf(path):
    from cadquery.occ_impl.exporters.dxf import DxfDocument
    layers = liner_flat_pattern()
    doc = DxfDocument()
    doc.add_layer("OUTLINE", color=7)
    doc.add_layer("HOLES", color=1)
    doc.add_layer("BEND", color=5, linetype="DASHED")
    for name, shapes in layers.items():
        for s in shapes:
            doc.add_shape(cq.Workplane("XY").add(s), name)
    doc.document.saveas(path)
