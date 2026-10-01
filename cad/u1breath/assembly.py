"""Part registry, assembled positions and the exploded view."""
from . import params as P
from . import back_plate as BP
from . import filter_bay as FB
from . import mid_body as MB
from . import heater as H

# name -> (builder, printable, quantity, print orientation note)
# Every builder returns the part in its assembled position (bay 0 / instance 0).
PARTS = {
    "back_plate_lower": (BP.back_plate_lower, True, 1, "flat, back face (Y=0) down"),
    "back_plate_upper": (BP.back_plate_upper, True, 1, "flat, back face (Y=0) down"),
    "back_plate":       (BP.back_plate, False, 1, "reference only: one-piece plate, too tall for a 256 mm bed"),
    "filter_bay_body":  (FB.filter_bay_body, True, 1, "front face (Y=53) down, open back up"),
    "intake_grille":    (FB.intake_grille, True, 2, "flat, front face down"),
    "carbon_cartridge": (FB.carbon_cartridge, True, 2, "mesh face (back, Y=33) down"),
    "carbon_cartridge_lid": (FB.carbon_cartridge_lid, True, 2, "flat"),
    "hepa_retainer":    (FB.hepa_retainer, True, 2, "flat"),
    "mid_body":         (MB.mid_body, True, 1, "front face (Y=48) down, open back up"),
    "electronics_cover": (MB.electronics_cover, True, 1, "flat, front face down"),
    "heater_shell":     (H.heater_shell, True, 1, "front face (Y=52) down, open back up"),
    "heater_liner":     (H.heater_liner, False, 1, "aluminium, folded from the DXF flat pattern"),
    "blower_keepout":   (MB.blower_keepout, False, 1, "reference only"),
    "electronics_keepouts": (MB.electronics_keepouts, False, 1, "reference only"),
    "ptc_keepout":      (H.ptc_keepout, False, 1, "reference only"),
}

PRINTED = [n for n, (_f, printable, _q, _o) in PARTS.items() if printable and not n.startswith("back_plate")]
PLASTIC = PRINTED + ["back_plate_lower", "back_plate_upper"]

# X offset between the two bay instances
BAY_PITCH = P.BAY_OPEN + P.BAY_DIVIDER
PER_BAY = {"intake_grille", "carbon_cartridge", "carbon_cartridge_lid", "hepa_retainer"}

# Exploded-view translation (dx, dy, dz) per part
EXPLODE = {
    "back_plate_lower": (0, -40, 0),
    "back_plate_upper": (0, -40, 0),
    "filter_bay_body": (0, 0, 0),
    "hepa_retainer": (0, 40, 0),
    "carbon_cartridge": (0, 70, 0),
    "carbon_cartridge_lid": (0, 95, 0),
    "intake_grille": (0, 125, 0),
    "mid_body": (0, 0, 30),
    "electronics_cover": (0, 40, 30),
    "heater_shell": (0, 0, 60),
    "heater_liner": (0, 50, 60),
    "blower_keepout": (0, 0, 30),
    "electronics_keepouts": (0, 0, 30),
    "ptc_keepout": (0, 50, 60),
}


def build_all(names=None):
    """Build the registered parts; returns {name: Workplane}."""
    names = names or list(PARTS)
    return {n: PARTS[n][0]() for n in names}


def instances(name, part):
    """All assembled instances of a part (bay parts are duplicated for bay 1)."""
    if name in PER_BAY:
        return [part.translate((i * BAY_PITCH, 0, 0)) for i in range(P.BAYS)]
    return [part]


def assembled(parts, names=None):
    """List of positioned solids (Workplanes) of the assembly."""
    out = []
    for n, p in parts.items():
        if names is not None and n not in names:
            continue
        out += instances(n, p)
    return out


def exploded(parts, names=None):
    out = []
    for n, p in parts.items():
        if names is not None and n not in names:
            continue
        d = EXPLODE.get(n, (0, 0, 0))
        out += [i.translate(d) for i in instances(n, p)]
    return out
