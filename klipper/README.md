# Klipper integration (paxx12 U1 Extended Firmware)

The unit speaks the DragonBreath REST API, which the
[paxx12 U1 Extended Firmware](https://github.com/paxx12-snapmaker-u1/SnapmakerU1-Extended-Firmware)
already supports. No Python, no custom Klipper module.

1. Give the unit a static DHCP lease (its IP must never change between prints).
2. On the printer open `http://<printer-ip>/firmware-config/`, section
   **Snapmaker Components -> PandaBreath / DragonBreath Chamber Heater**, enable
   **DragonBreath**, enter the unit's IP (port 80, token only if you set one in the
   unit's web UI), save. The printer generates
   `extended/klipper/dragonbreath.cfg` with `[dragonbreath] host: <ip>`.
3. Optional: install `u1breath.cfg` from this folder as a custom include for the
   `CHAMBER_PREHEAT`, `CHAMBER_SET`, `CHAMBER_OFF`, `CHAMBER_FILTER` macros.
4. In OrcaSlicer's U1 profile, set the filament's chamber temperature (ABS/ASA 55 C,
   PC 60 C) and make sure the machine start G-code emits `M191` after bed heating,
   for example:

```
M140 S[bed_temperature_initial_layer_single]
M191 S[chamber_temperature]     ; U1 Breath: heat and wait (S0 for PLA/PETG)
```

and the end G-code emits `M141 S0`.

## How the two controllers share the heater

- Klipper's `M141`/`M191` put the unit into a POWER_ON session with a heartbeat
  lease. If Klipper crashes or the printer goes away, the lease expires and the unit
  latches the heater off (default 5 minutes, adjustable 10 s to 5 min).
- The unit's AUTO mode (bed-probe trigger) keeps working underneath: Klipper's
  `M141 S0` at the end of a print returns the unit to AUTO "waiting" instead of OFF,
  so a print that never sends `M141` still gets chamber heat from the bed probe and
  filtration from the filtration band.
- The upstream Moonraker-fed AUTO (filament zone) is disabled while the paxx12
  helper is installed, as upstream intends. The bed probe path is not, because it is
  a physical sensor on the machine.
- `DRAGONBREATH_RESET` clears a latched fault from the printer console.

## Caveat

The paxx12 docs note that chamber heating needs extra U1 mainboard cooling (the
RK3562 throttles at 85 C). This build assumes the mainboard and stepper driver fan
mod is installed. Watch `temperature_sensor` values for the host during the first
heated prints (see `docs/bringup.md`).
