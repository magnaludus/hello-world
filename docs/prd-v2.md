# U1 Breath v2: product requirements

Status: reviewed draft for the Fusion rebuild. Owner: magnaludus. Branch: `u1breath-design`.

## 1. Summary

U1 Breath is a 300 W chamber heater plus HEPA and activated-carbon filter. It mounts on the rear wall inside a
Snapmaker U1's enclosure. v2 rebuilds the mechanical design natively in Autodesk Fusion. It keeps the same parts
list, electronics and firmware. It fixes every defect found in the v1 audit, and it serves four owner priorities:
easier to build, better heating, safer electrics, and filter drawers.

The v2 model is built in a local Claude Desktop Code session using the owner's Fusion connector. This document is
that session's brief. Sections 4 to 10 are requirements. Section 11 is a recommended architecture whose numbers
already add up, so start from it unless a requirement forces a change.

Each requirement carries a verification tag:

- **(F)** checked in Fusion before export, listed in section 10.
- **(B)** a bench test at assembly or bring-up.
- **(D)** a design rule the modeller follows and states in the part's notes.

**First prompt for the local session:**

> Read CLAUDE.md and docs/prd-v2.md. Build U1 Breath v2 in Fusion with the Fusion connector, following the PRD.
> Start with the user parameters (section 9), then the 2D layout sketches in section 6.4 and 11, and show me those
> before any solids. Then build one component at a time, run its section 10 checks, show me, and move on. Export to
> cad/fusion-v2/ and commit after each part passes.

## 2. Background: v1 and what went wrong

v1 is a CadQuery model in `cad/u1breath/`, kept only as a reference. Its firmware and Klipper integration carry over
unchanged. Its wiring and BOM carry over with the corrections in section 13. An audit found that v1 could not be
assembled as drawn.

| v1 defect | Prevented by |
|---|---|
| No wire passages between blower cavity, electronics bay and heater; no chamber sensor location | R-WIRE-1 to 8, R-SENS-1 |
| Heater liner left 1 mm around the element: no lead exit, nothing holding the element, no room for screws, rivets or nuts, no earth point | R-HTR-2 to 7 |
| Outlet plate sat 1 mm off the shell, so air leaked around the element | R-HTR-8, R-MECH-2 |
| Blower outlet not sealed to the heater | R-AIR-2, R-HTR-5 |
| Rear screws entered from the wall side with heads proud; countersinks on the wrong face | R-MECH-3 |
| A standoff plugged a wall-mount hole | R-MECH-6 |
| 5 V buck 1 to 2 mm from mains parts | R-ELEC-2 |
| Cord-grip locknut clashed with the fuse holder | R-ELEC-6 |
| Carbon-lid screw heads stopped the grille latching | R-FILT-5 |
| Back plate split in two because the model assumed a 256 mm bed (the U1 bed is 270 mm) | R-MECH-1 |
| Tests checked only the envelope, not fastener access, wire paths or clearances | section 10 |

## 3. Goals and non-goals

Goals, in the owner's words:

1. **Easier to build**: fewer parts and screws, a one-piece chassis, self-aligning parts, screws driven from the front.
2. **Better heating**: blower air ducted straight through the element with no bypass; element firmly held with room for its leads.
3. **Safer electrics**: mains walled off from low voltage, a real earth point on the heater metal, heater fasteners outside the hot air, nothing hot touching plastic.
4. **Easier filter changes**: each bay's carbon and HEPA slide out from the front as one drawer.

Non-goals:

- Firmware code or pin-map changes. Runtime settings are allowed (R-THERM-2).
- Electrical-chain changes. The chain stays L, T5A fuse, SSR, 130 C thermal fuse, element protector, element, N, with earth to the heater metal.
- Purchased-part changes beyond small passives, connectors, fasteners and the cord and gland fixes in section 12.
- A through-the-wall mount. The unit stays inside the chamber.

## 4. Constraints

| Item | Value |
|---|---|
| Envelope, hard limit | 273 tall (Z) x 175 wide (X) x 55 deep (Y), mm, including any VHB pad on the back |
| Envelope, target | 265 tall x 172 wide x 53.5 deep printed, so with a 1.1 mm VHB pad the depth is 54.6 |
| Printer | Snapmaker U1, bed 270 x 270 mm; every printed part at most 266 x 266 (2 mm margin) |
| Material | ASA for every printed part (heat deflection about 95 C) |
| Fasteners | M3 brass heat-set inserts; M3 screws; M2 only where M3 cannot fit |
| Mounting | inside the chamber on the rear wall; Y = 0 is the face against the wall, +Y faces the chamber |
| Mains | 120 V 60 Hz; cord exits through the Sterilite tote cover |
| Coordinates | X = 0 at the left edge as seen from inside the chamber; Y depth; Z up |

