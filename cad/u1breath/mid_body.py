"""Section 2 (Z 110..195): blower cavity on the left, electronics bay on the
right with a removable front cover.  Open at the back (closed by the back plate).
"""
import cadquery as cq

from . import params as P
from .geom import box, cyl_y, cyl_x, union_all
from .filter_bay import attach_bosses, attach_holes


def cover_boss_points():
    i = P.COVER_BOSS_INSET
    return [(P.ELEC_X0 + i, P.ELEC_Z0 + i), (P.ELEC_X1 - i, P.ELEC_Z0 + i),
            (P.ELEC_X0 + i, P.ELEC_Z1 - i), (P.ELEC_X1 - i, P.ELEC_Z1 - i)]


def mid_body():
    y_back = P.BACK_PLATE_T
    body = box(0, P.UNIT_W, y_back, P.MID_Y1, P.MID_Z0, P.MID_Z1)
    # blower cavity (sealed, fed from the filter plenum through the floor)
    body = body.cut(box(P.WALL, P.PARTITION_X0, y_back - 1, P.ELEC_Y1, P.ELEC_Z0, P.ELEC_Z1))
    # electronics cavity, open at the front for the cover
    body = body.cut(box(P.ELEC_X0, P.ELEC_X1, y_back - 1, P.MID_Y1 + 1, P.ELEC_Z0, P.ELEC_Z1))
    # floor opening from the filter crossover duct
    body = body.cut(box(P.DUCT_X0, P.DUCT_X1, P.DUCT_Y0, P.DUCT_Y1, P.MID_Z0 - 1, P.MID_Z0 + P.WALL + 1))
    # roof opening for the blower outlet (into the heater shell)
    body = body.cut(box(P.BLOWER_OUTLET_X0, P.BLOWER_OUTLET_X0 + P.BLOWER_OUTLET_W,
                        P.BLOWER_OUTLET_Y0, P.BLOWER_OUTLET_Y0 + P.BLOWER_OUTLET_D,
                        P.MID_Z1 - P.WALL - 1, P.MID_Z1 + 1))
    # cover bosses in the four corners of the electronics cavity
    b = P.BOSS_SIZE
    for (x, z) in cover_boss_points():
        body = body.union(box(x - b / 2, x + b / 2, P.ELEC_Y1 - P.INSERT_DEPTH, P.ELEC_Y1 + 0.01, z - b / 2, z + b / 2))
        body = body.cut(cyl_y(x, z, P.ELEC_Y1 - P.INSERT_DEPTH, P.ELEC_Y1 + 1, P.INSERT_HOLE_D))
    # PG7 cord grip through the right wall, low
    body = body.cut(cyl_x(P.PG7_Y, P.PG7_Z, P.UNIT_W - P.WALL - 1, P.UNIT_W + 1, P.PG7_HOLE_D))
    # bosses to the back plate (full-depth columns on the side walls)
    body = body.union(attach_bosses("mid", y_back, P.ELEC_Y1 + 0.01))
    body = body.cut(attach_holes("mid", y_back))
    return body


def electronics_cover():
    c = P.SLIDE_CLEAR / 2.0
    cov = box(P.ELEC_X0 + c, P.ELEC_X1 - c, P.ELEC_Y1, P.MID_Y1, P.ELEC_Z0 + c, P.ELEC_Z1 - c)
    for (x, z) in cover_boss_points():
        cov = cov.cut(cyl_y(x, z, P.ELEC_Y1 - 1, P.MID_Y1 + 1, P.M3_CLEAR_D))
    # status LED window
    cov = cov.cut(box(P.LED_X0, P.LED_X0 + P.LED_WINDOW, P.ELEC_Y1 - 1, P.MID_Y1 + 1, P.LED_Z0, P.LED_Z0 + P.LED_WINDOW))
    # JST-XH 2-pin bed-probe connector slot, lower front
    cov = cov.cut(box(P.JST_X0, P.JST_X0 + P.JST_SLOT_W, P.ELEC_Y1 - 1, P.MID_Y1 + 1, P.JST_Z0, P.JST_Z0 + P.JST_SLOT_H))
    return cov


def blower_keepout():
    """7530 blower body plus its outlet stub, reference only."""
    body = box(P.BLOWER_X0, P.BLOWER_X0 + P.BLOWER_W, P.BACK_PLATE_T, P.BACK_PLATE_T + P.BLOWER_T,
               P.BLOWER_Z0, P.BLOWER_Z0 + P.BLOWER_H)
    outlet = box(P.BLOWER_OUTLET_X0, P.BLOWER_OUTLET_X0 + P.BLOWER_OUTLET_W,
                 P.BLOWER_OUTLET_Y0, P.BLOWER_OUTLET_Y0 + P.BLOWER_OUTLET_D,
                 P.BLOWER_Z0 + P.BLOWER_H - 0.01, P.MID_Z1 + 1.0)
    return body.union(outlet)


def electronics_keepouts():
    """Keep-out boxes of the electronics, standing on the back-plate standoffs."""
    y0 = P.BACK_PLATE_T + P.STANDOFF_H
    boxes = [box(x0, x0 + w, y0, y0 + d, z0, z0 + h) for (_n, x0, z0, w, h, d) in P.ELEC_KEEPOUTS]
    return union_all(boxes)
