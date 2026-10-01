# U1 Breath

A chamber heater and HEPA + activated-carbon filter unit for the **Snapmaker U1**, in the
same class and the same 273 x 175 x 55 mm envelope as the BIQU Panda Breath.

- 300 W 120 V PTC heater, 7530 blower, two 80x80 filter bays (four 80x40x15 HEPA cells plus
  pellet carbon cartridges)
- Own mains power supply; plugs into a wall outlet, works with the printer off
- WiFi web UI, preheat, auto, filament-drying and filter-only modes
- A thermistor stuck under the heated bed turns the unit on and off by itself
  (default: heat when bed >= 90 C, stop below 70 C, filter-only above 45 C)
- Klipper integration with **zero printer-side code**: the firmware speaks the open
  [DragonBreath](https://github.com/plastikman/DragonBreath) REST API, which the
  [paxx12 U1 Extended Firmware](https://github.com/paxx12-snapmaker-u1/SnapmakerU1-Extended-Firmware)
  already drives as a `heater_generic`, so `M141` / `M191` from OrcaSlicer just work
- Mounts inside the chamber on the rear wall, printed in ASA/ABS with M3 heat-set inserts;
  only the heater duct liner is aluminum

## Repository map

| Path | What it is |
|---|---|
| `docs/design.md` | Architecture, airflow, thermal and dimension budgets, safety model |
| `docs/bom.md` | Bill of materials with ratings and example parts |
| `docs/wiring.md` | Wiring diagram, connector pinout, mains safety notes |
| `docs/assembly.md` | Print settings, inserts, step-by-step assembly, liner folding |
| `docs/bringup.md` | First-power checklist, foldback calibration, Klipper enable steps |
| `docs/measurements.md` | The handful of measurements only the owner can take |
| `cad/` | CadQuery parametric model; `python cad/build.py` exports STL, STEP, DXF, SVG |
| `firmware/` | DragonBreath fork with the `u1breath` board profile |
| `klipper/` | Optional macros for the paxx12 `klipper_includes` feature |

## Quick start

1. Read `docs/measurements.md` and fill in `cad/u1breath/params.py`.
2. `pip install cadquery` then `python cad/build.py` to get the printable parts in `cad/out/`.
3. Order the parts in `docs/bom.md`.
4. Build and flash the firmware (`firmware/README.md`), join it to WiFi, give it a static DHCP lease.
5. Assemble (`docs/assembly.md`), then follow `docs/bringup.md` before the first heated print.

## Safety

This project switches 120 V mains inside a printer enclosure. The heater path has three
independent cut-offs (bimetal thermal protector bundled with the PTC element, a one-shot
thermal fuse on the duct liner, and the firmware's latching over-temperature logic), but
the build is only as safe as its wiring. Use the cord, fuse, and crimps specified in the BOM,
keep every mains conductor inside the electronics bay, and never run the heater with the
blower disconnected.