Purchased parts (`docs/bom.md`, with the section 13 corrections). Anything marked param is unknown until measured
and is a Fusion user parameter.

| Part | Known data | Param (owner to measure) |
|---|---|---|
| PTC air heater, 110 V 300 W, **insulated** (fins isolated from the electrodes), finned, bundled ~150 C protector | assumed 150 L x 32 D (airflow) x 26 H | length, depth, height, lead-exit end, lead length, ear spacing or none, protector position |
| Blower 7530, 24 V | body 75 x 75 x 30; outlet on one edge; inlet on a large face | ear hole spacing, ear plane, outlet size and position, cable exit side |
| HEPA cells | 4 off, 80 x 40 x 15, two stacked per 80 x 80 bay | none |
| Carbon | pellets larger than 2 mm | none |
| Seeed XIAO ESP32-C3 + u.FL antenna | 21 x 17.5 board, USB-C on a short edge, BOOT and RESET beside it | antenna size |
| HLK-10M24 AC-DC | PCB pins, AC on one end, DC on the other; no mounting holes | body size and pin positions (start 38 x 23 x 18) |
| SSR, 10 A zero-cross, 3-32 V DC input | load and control terminals | body or carrier size (start 40 x 20 x 20) |
| MOSFET module, MP1584 buck | start 30 x 15 x 10 and 22 x 17 x 5 | measured sizes |
| Fuse holder 5 x 20 mm, T5A | style | inline or PCB, size |
| Lever connectors | Wago 221-412 x2 (L in, earth), 221-413 x2 (fused L, N) | none |
| Cord gland | PG7 holds 3 to 6.5 mm cable; PG9 holds 4 to 8 mm | cord outer diameter, so PG7 or PG9 |
| NTC 100K B3950 | chamber: glass bead; duct and bed: M3 ring lug | none |
| 130 C axial thermal fuse | about 6 dia x 14 mm body; **its metal case is live** | none |
| WS2812 LED breakout, JST-XH 2-pin x2 | small | LED board size |
| Aluminum sheet 1.0 mm (5052 or 3003), 3 mm silicone foam | housing and seals | none |

Allowed small additions: 3 x 100 nF, 100 ohm, 330 ohm, 100 uF, two perfboards, a 2-position 5.08 mm screw terminal
for the HLK input, insulated M3 ring terminals, star washers, glass-fibre sleeve, silicone grommets and edge trim
rated 200 C, M3 x 8 metal or ceramic standoffs, fiber or mica washers, M3 nuts, a stainless or aluminum saddle clip,
mica or polyimide insulation, M2.5 screws, female headers.

## 5. Functional requirements

### 5.1 Airflow and heating

- **R-AIR-1 (F)** Air path, in order: chamber, grille, carbon, HEPA, rear plenum, blower inlet, blower outlet, manifold, heater inlet slot, inlet plenum, element fins, outlet face, chamber. Every hole that opens into the path after the filters is sealed (R-SEAL-2).
- **R-AIR-2 (F)** All air leaving the blower passes through the element's fins. The manifold seals to the blower outlet and to the heater's inlet collar (R-HTR-5).
- **R-AIR-3 (F)** Every section of the air path, taken normal to the local flow, is at least `air_min = blower_out_w * blower_out_d` (about 750 mm2). The outlet face's open area is at least `outlet_min = 1.5 * air_min`.
- **R-AIR-4 (F)** Inside the heater, the gap between the element and the housing is at most 2 mm on every side the air could bypass.

### 5.2 Filtration

- **R-FILT-1 (F)** Two bays, each holding two stacked HEPA cells (80 x 40 x 15) behind a carbon cartridge.
- **R-FILT-2 (F)** Each bay's grille, carbon and HEPA come out together as one drawer, from the front, without tools.
- **R-FILT-3 (F)** Each drawer has a positive latch that holds it home against its seal: a quarter-turn cam or an over-centre lever, not a friction tongue. Latched, the drawer cannot move +Y without the latch being released.
- **R-FILT-4 (F)** The seal is a silicone foam gasket on a land at the drawer's back, compressed about 20% (3.0 to 2.4 mm), or a wiping lip seal. A rib or foam strip seals the seam between the two stacked HEPA cells.
- **R-FILT-5 (F)** The carbon cartridge has mesh with 2 mm openings on both faces and a snap lid or flush countersunk M2 screws. Nothing on it projects into other drawer parts.

### 5.3 Sensors and user access

