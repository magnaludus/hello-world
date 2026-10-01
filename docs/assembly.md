# Assembly

Part names match `cad/build.py` output in `cad/out/stl/`. Print everything in ASA
(ABS is fine). Before printing, fill in `cad/u1breath/params.py` from
`measurements.md` and re-run `python cad/build.py`.

## Print settings

| Part | Qty | Orientation | Notes |
|---|---|---|---|
| back_plate_lower, back_plate_upper | 1 each | flat, back face down | 4 walls, 30 % infill; the two halves lap-joint at Z 140 to 150 because a 273 mm plate does not fit the 256 mm bed. `back_plate` (one piece) is exported for reference only |
| filter_bay_body | 1 | front face down | boss columns print as plain walls, no overhangs |
| intake_grille | 2 | flat | 0.2 mm layers, slots print without support |
| hepa_retainer | 2 | flat | goes into each bay first, rests on the stop lip at the back of the bore |
| carbon_cartridge | 2 | mesh face down | 2 mm openings, 1 mm bars; or print the frame and glue aluminum mesh |
| carbon_cartridge_lid | 2 | flat | |
| mid_body | 1 | front face down | blower and electronics bay; the PG7 hole is in the high-X side wall |
| electronics_cover | 1 | flat, outside face down | LED window: pause and insert a clear PETG square, or print the window in natural ASA |
| heater_shell | 1 | front face down | ASA only here, it sees the warmest air; side walls are 2 mm by design |
| heater_liner (STEP) and heater_liner_flat (DXF) | 1 | not printed | aluminum, see below; the slotted outlet plate is the second outline in the DXF |

Reference exports that are not printed: `blower_keepout`, `electronics_keepouts`, `ptc_keepout` (STEP/STL volumes used by the clearance tests).

Orientation note: with Y = 0 at the rear wall and Z up, +X runs to your left when you face the unit from inside the chamber. The blower sits at low X, the electronics bay at high X.

Heat-set inserts: M3 x 5.7 (OD 4.0) in every 4.0 mm boss hole; M2 in the cartridge
lids. Set them with a soldering iron at 230 C, press slowly, let the plastic flow.

## Aluminum liner

1. Print `cad/out/dxf/heater_liner_flat.dxf` at 1:1 on paper and spray-glue it to
   1.0 mm aluminum sheet, or send the DXF to a laser shop. The DXF holds two
   outlines: the folded box (layers OUTLINE, HOLES, BEND) and the flat slotted
   outlet plate that screws onto the box's 16 mm lips.
2. Cut the outline and the outlet slots (a nibbler or a Dremel cut-off wheel for the
   slots, file the burrs; any burr facing the airflow whistles).
3. Drill the thermal-fuse tab hole, the NTC ring-lug hole, and the PE bond hole (all
   M3 clearance, 3.2 mm).
4. Fold on the bend lines in a vise with two pieces of angle iron. The flange with
   the slots faces +Y (the chamber). Rivet or M3 the tabs.
5. Test fit the PTC element: it should slide in with the fins across the airflow and
   be held by its own mounting tabs or two M3 screws through the liner side walls
   into the element's frame holes (most 300 W elements have them). Never let the
   ceramic touch the liner directly; the element's own aluminum frame is the
   contact.

## Order of assembly

1. **Back plate** halves: join them at the lap (two M3 through the lap, nuts behind),
   then offer the assembled plate up to the printer, empty, to confirm the hole
   pattern and that the bed at Z max and the gantry clear it. Take it back off.
2. **Filter bay body** onto the back plate (6 x M3). Foam tape along the top edge of
   the bay where it meets the mid body.
3. **Mid body** onto the back plate. Mount the blower on its four M4 standoffs with
   the outlet pointing up through the slot into the heater plenum. Foam tape around
   the blower outlet flange.
4. **Electronics bay**: the standoff bosses are on the back plate, so fit the
   HLK-10M24, SSR carrier, MOSFET module, buck, fuse holder and terminal block to
   the plate before the mid body goes on, then close the mid body over them. Wire per `wiring.md` with the cover
   off. Route the three NTC leads: chamber NTC pokes into the filter plenum through
   the small hole at the bay floor; duct NTC and thermal fuse lead go up into the
   heater section through the grommet hole; the bed probe JST-XH sits in the slot on
   the lower front. Fit the PG7 grip in the side-wall hole and the cord last.
5. **Heater shell** over the liner: the blower discharges up through the mid-body
   roof into the shell cavity, which is the cold-side plenum around the liner; the
   liner takes air through the slot in its bottom wall. Screw the liner to the back
   plate through its slotted tabs (the slots allow thermal expansion), fit the shell
   over it with the 8 mm gap all round, then screw the slotted outlet plate through
   the liner lips into the four shell bosses. Strap the 130 C thermal fuse to the liner's top face with
   its tab and a dab of thermal paste, the duct NTC ring lug on the outer side face
   near the outlet end, the PE ring lug on the other side.
6. Plug the PTC into its two spade terminals, the blower into its JST-XH, the LED
   into its header. Fit the electronics cover.
7. Fill both carbon cartridges, screw the lids, slide them in, then the HEPA cells
   (two per bay, side by side), then the retainers, then snap the grilles on.
8. Antenna: stick the u.FL antenna on the inside of the electronics cover, as far
   from the liner and the back plate as it goes.

## Fitting to the U1

1. Route the cord up the rear wall, through the Sterilite cover grommet, out to the
   outlet. Leave a service loop inside so the cover can be lifted.
2. Run the bed probe lead from the unit's lower front along the rear wall and under
   the bed. Clip it to the existing bed cable route so bed travel cannot pinch it.
   Check it at Z max and Z min by hand before the first homing.
3. Mount the unit on its four fasteners, foam tape between the back plate and the
   wall. Confirm by hand that the toolhead dock, the cable chain, and the bed at
   every Z clear the unit by at least 10 mm.
4. Bring-up: `bringup.md`, in order. Do not skip the GFCI step.
