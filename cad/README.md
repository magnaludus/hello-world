# U1 Breath CAD

Parametric CadQuery model of the U1 Breath chamber heater + HEPA/carbon filter
unit for the Snapmaker U1.  Overall 172 (X) x 54 (Y) x 273 (Z) mm, three stacked
sections serviced from the front, all plastic parts in ASA with M3 heat-set
inserts, only the heater duct liner in 1 mm aluminium.

## Run

```sh
pip install cadquery pytest          # CadQuery 2.8 or newer
python3 cad/build.py                 # everything, about a minute
python3 cad/build.py mid_body        # one part (STL + STEP only)
python3 -m pytest cad/tests -q       # envelope, build-volume and hot-gap checks
```

Outputs land in `cad/out/` (git-ignored):

| Path | Content |
|---|---|
| `out/stl/<part>.stl`, `out/step/<part>.step` | every part, in its assembled position (bay 0 for the per-bay parts) |
| `out/dxf/heater_liner_flat.dxf` | liner flat pattern, layers `OUTLINE`, `HOLES`, `BEND` |
| `out/layout.svg` | front and side views of the assembly |
| `out/exploded.svg` | exploded isometric view |

Every dimension is a named constant in `cad/u1breath/params.py`; change it there
and rebuild.  Fill in the values from `docs/measurements.md` first (`MOUNT_HOLES`,
`PTC_L/D/H`, `CARBON_MESH_PITCH`).

## Coordinate frame

`Y = 0` is the back face on the printer's rear wall, `+Y` toward the chamber,
`Z = 0` the bottom, air flows up.  The frame is right-handed, so `+X` runs to your
left when you face the unit from inside the chamber (and to the right when the
unit lies on its back, as the parts are printed).  Low X holds the blower, high X
the electronics bay.

## Parts

| Part | Qty | What it is | Print orientation |
|---|---|---|---|
| `back_plate_lower`, `back_plate_upper` | 1 + 1 | 3 mm plate on the rear wall, split at Z 140 with a 10 mm half-thickness lap joint (the full 273 mm plate does not fit the 256 mm bed). Carries the 20 mm mounting grid (4.5 mm, X 10 / 162), six countersunk M4 holes, the M3 clearance holes for the three bodies, the blower's 4 x M4 holes and the standoff bosses for the electronics. | flat, back face (Y = 0) down; the bosses point up |
| `back_plate` | ref. | the same plate in one piece, for printers with a taller bed | flat |
| `filter_bay_body` | 1 | Z 0..110. Two 80 x 80 bay tunnels; from the front: grille, carbon cartridge slot (15), HEPA slot (2 cells 80 x 40 x 15 stacked), retainer frame (3), 12 mm plenum. The plenum fills the whole cavity behind the tunnels and leaves through the 85 x 30 mm roof opening into the blower cavity. | front face (Y = 53) down, open back up; the boss blocks print as columns |
| `intake_grille` | 2 | 3 mm slotted grille (5 mm slots, 2 mm bars), snaps into the bore with two 1 mm nubs; sits 2 mm behind the front face | flat, front down |
| `carbon_cartridge` | 2 | 79.5 x 79.5 x 13 tray with a 2 mm square-mesh back face and two M2 insert bosses; fill with pellet carbon | mesh face down |
| `carbon_cartridge_lid` | 2 | 79.5 x 79.5 x 2 mesh lid, 2 x M2 button screws | flat |
| `hepa_retainer` | 2 | 3 mm open frame with a centre bar between the two cells; goes in first and rests on a 1.5 mm lip at the back of the bore, the HEPA cells drop in after it | flat |
| `mid_body` | 1 | Z 110..195. Sealed blower cavity (low X, fed through the floor opening from the filter plenum; the 7530 lies flat, inlet toward +Y, outlet through the roof opening into the heater shell) and the electronics bay (high X) with four M3 cover bosses and the 12.5 mm PG7 cord-grip hole in the side wall | front face (Y = 48) down, open back up |
| `electronics_cover` | 1 | 3 mm cover with the 10 x 10 LED window and the 8 x 6 JST-XH bed-probe slot; 4 x M3 button screws | flat, front down |
| `heater_shell` | 1 | Z 195..273. ASA box around the liner keeping an 8 mm air gap on every side (2 mm side walls, see below), floor opening above the blower outlet, four bosses behind the front frame for the liner screws | front face (Y = 52) down, open back up |
| `heater_liner` | ref. | folded 1 mm aluminium box (back, top, bottom, two sides; outward 16 mm lips on top and bottom; 10 mm corner tabs) plus the flat slotted front plate 172 x 78 (four rows of 3 x 132 mm slots). Cut both from the DXF. Holes: inlet slot in the bottom wall over the plenum, M3 for the bimetal thermal protector on the top face, M3 for the ring-lug NTC on the high-X side face, 8 mm lead grommet on the low-X side face, four M3 screw holes in the lips and the plate. | not printed |
| `blower_keepout`, `electronics_keepouts`, `ptc_keepout` | ref. | keep-out boxes used by the collision tests | not printed |