- **R-SENS-1 (F)** The chamber NTC sits in filtered air upstream of the heater: in the rear plenum behind the blower.
- **R-SENS-2 (F)** The duct NTC (M3 ring lug, Kapton under the lug) fastens on a tab folded up from the housing's top wall at the outlet edge. The tab has three M3 holes at 20 mm pitch over the middle third of the element, so the position can be tuned at bring-up. Each hole has room for a screw head on the front and a nut behind.
- **R-SENS-3 (F)** The 130 C thermal fuse sits in the lead compartment (R-HTR-6), on the baffle facing the element's end. Its live case is insulated: two wraps of polyimide tape plus glass-fibre sleeve, or a 0.2 mm mica sheet. A saddle clip about 10 x 25 mm under one M3 screw and nut presses it onto the baffle. Its crimps sit at least 10 mm from the case.
- **R-SENS-4 (F)** The bed probe plugs into a JST-XH socket on the low-voltage board. Its cable leaves through a slot open to the low-voltage cover's edge, so the cover lifts off over it, and a strain relief on the chassis takes the pull.
- **R-UI-1 (F)** The WS2812 sits within 8 mm behind a 10 x 10 mm window in the low-voltage cover. It is either on the board under a printed light pipe, or on the cover on a JST lead.
- **R-UI-2 (F)** The XIAO's BOOT button is pressed through a printed guide tube from the cover to within 2 mm of the button, inner diameter about 2.5 mm. A 1.5 mm pin along the tube's axis touches BOOT and clears RESET by at least 1.5 mm.
- **R-UI-3 (F)** The XIAO's USB-C port can be reached with only the low-voltage cover removed. A plug keep-out (20 x 12 x 8 mm, then cable room) in front of the port interferes with nothing.
- **R-UI-4 (F)** The u.FL antenna sits on the inside of the low-voltage cover or the outer side wall. It is at least 20 mm from heater metal and the back face, and at least 6 mm from mains parts. Its lead stays in the low-voltage area with slack to remove the cover.

### 5.4 Thermal limits

- **R-THERM-1 (D, B)** Printed parts stay out of the outlet jet. Surfaces within 20 mm of heater metal measure at most 85 C with a 70 C chamber during bring-up.
- **R-THERM-2 (D, B)** The electronics are rated about 70 C, and the firmware allows chamber targets up to 70 C. Until the bring-up shows SSR, HLK and buck case temperatures inside their derating at the chamber target in use, set the unit's maximum target to 60 C. This is a runtime setting (`/settings?max=60`), not a firmware change.

## 6. Subsystem requirements

### 6.1 Chassis and mechanics

- **R-MECH-1 (F)** One printed chassis carries the back face, outer walls, slabs between bands, internal walls, bosses, standoffs and cradles. It prints back-face-down within 266 x 266, without supports.
- **R-MECH-2 (F)** Every other part locates on the chassis by a feature (lip, rail, pin, pocket or tongue and groove) before its screws go in. That includes the heater's outlet face, which seats with zero gap or a stated gasket.
- **R-MECH-3 (F)** No assembly screw enters from the back face. The back face is flat apart from wall-mount holes. The only exception is the optional wall bolts in R-MECH-6.
- **R-MECH-4 (F)** Every screw is driven from the front with a straight tool path at least 8 mm wide and 60 mm long at its step in the assembly sequence (section 10.2). It lands in a heat-set insert, a captive nut, or, for metal-to-metal joints, a free nut with a 5.5 mm nut-driver lane at least 10 mm long.
- **R-MECH-5 (F)** Insert bosses are at least 7.5 mm across. Hole diameter follows the insert maker's spec for the measured insert (`insert_d`), and hole depth is the insert length plus 1 mm (`insert_depth`). Each insert can be pressed in with a soldering iron from the front.
- **R-MECH-6 (F)** Wall mounting: the flat back takes 3M VHB pads by default. Options are keyhole slots, or through-bolt bosses with M4 inserts whose bolts enter from the wall side. Mounting holes sit only in solid regions outside the air path, or in sealed boss tubes, at least 2 mm from any other feature. Nothing covers a mounting hole. An allowed-zone sketch on the back face shows where holes may go.

### 6.2 Heater housing (1.0 mm aluminum)

