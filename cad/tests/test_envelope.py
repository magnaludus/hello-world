"""Envelope, build-volume and heater-clearance checks for U1 Breath.

Run with:  python3 -m pytest cad/tests -q
"""
import os
import sys

import pytest
import cadquery as cq

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from u1breath import assembly as A      # noqa: E402
from u1breath import params as P        # noqa: E402
from u1breath import heater as H        # noqa: E402
from u1breath.geom import bbox, box     # noqa: E402


@pytest.fixture(scope="module")
def parts():
    return A.build_all()


def _bbox_of(solids):
    shapes = []
    for s in solids:
        shapes += s.vals()
    bb = cq.Compound.makeCompound(shapes).BoundingBox()
    return (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)


def test_every_part_is_one_solid(parts):
    for name, part in parts.items():
        if name == "electronics_keepouts":
            continue
        n = len(part.solids().vals())
        assert n == 1, f"{name} has {n} solids (floating geometry?)"
        assert part.val().Volume() > 0, name


def test_assembled_envelope(parts):
    """Assembled unit (all plastic parts + liner) within 273 (Z) x 175 (X) x 55 (Y)."""
    solids = A.assembled(parts, names=A.PLASTIC + ["heater_liner"])
    x0, x1, y0, y1, z0, z1 = _bbox_of(solids)
    tol = 0.05
    assert z1 - z0 <= P.ENVELOPE_MAX_H + tol, f"height {z1 - z0:.2f}"
    assert x1 - x0 <= P.ENVELOPE_MAX_W + tol, f"width {x1 - x0:.2f}"
    assert y1 - y0 <= P.ENVELOPE_MAX_D + tol, f"depth {y1 - y0:.2f}"
    assert y0 >= -tol, "nothing may stick out behind the back face (Y < 0)"


def test_total_depth_parameter():
    assert P.HEATER_DEPTH <= P.ENVELOPE_MAX_D
    assert P.FILTER_Y1 <= P.ENVELOPE_MAX_D
    assert P.MID_Y1 <= P.ENVELOPE_MAX_D


def test_each_printed_part_fits_build_volume(parts):
    for name in A.PLASTIC:
        x0, x1, y0, y1, z0, z1 = bbox(parts[name])
        dims = sorted((x1 - x0, y1 - y0, z1 - z0))
        assert dims[-1] <= P.BUILD_VOLUME + 0.05, f"{name} {dims} exceeds {P.BUILD_VOLUME} mm build volume"


def test_filter_depth_stack():
    assert P.FILTER_Y1 == P.BACK_PLATE_T + P.PLENUM_T + P.HEPA_RETAINER_T + P.HEPA_T + P.CARBON_T + P.WALL + P.FRONT_LIP


def test_plastic_keeps_hot_gap_from_liner(parts):
    """No plastic within HOT_GAP of the liner's inner volume inside the heater
    section: intersect each plastic solid with the inner box grown by HOT_GAP
    (clipped to the heater section) and demand zero volume."""
    g = P.HOT_GAP
    keepout = box(P.LINER_IN_X0 - g, P.LINER_IN_X1 + g, P.LINER_IN_Y0 - g, P.LINER_IN_Y1 + g,
                  P.LINER_IN_Z0 - g, P.LINER_IN_Z1 + g)
    keepout = keepout.intersect(box(-1, P.UNIT_W + 1, -1, P.ENVELOPE_MAX_D + 1, P.HEATER_Z0, P.HEATER_Z1))
    for name in A.PLASTIC:
        for inst in A.instances(name, parts[name]):
            x0, x1, y0, y1, z0, z1 = bbox(inst)
            if z1 < P.HEATER_Z0:          # entirely below the heater section
                continue
            hit = inst.intersect(keepout)
            vol = sum(s.Volume() for s in hit.solids().vals()) if hit.solids().vals() else 0.0
            assert vol < 1e-3, f"{name} intrudes {vol:.3f} mm^3 into the {g} mm hot gap around the liner"


def test_liner_matches_inner_box(parts):
    """The liner's inner volume (box used for the clearance test) is really
    empty: the liner solid must not intersect it."""
    inner = H.liner_inner_box()
    hit = parts["heater_liner"].intersect(inner)
    vol = sum(s.Volume() for s in hit.solids().vals()) if hit.solids().vals() else 0.0
    assert vol < 1e-3


def test_ptc_fits_in_liner():
    assert P.LINER_IN_X1 - P.LINER_IN_X0 >= P.PTC_L + 2 * P.PTC_CLEAR - 1e-9
    assert P.LINER_IN_Z1 - P.LINER_IN_Z0 >= P.PTC_H + 2 * P.PTC_CLEAR - 1e-9
    assert P.LINER_IN_Y1 - P.LINER_IN_Y0 >= P.PTC_D + P.HEATER_PLENUM_T - 1e-9


def test_keepouts_do_not_hit_bodies(parts):
    """Blower, PTC and electronics keep-outs stay clear of every printed part."""
    for ko in ("blower_keepout", "electronics_keepouts", "ptc_keepout"):
        for name in A.PLASTIC:
            for inst in A.instances(name, parts[name]):
                hit = inst.intersect(parts[ko])
                vol = sum(s.Volume() for s in hit.solids().vals()) if hit.solids().vals() else 0.0
                assert vol < 1e-3, f"{ko} collides with {name} ({vol:.2f} mm^3)"