Screws: all section bodies screw from behind the back plate into M3 inserts in
the bodies (four per section); the electronics cover and the liner plate screw
from the front.  Inserts: M3 x 5.7 (4.0 mm hole, 6 mm bosses), M2 for the
cartridge lids.  Clearances: 0.3 mm on sliding fits (filters, cartridge,
cover), 0.15 mm on the grille snap nubs.

## Airflow

Grille -> carbon cartridge -> two HEPA cells -> retainer frame -> 12 mm plenum ->
up through the roof opening of the filter bay into the blower cavity -> blower
inlet (+Y face) -> outlet through the mid-body roof and heater-shell floor into
the cold jacket around the liner -> slot in the liner's bottom wall into the 8 mm
plenum behind the PTC -> through the fins toward +Y -> out through the slotted
front plate.  The jacket air keeps the shell cool; the liner never touches plastic.

## Depth budget (Y)

| Section | Stack | Total |
|---|---|---|
| filter bay | 3 plate + 12 plenum + 3 retainer + 15 HEPA + 15 carbon + 3 wall + 2 lip | 53 |
| mid | 3 plate + 30 blower + 12 inlet plenum + 3 wall | 48 |
| heater | 3 plate + 8 gap + 1 liner + 8 plenum + 32 PTC + 1 lips + 1 slotted plate | 54 |

`HEATER_DEPTH` (54) is asserted <= 55 by the tests.

## Tests (`cad/tests/test_envelope.py`)

- every part is a single solid
- the assembled unit is within 273 x 175 x 55 mm (H x W x D) and nothing is behind Y = 0
- every printed part fits a 256 mm cube
- no plastic part intrudes into the liner's inner volume grown by `HOT_GAP` (8 mm) within the heater section
- the PTC, blower and electronics keep-outs collide with nothing

## Design notes / deviations from the brief

- The heater shell's side walls are 2 mm (not 3): 150 mm element + 2 x 1 mm clearance + 2 x 8 mm gap + 2 x 2 mm wall is exactly 172 mm.
- The liner has no printed duct from the blower: the whole shell cavity is the cold-side plenum and the liner takes air through a slot in its bottom wall.  A printed duct would have to touch the liner.
- The slotted outlet is a separate flat plate (second outline in the DXF), screwed through the liner's top/bottom lips into the shell; it adds 1 mm of depth (54 total).  Outlet slots are straight, not angled.
- The HEPA retainer frame adds 3 mm to the filter bay depth (53 instead of 50) because it cannot live inside the 15 mm HEPA slot while the cells fill the full 80 x 80 bore.
- The back plate is printed in two halves with a lap joint.
- The electronics standoff bosses are on the back plate (prints flat), not inside the mid body, so the mid body prints front-face-down without supports.
- The bosses that hold the bodies to the back plate are full-depth columns on the walls (filter bay: blocks in the strips above and below the bay tunnels) so that they print without overhangs; their positions avoid the 20 mm mounting grid.
- `outlet_shroud` was skipped (any trim in front of the plate would exceed the 55 mm depth).
