# Bring-up

Do this in order. Every step before "first heat" happens with the PTC unplugged
from the SSR.

## 0. Bench, no mains

1. Flash the firmware over the XIAO's USB-C (`firmware/README.md`). Open the serial
   monitor. Expect `board init: U1 Breath`, `pb_ntc init ok (Rref=100 kOhm)`,
   `pb_fan init: DC blower PWM on GPIO7`.
2. Power the XIAO from USB only. Plug in the three NTCs. Open the web UI calibration
   page (`/api/v2/calibration` or the Settings page): chamber, ptc and bed should
   read room temperature within a degree or two. Warm each one with a finger and
   watch it move. A reading of "open" means a swapped or broken divider.
3. Blower: from the web UI turn the filter on. It must spin at the 40 percent floor
   and at 100 percent. If it twitches but does not start, raise
   `PB_FAN_MIN_PERCENT` in `pb_board.h`.
4. LED: dim white idle, green when you arm AUTO, red blinking if you unplug a
   sensor while heating is armed.

## 1. Mains, heater still unplugged

1. Check continuity: PE pin of the plug to the liner, to the back plate if metal,
   and to nothing else. L and N to nothing on the chassis.
2. Plug into a GFCI outlet. The HLK should give 24.0 V, the buck 5.0 V. The XIAO
   boots on its own power and joins WiFi.
3. From the web UI set a manual target of 40 C. The SSR LED must light; a meter on
   the SSR output must show 120 V. Set target 0: it drops.

## 2. First heat

1. Plug the PTC in. Blower on, then target 45 C. The duct sensor should climb
   within 30 s. Watch for: smell of hot plastic (stop), the shell near the liner
   getting too hot to touch (stop), the fault LED.
2. Let it run to the target with the chamber open, then closed with the tote on.
   Log `sensors.ptc.temperature_c` at steady state with the chamber at 60 C.

## 3. Set the duct foldback

The upstream firmware trips a latching fault at 105 C on the duct sensor and folds
power back (soft cut) at `fb_cut`, default 102 C. Your duct sensor sits on the liner
wall, not on the Panda's element, so:

- If the steady-state duct reading is **below 85 C**: leave `fb_cut` at auto.
- If it is **85 to 95 C**: set `fb_cut` to about 8 C above the reading (web UI
  Settings, or `POST /settings?fb_cut=98`). The foldback then only acts when the
  blower stalls or a filter clogs, which is what it is for.
- If it is **above 95 C**: move the ring-lug NTC 20 mm further toward the outlet
  end of the liner (cooler), or add the second liner screw as a thermal path to
  the back plate. Do not raise the hard cutoff in firmware.

Confirm the blower-failure trip once: unplug the blower with the heater at 60 C.
The duct reading must climb and the unit must latch a fault (red blinking, heater
off) before the shell gets hot. Clear with the web UI or `DRAGONBREATH_RESET`.

## 4. Bed probe

1. Stick the probe under the bed plate (`measurements.md`). Heat the bed to 60 C
   from the printer; the `bed` sensor should follow within a few degrees and a
   minute of lag. Use the calibration offset (max 5 C) to trim it.
2. Arm AUTO. Set the bed to 100 C: the unit must engage at 90 C on the probe and
   heat to the AUTO target. Drop the bed to 50 C: it must release once the probe
   reads below 70 C and keep the blower on until the duct cools.
3. Set the bed to 55 C: no heat, but the blower runs (filtration band at 45 C).

## 5. Klipper

1. Static DHCP lease for the unit. Enable DragonBreath in the printer's Firmware
   Config with that IP (`klipper/README.md`).
2. In the printer console: `M141 S50`. The unit's web UI shows mode POWER_ON, owner
   `klipper`, and a lease countdown that keeps resetting. `M141 S0`: the unit
   returns to AUTO (if armed) or OFF.
3. Print an ABS calibration cube with `M191 S55` in the start G-code. Watch the
   U1's host temperature in Fluidd; if the mainboard passes 75 C, improve the
   mainboard cooling before longer prints.

## 6. Ongoing

- Carbon: swap when the smell returns (typically 100 to 150 h of ABS).
- HEPA: when the blower note rises or airflow at the outlet drops noticeably.
- Thermal fuse: if it ever opens, find the cause (blower, clogged filter, SSR
  failed shorted) before replacing it.