- **R-HTR-1 (F)** The element sits in a folded aluminum housing. Its back wall is closed and forms an inlet plenum behind the element. Air enters through a slot in the bottom wall under that plenum and leaves through the front outlet face.
- **R-HTR-2 (F)** The housing's inner length is `ptc_l + ptc_lead_allow + ptc_end_clear`. The lead allowance is at least `lead_slot_w + 2 * (2.5 * al_t + bend_r)` (15 mm; start 16).
- **R-HTR-3 (F)** The element is held by its own ears through slots no wider than the ear plus 1 mm, out to outward flanges. If it has no ears, two folded clamp straps outside the fins hold it. The ceramic never carries load.
- **R-HTR-4 (F)** No fastener, rivet or nut sits in the element zone, where gaps are at most 2 mm. Fasteners go on outward flanges, on tabs, in the lead compartment, or in the inlet plenum.
- **R-HTR-5 (F)** An aluminum inlet collar surrounds the bottom slot and reaches at least `hot_gap + 3` mm down into the manifold. The manifold seals to the collar's lower end with silicone foam in the cool inlet stream.
- **R-HTR-6 (F)** At the lead end, an aluminum baffle with a notch for the leads (gap at most 2 mm) separates a lead compartment from the air path. The compartment is closed on the front, top and outer end, and the outlet openings and inlet slot do not extend over it. The leads leave through an 8 x 14 mm slot in its bottom wall with 200 C silicone edge trim. An aluminum chimney carries them down across the hot gap to the slab over the mains area, so no lead is exposed. The thermal fuse (R-SENS-3) and the earth screw (R-HTR-7) are inside it. If the element has leads at both ends, the far lead returns inside an aluminum channel along the housing, glass-sleeved.
- **R-HTR-7 (F, B)** A dedicated earth screw in the lead compartment clamps nothing else. A star washer bites bare aluminum under the ring lug, and another sits under the nut. Every separate metal part (housing body, baffle, chimney, straps, outlet face, element ears) bonds through at least one star-washered M3 joint.
- **R-HTR-8 (F)** The outlet face is part of the housing or screws to its flanges with no gap. Its openings cover only the element zone.
- **R-HTR-9 (F)** The housing mounts to the chassis back through at least four M3 standoffs at least `hot_gap` long, made of stainless steel, ceramic or PPS, with a fiber or mica washer at the aluminum end.
- **R-HTR-10 (F)** The housing's flat patterns, including the baffle, chimney, clip and tab, nest on one sheet no larger than the BOM sheet size and export to DXF with bend lines.

### 6.3 Hot-gap rule

- **R-GAP-1 (F)** Plastic and purchased plastic bodies stay at least `hot_gap` (8 mm) from heater metal. The only exceptions are named bodies in this table.

| Exception | Why allowed |
|---|---|
| Housing standoffs (R-HTR-9) | metal or ceramic, with the boss face `hot_gap` from the sheet |
| Manifold seal at the inlet collar's lower end (R-HTR-5) | in the cool inlet stream, silicone foam |
| Lead slot edge trim and the chimney's silicone grommet in the slab | silicone rated 200 C |

### 6.4 Electronics bay

- **R-ELEC-0 (F)** Before modelling solids, draw a 2D layout sketch of the bay with every module footprint driven by parameters, the mains/low-voltage wall, the gland and its wrench envelope, and every wire route. The owner approves it first.
- **R-ELEC-1 (F)** The bay has a mains area and a low-voltage area, separated by a printed wall from the chassis back to the covers. The wall's front edge has a tongue at least 2 mm deep in a groove in the covers.
- **R-ELEC-2 (F)** Every mains body (gland, cord, Wagos, fuse holder, SSR load side, HLK AC pins and screw terminal, heater leads) is at least 6 mm from every low-voltage body, unless the wall stands between them.
- **R-ELEC-3 (F)** The HLK sits in a cradle formed in the wall, notch = body outline + `fit_slide`. Its AC pins solder to a small mains board carrying the 2-position screw terminal; its DC pins solder to the low-voltage board. No board crosses the wall. Soldered component pins on a screwed-down board are acceptable; R-SAFE-4 applies to wire joints.
- **R-ELEC-4 (F)** The SSR straddles the wall through a notch, load terminals on the mains side and control on the low-voltage side, each terminal at least 6 mm from the wall. Notch gaps around the HLK and SSR are at most 1 mm.
- **R-ELEC-5 (F)** The mains area has its own cover with at least two screws. Its insert bosses sit at least 6 mm from mains terminals, or the cover uses nylon screws. The low-voltage area has its own cover with two M3 screws, the LED window, the BOOT guide tube and the probe slot. Removing it leaves the mains cover in place.
- **R-ELEC-6 (F)** The cord enters the mains area through a PG7 or PG9 gland (param) in a recessed pocket, so the gland stays inside the envelope. A printed hex trap holds the locknut, so the gland tightens from outside. Hole = thread diameter + `fit_slide`. The locknut envelope (corner diameter x thickness) and a 25 x 15 mm wrench envelope interfere with nothing.
- **R-ELEC-7 (F)** Every mains part is held mechanically: the Wagos in a printed holder or a 221-500 carrier, the fuse holder clipped, boards screwed. VHB is allowed only for low-voltage parts. Do not assume mounting holes a module does not have.
- **R-ELEC-8 (F, B)** Both areas have low and high vent slots to chamber air, each area about 300 mm2 or more. Slots are at most 3 mm wide, with no straight line from a vent to a live terminal closer than 10 mm. The SSR sits near the high vents with 5 mm of free air on its faces. The slab over the mains area has an air gap below the heater band.
- **R-ELEC-9 (F)** The mains area sits directly below the heater's lead end. The parameter `layout_mirror` swaps the blower side and the electronics side when the element's leads exit at the other end.

