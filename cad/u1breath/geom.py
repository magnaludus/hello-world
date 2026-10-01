"""Small geometry helpers shared by every part module."""
import cadquery as cq
from cadquery import Vector


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min/max corners, as a Workplane solid."""
    return (
        cq.Workplane("XY")
        .box(x1 - x0, y1 - y0, z1 - z0, centered=False)
        .translate((x0, y0, z0))
    )


def cyl_y(xc, zc, y0, y1, d):
    """Cylinder along +Y (hole axis Y), from y0 to y1."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(d / 2.0, y1 - y0, Vector(xc, y0, zc), Vector(0, 1, 0))
    )


def cyl_x(yc, zc, x0, x1, d):
    """Cylinder along +X."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(d / 2.0, x1 - x0, Vector(x0, yc, zc), Vector(1, 0, 0))
    )


def cyl_z(xc, yc, z0, z1, d):
    """Cylinder along +Z."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCylinder(d / 2.0, z1 - z0, Vector(xc, yc, z0), Vector(0, 0, 1))
    )


def cone_y(xc, zc, y0, y1, d0, d1):
    """Cone along +Y, diameter d0 at y0 and d1 at y1 (countersinks)."""
    return cq.Workplane("XY").add(
        cq.Solid.makeCone(d0 / 2.0, d1 / 2.0, y1 - y0, Vector(xc, y0, zc), Vector(0, 1, 0))
    )


def union_all(parts):
    """Union a list of Workplanes into one."""
    result = parts[0]
    for p in parts[1:]:
        result = result.union(p)
    return result


def bbox(wp):
    """(xmin, xmax, ymin, ymax, zmin, zmax) of a Workplane's solids."""
    bb = cq.Compound.makeCompound(wp.vals()).BoundingBox() if len(wp.vals()) > 1 else wp.val().BoundingBox()
    return (bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax)
