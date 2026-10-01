#!/usr/bin/env python3
"""Export every U1 Breath part.

    python3 cad/build.py            # everything
    python3 cad/build.py mid_body   # one or more parts (STL + STEP only)

Outputs under cad/out/: stl/<part>.stl, step/<part>.step,
dxf/heater_liner_flat.dxf, layout.svg (front + side views) and exploded.svg.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cadquery as cq
from cadquery import exporters

from u1breath import assembly as A
from u1breath import heater as H
from u1breath import params as P
from u1breath.geom import bbox

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def _compound(solids):
    shapes = []
    for s in solids:
        shapes += s.vals()
    return cq.Workplane("XY").add(cq.Compound.makeCompound(shapes))


def export_svg(solids, path, direction, width=1200, height=800):
    exporters.export(
        _compound(solids), path, exportType="SVG",
        opt={"width": width, "height": height, "marginLeft": 20, "marginTop": 20,
             "showAxes": False, "projectionDir": direction, "strokeWidth": 0.4,
             "strokeColor": (30, 30, 30), "hiddenColor": (180, 180, 180), "showHidden": False},
    )


def main(argv):
    names = argv or list(A.PARTS)
    for d in ("stl", "step", "dxf"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    t0 = time.time()
    parts = A.build_all(names)
    rows = []
    for name, part in parts.items():
        exporters.export(part, os.path.join(OUT, "stl", name + ".stl"), tolerance=0.05, angularTolerance=0.1)
        exporters.export(part, os.path.join(OUT, "step", name + ".step"))
        bb = bbox(part)
        rows.append((name, bb))
        print(f"{name:24s} X {bb[0]:7.2f}..{bb[1]:7.2f}  Y {bb[2]:6.2f}..{bb[3]:6.2f}  Z {bb[4]:7.2f}..{bb[5]:7.2f}"
              f"   ({bb[1]-bb[0]:.1f} x {bb[3]-bb[2]:.1f} x {bb[5]-bb[4]:.1f})")

    if not argv:
        dxf_path = os.path.join(OUT, "dxf", "heater_liner_flat.dxf")
        H.export_liner_dxf(dxf_path)
        print("wrote", dxf_path)
        # Drawings.  The SVG exporter picks its own "up" vector, so the model is
        # first turned so that model Z becomes drawing Y and the front (+Y)
        # faces the viewer (-Z); the views are then projected along Z.
        def to_drawing(solids):
            return [s.rotate((0, 0, 0), (1, 0, 0), -90) for s in solids]

        front = to_drawing(A.assembled(parts))
        side = [s.rotate((0, 0, 0), (0, 1, 0), 90).translate((-(P.UNIT_W + 60), 0, 0)) for s in front]
        export_svg(front + side, os.path.join(OUT, "layout.svg"), (0, 0, -1))
        print("wrote", os.path.join(OUT, "layout.svg"))
        export_svg(to_drawing(A.exploded(parts)), os.path.join(OUT, "exploded.svg"), (-1, 0.8, -1.2))
        print("wrote", os.path.join(OUT, "exploded.svg"))
    print(f"done in {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main(sys.argv[1:])
