# U1 Breath firmware

The firmware is [DragonBreath](https://github.com/plastikman/DragonBreath) with a
`u1breath` board profile (see `UPSTREAM.md` for exactly what differs). You get the
upstream web UI, captive-portal WiFi setup, OTA, Moonraker client, lease/heartbeat
safety model, drying mode, and the paxx12 U1 Extended Firmware integration, plus
the local bed-probe AUTO trigger and the DC blower / WS2812 / 100K NTC hardware.

## Build

Requires ESP-IDF **v5.3.2 or newer** (CI uses v5.3.5). From `firmware/dragonbreath/`:

```bash
. ~/esp/esp-idf/export.sh
idf.py -B build-u1breath \
  -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.u1breath" build
```

The board is selected by `sdkconfig.u1breath` (`CONFIG_PB_BOARD_U1BREATH=y`). A
plain `idf.py build` still produces the stock Panda Breath image; never flash that
one onto a U1 Breath board.

Optional: copy `main/dev_config.h.example` to `main/dev_config.h` with your WiFi
SSID/password and the printer's Moonraker IP to seed them at first boot. Otherwise
the device starts a `DragonBreath-xxxx` access point and you set them in the portal.

## Flash

The XIAO ESP32-C3's own USB-C port is the flashing and console port (native USB
Serial/JTAG). Hold BOOT while plugging in only if the chip refuses to enter the
bootloader on its own.

```bash
idf.py -B build-u1breath -p /dev/ttyACM0 flash monitor
```

Later updates: use the web UI's firmware update page with
`build-u1breath/dragonbreath.bin` (OTA with automatic rollback if the new image
does not come up healthy).

## First boot

1. Join the `DragonBreath-xxxx` AP, open `http://192.168.4.1`, enter WiFi and the
   printer's Moonraker address. Control source: **Klipper**.
2. Give the unit a **static DHCP lease** on your router. The paxx12 integration
   needs a stable IP.
3. Open `http://<unit-ip>/`. Settings to check on a U1 Breath:

| Setting | Default | Meaning |
|---|---|---|
| `probe_auto` | on | AUTO may heat from the bed probe |
| `probe_on` | 90 C | bed probe at or above this engages heat (in AUTO) |
| `probe_off` | 70 C | bed probe below this releases heat (at least 5 C under `probe_on`) |
| `filter_auto` / `filter_temp` | on / 45 C | blower-only filtration when the bed (probe or printer setpoint) reaches this |
| `max` | 70 C | chamber set-point ceiling (absolute firmware cap, not raisable) |
| `fb_cut` | auto (102 C) | duct-sensor soft foldback; set from bring-up measurements, see `docs/bringup.md` |

The status pixel: dim white idle, green AUTO (slow blink = waiting, solid = heating),
amber manual, blue drying, red blinking = fault latched (clear it from the web UI
or from Klipper with `DRAGONBREATH_RESET`).

BOOT button: tap = arm AUTO / master OFF, hold 2 s = panic-off (latches a fault),
hold 10 s = factory reset (erases WiFi and settings, reboots to the setup AP).

## Modes

- **OFF**: nothing runs except the filtration band and residual-heat purge.
- **AUTO**: heats to the AUTO card target when either the printer reports a filament
  zone through Moonraker (upstream behaviour, blocked while the paxx12 helper is
  installed) or the local bed probe passes `probe_on`. Releases when the probe drops
  below `probe_off`.
- **POWER_ON**: a manual or Klipper-commanded target with a heartbeat lease. Klipper's
  `M141 S0` at the end of a print returns the unit to AUTO if AUTO was armed before.
- **DRYING**: hold a target for N hours (spools on the bed, printer idle).
- **Filter**: blower only, from the web UI, Klipper's `SET_PIN PIN=dragonbreath_filter`,
  or automatically from the filtration band.

## Tests

```bash
cd firmware/dragonbreath
for t in tests/run_*.sh; do sh "$t"; done
```

`tests/run_probe_host_test.sh` compiles the real policy with the U1 Breath board
selected and checks the probe hysteresis, the filtration band, the Klipper OFF
restore, and the single-button mapping. The others are upstream's and must keep
passing in the Panda configuration.
