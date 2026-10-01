# Bill of materials

Prices are rough 2026 US retail. "Example" parts are ones that match the spec; any part with
the same ratings works. Confirm the three outer dimensions of the PTC element you buy and put
them in `cad/u1breath/params.py` (see `docs/measurements.md`).

## Heater and air

| Qty | Part | Spec | Example / notes | ~USD |
|---|---|---|---|---|
| 1 | PTC air heater element | 110 V, 300 W, insulated, finned, with bundled normally-closed thermal protector (about 150 C). Typical body 150 x 32 x 26 mm | AliExpress/Amazon "110V 300W insulated PTC ceramic air heater". The 120 V US supply pushes it slightly above nameplate; the element self-limits | 12 |
| 1 | Thermal fuse | 130 C, 10 A, 250 V, axial (TF type). One-shot backstop strapped to the liner | Microtemp G4A01130 or equivalent | 2 |
| 1 | Blower | 7530 centrifugal, 24 V DC, 2-wire, ball bearing preferred, 15 to 20 CFM, 0.15 to 0.25 A | GDSTIME 7530 24 V, Sunon/ Delta equivalents | 9 |
| 4 | HEPA cells | 80 x 40 x 15 mm (you have these) | | 0 |
| 2 | Carbon fill | pellet activated carbon, about 60 g per cartridge | your Amazon pellet carbon | 0 |
| 1 | Aluminum sheet | 1.0 mm, 5052 or 3003, 200 x 160 mm minimum, for the folded liner and outlet flange | hardware store or McMaster 89015K18 | 8 |
| 1 | Aluminum mesh (optional) | fine mesh for the carbon cartridge faces if you prefer not to print mesh | | 4 |

## Electronics

| Qty | Part | Spec | Example / notes | ~USD |
|---|---|---|---|---|
| 1 | MCU board | Seeed XIAO ESP32-C3 with u.FL antenna | the external antenna matters inside a metal printer | 6 |
| 1 | 2.4 GHz antenna | u.FL, flexible FPC or short dipole, 50 to 100 mm lead | mounted on the plastic shell, away from the liner | 3 |
| 1 | AC-DC module | HLK-10M24, 24 V 0.42 A, 100 to 240 V in, rated to 70 C | Hi-Link | 6 |
| 1 | Buck module | 24 V to 5 V, 1 A, rated to 70 C | MP1584 mini module set to 5.0 V | 2 |
| 1 | SSR | PCB-mount, zero-cross, 10 A at 240 VAC, 3 to 32 VDC input | Omron G3MB-202P is only 2 A: do not use. Use a 10 A class part (e.g., "MGR-1 D4810" style on a small carrier, or a 10 A G3NA-210B with its heatsink if the bay is widened) | 8 |
| 1 | MOSFET module | logic-level N-channel, 3.3 V gate drive, for 24 V fan PWM at 25 kHz | D4184 module, or AO3400 on a breakout | 2 |
| 3 | NTC thermistor | 100K, Beta 3950, 1%: one glass bead for chamber air, one ring-lug M3 type for the duct wall, one ring-lug M3 type for the bed probe | Klipper's standard sensor; ring-lug types from 3D printer bed-thermistor listings | 6 |
| 3 | Resistor | 100 kOhm, 1%, 0603 or through-hole, NTC divider | | 0.5 |
| 1 | WS2812B LED | single 5 mm or 5050 on a tiny breakout | status LED behind a translucent window | 1 |
| 1 | Fuse holder + fuse | panel or inline 5 x 20 mm holder, 5 A slow-blow (T5A 250 V) | | 3 |
| 1 | Terminal block | 3-position, 10 A, screw or lever (Wago 221-413 x2) | mains junction inside the electronics bay | 3 |
| 1 | Power cord | 18 AWG SJT, 3-conductor, grounded, 1.8 m, bare end | the earth conductor bonds to the liner | 8 |
| 1 | Cord grip | PG7 or M12 strain relief, nylon | | 1 |
| 1 | Rubber grommet | for the Sterilite cover hole, sized to the cord | | 1 |
| 1 | JST-XH 2-pin pair | bed probe connector on the unit | | 1 |
| 1 | JST-XH 2-pin pair | blower connector (most blowers come with XH 2.54) | | 1 |
| | Wire | 18 AWG silicone high-temp for mains inside the bay, 24 AWG silicone for sensors, 600 mm 2-conductor silicone lead for the bed probe | | 5 |
| | Crimps | insulated spade/ring crimps for the PTC and fuse holder leads, ferrules for the terminal block | | 3 |
| 1 | Heat-shrink | assorted, plus a few glass-fiber sleeves for the PTC leads | | 2 |

## Mechanical and consumables

| Qty | Part | Spec | ~USD |
|---|---|---|---|
| 24 | Heat-set inserts | M3 x 5.7 mm (OD 4.0), brass | 4 |
| 24 | Screws | M3 x 8 button head | 2 |
| 8 | Screws | M2 x 6 (carbon cartridge lids) + M2 inserts | 2 |
| 4 | Mounting | M4 x 12 + nuts or 3M VHB 5952 pads, depending on the rear wall | 3 |
| 1 | Kapton tape | 20 mm | 3 |
| 1 | Thermal epoxy or a dab of RTV | bed probe retention | 4 |
| 1 | High-temp foam tape | 3 mm silicone foam, seals the filter grille and liner flange | 4 |
| | Filament | about 350 g ASA or ABS | 10 |

Total, excluding filters and carbon you already own: roughly 120 to 150 USD.

## Why these ratings

- 300 W at 120 V is 2.5 A. Fuse at 5 A slow-blow so PTC inrush (about 2x for a second) does
  not nuisance-trip. SSR at 10 A gives 4x margin for derating at 60 C chamber temperature.
- Blower at 24 V keeps the HLK-10M24 as the only AC-DC converter. The XIAO draws under 150 mA
  at 5 V through the buck.
- Every active part is rated for at least 70 C ambient because the whole unit lives at
  chamber temperature.