### 6.5 Wire passages

Each passage lists its conductors and a bore. Passages that open into the air path after the filters are sealed
after wiring (R-SEAL-2).

| ID | From, to | Conductors | Bore |
|---|---|---|---|
| R-WIRE-1 | outside to mains area, via the gland | cord | gland |
| R-WIRE-2 | heater lead compartment to mains area, via slot, chimney and slab grommet | live feed from SSR load 2 to the thermal fuse, neutral return from the element, earth (the fuse, protector and element leads stay in the compartment) | 9 mm |
| R-WIRE-3 | duct NTC tab, along the housing top to the blower-side end, down outside the housing in a printed lane at least `hot_gap` from metal or in glass-fibre sleeve, through the slab over the blower into the blower cavity | 2 NTC wires | 5 mm, sealed |
| R-WIRE-4 | blower cavity to low-voltage area, through the partition at low-voltage height | blower cable, chamber NTC, duct NTC | 8 mm, sealed |
| R-WIRE-5 | SSR control and HLK DC cross the wall only through the modules themselves | none | none |
| R-WIRE-6 | bed probe, outside to low-voltage area via the open-edged slot | probe cable | slot |

- **R-WIRE-7 (F)** Every route is a swept pipe of its bundle diameter (18 AWG silicone about 2.5 mm, glass-sleeved about 3.5 mm) with a bend radius of at least 3x the bundle diameter, in a "Routes" component included in the interference and mains-spacing checks.
- **R-WIRE-8 (D)** Each route's swept length plus a 30 mm service loop goes into a wire cut list in `docs/assembly.md`. Flag any heater-lead route longer than the element's own leads.

### 6.6 Sealing

- **R-SEAL-1 (F)** Every joint in the air path between filters and outlet has a gasket land for 3 mm silicone foam at about 20% compression, or a slip fit with at least 3 mm overlap where both parts are plastic.
- **R-SEAL-2 (D)** Passages R-WIRE-3 and R-WIRE-4 get slit membrane grommets or RTV after wiring.

## 7. Safety requirements

- **R-SAFE-1 (F)** With all covers on, a 12 x 80 mm finger body and a 2.5 x 100 mm rod pushed through every opening reach no mains body or route. These openings are the outlet face, side windows, vents, LED window, BOOT tube, probe slot and gland.
- **R-SAFE-2 (F)** With only the low-voltage cover off, the finger reaches no mains body from the low-voltage side.
- **R-SAFE-3 (B)** Earth: with meter leads zeroed, the plug earth pin to each separate metal part reads under 0.1 ohm. L or N to earth reads open.
- **R-SAFE-4 (D)** No mains wire joint is solder-only. Mains wires use crimps, ferrules, Wago connectors or screw terminals.
- **R-SAFE-5 (F)** Mains wires that leave the electronics bay run only inside the lead compartment, its chimney and the far-lead channel.
- **R-SAFE-6 (B)** Before assembly, on the highest resistance range: no continuity from either element lead to its fins or ears. With the thermal fuse fitted and clipped, no continuity from either fuse lead to the housing.
- **R-SAFE-7 (B)** Supervised stall test at bring-up on a GFCI, blower unplugged, with thermocouples at the duct NTC hole, the thermal fuse and the nearest plastic. It passes when the 105 C duct cutoff trips while the fuse position is at least 15 K below 130 C and the plastic stays at or below 85 C. Otherwise move the NTC to another tab hole and repeat.

## 8. Manufacturability

- **R-MFG-1 (F)** Every printed part fits 266 x 266 in its stated print orientation.
- **R-MFG-2 (F)** No printed part needs supports: Fusion's overhang analysis in print orientation shows nothing below 45 degrees except bridges under 20 mm.
- **R-MFG-3 (D)** Sliding fits use `fit_slide` (0.3 mm per side); press fits use `fit_press` (0.15 mm).
- **R-MFG-4 (D)** STL exports are in print orientation.

## 9. Fusion deliverable

