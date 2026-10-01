# Measurements only you can take

The CAD is parametric so that nothing here blocks the design, but each of these feeds a
value in `cad/u1breath/params.py` or `docs/bom.md`. Take them before printing.

| # | Measure | Feeds | Default assumed |
|---|---|---|---|
| 1 | Rear wall clear rectangle: width and height of flat wall below the toolhead dock and above the bed at max Z. Note wall material and thickness, and any existing holes or slots with their spacing. | `MOUNT_HOLES` list and `BACK_PLATE_*` in `params.py` | 273 x 175 mm free, slots on a 20 mm grid |
| 2 | Carbon pellet size (from the bag, or measure ten pellets). | `CARBON_MESH_PITCH` | 2 mm openings for 3 to 4 mm pellets |
| 3 | A bare aluminum spot on the underside of the bed plate for the probe, and a cable route to the rear wall that clears bed travel. | Bed probe lead length in the BOM | 600 mm silicone lead |
| 4 | The three outer dimensions of the 300 W PTC element you order (length, depth in the airflow direction, height). | `PTC_L`, `PTC_D`, `PTC_H` | 150 x 32 x 26 mm |
| 5 | Where on the Sterilite cover the cord grommet goes. | Cord length in the BOM | 1.8 m cord |

## How to measure the rear wall

1. Home the printer, then jog the bed to Z max and the gantry to Y max so you see the real
   envelope.
2. Measure from the bed plate top at Z max up to the lowest part of the toolhead dock or
   cable chain. That is the available height; subtract 10 mm for air.
3. Measure the flat width between the frame uprights or any ribs.
4. Photograph the wall and mark any pre-existing holes. If there are none, the back plate
   takes M3 or M4 through-holes with nuts behind the panel, or 3M VHB pads on a clean
   metal panel (the unit weighs under 900 g).

## Bed probe placement

The bed probe is a 100K 3950 NTC. A ring-lug style thermistor under an existing bed screw
is best; a glass bead held with Kapton and a dab of thermal epoxy on the aluminum plate is
fine. Keep it 20 mm or more from the silicone heater's wires and off the heater pad
itself, so it reads plate temperature, not heater wire temperature.
