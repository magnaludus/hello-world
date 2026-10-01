# Upstream

`firmware/dragonbreath/` is a git subtree of
[plastikman/DragonBreath](https://github.com/plastikman/DragonBreath) (MIT),
squashed at commit `f311a22c39a3e3aef92d10f0f6c3f2d5d63e02b9` (release v1.1.19,
2026-09-23). Its shared services come from
[justinh-rahb/dragon-core](https://github.com/justinh-rahb/dragon-core) v0.35.2
through the ESP-IDF component manager (see `main/idf_component.yml`).

## What this fork changes

Everything U1 Breath-specific is behind the `CONFIG_PB_BOARD_U1BREATH` Kconfig
choice (`components/pb_board/Kconfig`), so the stock Panda Breath build is
unchanged:

| Area | Panda Breath (upstream) | U1 Breath |
|---|---|---|
| Heater SSR | GPIO18 | GPIO6 |
| Fan | 220 V blower, TRIAC on GPIO3, ZCD GPIO7 | 24 V DC blower, LEDC PWM on GPIO7 (`pb_fan_pwm.c`) |
| NTCs | 2, stock R/T table, 82k/33k strap | 3 x 100K/3950 Beta model, fixed 100k (chamber GPIO2, duct GPIO3, bed probe GPIO4) |
| LEDs | 4 panel LEDs | 1 WS2812 on GPIO10 (`pb_leds_ws2812.c`) |
| Buttons | 4 | XIAO BOOT on GPIO9 (short: AUTO/OFF toggle, 2 s: panic-off, 5 s: factory reset) |
| AUTO | printer filament zone via Moonraker | plus a local bed-probe trigger with hysteresis |
| Console | UART0 on GPIO21/20 | native USB Serial/JTAG |
| Extra component | none | `components/led_strip` vendored from idf-extra-components (Apache-2.0) |

## Pulling upstream

```bash
git subtree pull --prefix=firmware/dragonbreath https://github.com/plastikman/DragonBreath.git main --squash
```

Resolve conflicts in the files listed above; everything else should merge clean.