- **R-FUS-1** One Fusion design with one component per part: chassis, each cover, each drawer's parts, manifold, and each aluminum part. Purchased parts are placeholder bodies in a "Purchased" component, split into named bodies where a check needs it (`hlk_ac`, `hlk_dc`, `hlk_body`, `ssr_load`, `ssr_ctrl`, `ssr_body`). Also include: an "Airpath" component (a solid of the air volume with named section planes S1 to Sn); "Routes" (R-WIRE-7); and "Keepouts" (USB-C plug, wrench, locknut, finger and rod probes, tool cylinders).
- **R-FUS-2** User parameters drive the model. Derived values are expressions.

| Parameter | Start | Meaning |
|---|---|---|
| bed / bed_margin | 270 / 2 mm | printer bed and margin; parts at most `bed - 2*bed_margin` |
| unit_h / unit_w / unit_d | 265 / 172 / 53.5 mm | printed envelope |
| vhb_t | 1.1 mm | VHB pad, counted in the 55 mm limit |
| wall / slab_t | 3 / 3 mm | printed wall and band slab |
| layout_mirror | 0 | 1 swaps blower and electronics sides |
| ptc_l / ptc_d / ptc_h | 150 / 32 / 26 mm | element |
| ptc_lead_allow / ptc_end_clear | 16 / 1 mm | lead end allowance, far end clearance |
| ptc_ear_pitch / ptc_ear_w | 0 / 10 mm | ear spacing (0 = no ears, use straps), ear width |
| lead_slot_w / lead_slot_l | 8 / 14 mm | lead exit slot |
| al_t / bend_r | 1 / 1 mm | sheet and bend radius |
| hot_gap | 8 mm | plastic to heater metal |
| inlet_plenum_t | `max(6 mm; unit_d - wall - hot_gap - 2*al_t - ptc_d)` | heater inlet plenum depth |
| inlet_slot_l | `ptc_l - 10 mm` | inlet slot length; `inlet_slot_l * inlet_plenum_t` must be at least `air_min` |
| ntc_tab_h | 10 mm | duct NTC tab height |
| blower_w / blower_h / blower_t | 75 / 75 / 30 mm | blower body |
| blower_ear_pitch / blower_ear_d | 64 / 4.5 mm | blower ears |
| blower_out_w / blower_out_d | 30 / 25 mm | blower outlet |
| air_min / outlet_min | `blower_out_w*blower_out_d` / `1.5*air_min` | air path minimums |
| plenum_t | 12 mm | rear plenum depth |
| manifold_h | `air_min / blower_out_d` (30 mm) | manifold interior height |
| hepa_w / hepa_h / hepa_t / carbon_t | 80 / 40 / 15 / 15 mm | filters |
| rail_t / grille_t / front_lip | 2 / 3 / 2 mm | drawer |
| gasket_t / gasket_comp | 3 / 0.2 | gasket thickness and compression |
| standoff_h | 4 mm | module standoffs |
| mains_lv_gap | 6 mm | mains to low-voltage spacing |
| gland_hole / gland_nut_af / gland_nut_t | 12.5 / 19 / 5 mm | gland (PG7 start; PG9: 15.2 / 24 / 5) |
| hlk_w / hlk_l / hlk_t, ssr_w / ssr_l / ssr_t, mosfet_*, buck_*, lv_board_w / lv_board_l | see section 4 | module sizes (LV board start 50 x 70) |
| insert_d / insert_depth | per insert spec / insert length + 1 mm | M3 insert hole |
| fit_slide / fit_press | 0.3 / 0.15 mm | fits |
| tool_d / tool_l | 8 / 60 mm | tool-access cylinder |
| z1 / z2 | `slab_t + 2*rail_t + 2*hepa_h + 2*fit_slide + 3.4 mm + slab_t` / `z1 + blower_h + 1 mm + slab_t` | band boundaries (94, 173) |

- **R-FUS-3** Sheet-metal parts use a Fusion sheet-metal rule: 1.0 mm aluminum, K-factor about 0.44, bend radius 1 mm. If the connector cannot create sheet-metal features, model thin solids and draw the flat patterns as sketches for DXF.
- **R-FUS-4** The timeline is grouped per part, features are named, and sketches are fully constrained.
- **R-FUS-5** Exports go to `cad/fusion-v2/`: STL per printed part in print orientation, STEP of the assembly and of each part, DXF flat patterns, and a `.f3d` archive.

## 10. Acceptance checks

### 10.1 Checks run in Fusion before export

| Check | Pass when |
|---|---|
| Interference | none across all components, purchased placeholders, Routes and Keepouts (except a keep-out body tested against its own target) |
| Envelope | assembly bounding box at most `unit_h x unit_w x unit_d`; plus `vhb_t`, at most 273 x 175 x 55 |
| Bed fit | every printed part in print orientation within `bed - 2*bed_margin` square |
| Hot gap | minimum distance from heater metal to every plastic and purchased plastic body is at least `hot_gap`, except the R-GAP-1 bodies |
| Mains spacing | every mains body or route at least `mains_lv_gap` from every low-voltage body or route, measured pairwise; a pair closer than that passes only if a straight line between them hits the wall |
| Air path | every Airpath section S1..Sn at least `air_min`; outlet open area at least `outlet_min`; no unsealed hole joins the path after the filters |
| Element gap | maximum element-to-housing-inner distance on bypass sides at most 2 mm |
| Gland | locknut and wrench envelopes interfere with nothing |
| Tool access | a `tool_d x tool_l` cylinder on each screw axis, in front of the head, clears everything present at that screw's step in 10.2 |
| Drawers | each drawer travels its own depth plus 15 mm along +Y without interference; latched, the gasket gap equals `gasket_t*(1-gasket_comp)` within 0.3 mm all round |
| Outlet face | seats on its locating feature with zero gap or the stated gasket |
| UI | BOOT pin cylinder hits BOOT only and clears RESET by 1.5 mm; LED within 8 mm of its window; USB-C keep-out clears with the low-voltage cover off |
| Touch | finger and rod probes per R-SAFE-1 and R-SAFE-2 reach no mains body |
| Flat back | nothing behind Y = 0 except optional wall bolts |
| Overhangs | overhang analysis per R-MFG-2 |
| Sheet | housing flat patterns nest within the BOM sheet |
| Parameter sweep | rebuild and re-check with: `ptc_l` 140 and 150; `ptc_d` 32 and 33; `ptc_h` 26 and 28; `ptc_ear_pitch` 0 and 120; `layout_mirror` 0 and 1 |

### 10.2 Assembly sequence (used by the tool-access check)

1. Press all inserts into the chassis.
2. Fit the low-voltage board (XIAO on female headers, dividers, JSTs) and the mains board (HLK screw terminal) with the HLK in its wall cradle.
3. Fit the SSR through its wall notch, then the MOSFET module, buck, fuse holder and Wago holder.
4. Fit the gland and its locknut; feed the cord through.
5. Fit the blower in its cradle, inlet toward the rear plenum; fit the chamber NTC in the plenum.
6. Wire the low-voltage side; pass the blower cable and chamber NTC through R-WIRE-4.
7. Assemble the heater off the unit: element in the housing, baffle, thermal fuse with its insulation and clip, earth screw and lug, chimney, duct NTC on its tab.
8. Fit the manifold with its seals.
9. Mount the heater on its four standoffs, feeding the leads down the chimney into the mains area.
10. Wire the mains side; route the duct NTC lead via R-WIRE-3 and R-WIRE-4; seal the passages.
11. Fit the mains cover, then the low-voltage cover.
12. Load the drawers (HEPA, seam strip, carbon cartridge) and latch them in.
13. Run the bench tests R-SAFE-3 and R-SAFE-6.
14. Mount on the rear wall; route the cord and bed probe.
15. Bring-up per `docs/bringup.md`, including R-SAFE-7 and R-THERM-2.

## 11. Recommended architecture

A one-piece printed chassis tub, open to the front, in three bands. The blower's inlet faces the back, so filtered
air rises straight from the rear plenum into it.

### 11.1 Bands (Z, mm)

| Band | Z | Stack |
|---|---|---|
| Filters | 0 to 94 | floor 3; bottom rail + fit 2.3; two HEPA cells 80; top rail + fit 2.3; latch reserve 3.4; slab 3 (shared with the blower band floor) |
| Blower + electronics | 94 to 173 | blower 75; clearance 1; slab 3 |
| Heater | 173 to 265 | manifold 30; manifold top and seal land 3; hot gap 8 (bridged by the inlet collar); housing 30 (sheet 1 + clearance 1 + element 26 + clearance 1 + sheet 1); NTC tab 10; hot gap 8; roof 3 |

The heater band sums to 92 exactly. If any value grows (for example `ptc_h` 28), drop the heater-band roof and leave
the housing top open to chamber air like its sides.

### 11.2 Depth (Y, mm)

| Band | Stack | Total |
|---|---|---|
| Filters | back 3; rear plenum 12; gasket 2.4; HEPA 15; carbon 15; grille 3; front lip 2 | 52.4 |
| Blower | back 3; rear plenum 12 (blower inlet faces it); blower 30; cover 3 | 48 |
| Electronics | back 3; standoffs 4; modules up to 20; headroom; cover 3 at Y 45 to 48 | 48 |
| Heater | back 3; hot gap 8; housing back 1; inlet plenum 8.5; element 32; outlet face 1 | 53.5 |

The heater stack plus a 1.1 mm VHB pad is 54.6, inside 55. The inlet plenum follows its expression: 7.5 with
`ptc_d` 33, 6.5 with 34, and 6 (its minimum) at 35, where the heater no longer fits and the owner must decide.

### 11.3 Width (X, mm)

| Band | Stack | Total |
|---|---|---|
| Filters | wall 3; bay 80.6; divider 3.4; bay 80.6; wall 3 | 170.6 |
| Blower + electronics | wall 3; blower pocket 75.6; partition 3; bay 87.4; wall 3 | 172 |
| Heater | housing `ptc_l + 16 + 1 + 2` = 169, on open side windows | 169 |

The bay divider stops at the rear plenum, so both bays share it. Above Z 94 the plenum continues only behind the
blower: 12 x 75 = 900 mm2, about 780 after two cradle posts in one plane, which is at least 750.

**Width conflict at the heater.** A 169 mm housing leaves 1.5 mm per side, so the heater band has no side walls. The
housing's aluminum ends face chamber air through open side windows, inside the printer enclosure, as on the Panda
Breath's metal body. If the measured `ptc_l` is 131 mm or less (`unit_w - 2*(hot_gap + wall) - 19`), side walls fit
with full gaps.

### 11.4 Air path

Grille, drawer, rear plenum (both bays) up behind the blower into its inlet, outlet up through the slab into the
manifold. The manifold spreads the 30 x 25 outlet along X and moves it back to the inlet slot under the housing's
inlet plenum. Each manifold section is `manifold_h` x 25 = 750 mm2 or more. The inlet collar drops into the
manifold's top opening and seals there. The inlet plenum feeds the fins, and the fins feed the outlet face.

### 11.5 Electronics bay

The bay is 87.4 x 76 mm (X x Z) at the electronics side of the blower band, with the mains area at its top, directly
under the heater's lead end and chimney. The low-voltage area is below, near R-WIRE-4. Estimated module footprints fill
about 75% of the area before spacing. If the layout sketch (R-ELEC-0) does not fit, move the Wagos and fuse holder
into a printed mains junction box in the heater band under the lead end, walled and at least `hot_gap` from the
housing.

## 12. Open questions for the owner

1. **Element:** length, depth, height, which end the leads exit (and whether both ends), lead length, mounting ears and spacing, protector position. Confirm it is the insulated type.
2. **Blower:** ear spacing, diameter and which face the ears are on; outlet size and position; cable exit side.
3. **Cord:** measure its outer diameter. Over 6.5 mm needs a PG9 gland instead of PG7. A 105 C cord (SJTW or SJOOW) is better than plain SJT inside a hot chamber.
4. **Lever connectors:** the circuit needs two Wago 221-412 and two 221-413. A 221-413 joins all three of its ports, so one cannot hold L, N and earth apart.
5. **Rear wall:** clear width and height, existing holes and spacing, material. This decides VHB, keyholes or bolts.
6. **Module sizes:** measure the HLK-10M24, SSR, MOSFET module, buck and fuse holder you received.
7. **Chamber target:** keep the 60 C cap (R-THERM-2) until bring-up measures the electronics, or source 85 C-rated modules.

## 13. Rules for the local session

- Follow CLAUDE.md's cost rules. Fusion connector calls and screenshots are expensive: build one part, run its checks, show it, then move on. Screenshot only finished parts and failed checks.
- Keep the v1 model in `cad/u1breath/` untouched until v2 passes section 10.
- Commit exports and docs together, one validated commit per finished part, on `u1breath-design`.
- With the v2 commit, correct these documents:
  - `docs/wiring.md`: mains stays in the mains area or the lead compartment; one lever connector per node (L in, fused L, N, earth); the SSR wall crossing; the thermal-fuse clip and insulation; the new chamber and duct NTC locations.
  - `docs/bom.md`: Wago 2 x 221-412 and 2 x 221-413; measured SSR and HLK sizes; 105 C cord and PG7 or PG9; silicone grommets and trim; M3 x 8 metal standoffs and mica or fiber washers; the fuse clip and insulation; sheet size for the nested flat patterns; insert spec and M3 x 10 for flange mounts.
  - `docs/bringup.md`: element and fuse isolation checks (R-SAFE-6), per-part earth checks (R-SAFE-3), the stall test (R-SAFE-7), the 60 C cap (R-THERM-2), and re-measuring the duct NTC target at its new location.
  - `docs/assembly.md` and the assembly guide document: rewrite for v2, with the wire cut list (R-WIRE-8).
