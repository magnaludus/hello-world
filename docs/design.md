# Design

## What it is

A Panda Breath class unit for the Snapmaker U1: 300 W PTC chamber heater, HEPA +
activated-carbon filtration, its own 120 V supply, WiFi, and a bed probe that lets it
run with no printer connection at all. It fits the Panda Breath envelope
(273 x 175 x 55 mm) and mounts inside the chamber on the rear wall.

The firmware speaks the DragonBreath REST API, which the paxx12 U1 Extended Firmware
already drives as a Klipper `heater_generic`. That decision removed the biggest
chunk of custom work (a Klipper module and a web UI) and bought a proven safety model.

## Layout

Air moves bottom to top. Y = 0 is the back face on the rear wall, +Y faces the chamber.

```
 Z 273 ┌──────────────────────────────────┐
       │  HEATER  ░ 300 W PTC in Al liner ░ │  outlet slots in the liner flange,
       │          blower plenum behind     │  air through the fins toward +Y
 Z 195 ├──────────────────┬───────────────┤
       │  7530 BLOWER     │  ELECTRONICS  │  blower inlet faces +Y inside a sealed
       │  outlet points +Z│  under cover  │  cavity fed from the filter plenum
 Z 110 ├──────────────────┴───────────────┤
       │  BAY 1 80x80     │  BAY 2 80x80  │  grille > carbon cartridge > 2 HEPA cells
       │  carbon | HEPA   │  carbon | HEPA│  > 12 mm plenum, both bays merge upward
 Z 0   └──────────────────────────────────┘
        X 0                            X 172
```

### Depth budget (the tight axis, limit 55 mm)

| Section | Stack (mm) | Total |
|---|---|---|
| Filter bay | back 3 + plenum 12 + HEPA 15 + carbon 15 + grille 3 | 48 |
| Blower / electronics | back 3 + blower 30 + inlet gap 12 + cover 3 | 48 |
| Heater | back 3 + gap 8 + liner 1 + plenum 8 + element 32 + flange 1 | 53 |

The heater section sets the depth. A 300 W element deeper than 34 mm does not fit;
put the real element dimensions in `cad/u1breath/params.py` and the envelope test
will tell you.

### Why four HEPA cells

HEPA media is restrictive and a 30 mm blower has limited static pressure. Two bays
of two 80 x 40 cells give 128 cm2 of face area, so face velocity at 15 CFM is about
0.55 m/s, which a 7530 blower can push through H11/H13 media. Two cells would need
twice the velocity and a bigger, deeper fan. You have a dozen cells, so spares are free.

### Carbon

Pellet carbon sits in a printed 80 x 80 x 15 mesh cartridge upstream of the HEPA, so
any carbon fines end in the HEPA, not the chamber. About 60 g per cartridge. Change
cartridges every 100 to 150 print hours of ABS/ASA, or when the smell comes back.

## Thermal estimate

Chamber volume of the U1 is roughly 55 L. With the Sterilite tote cover the enclosure
is a thin, leaky box; a workable loss model is UA of about 4 to 5 W/K (cover and
front door glass dominate). At 300 W net and 22 C ambient:

| Loss UA | Steady-state rise | Chamber |
|---|---|---|
| 4 W/K | 75 K (capped by the 70 C setpoint) | 60 C target reached |
| 6 W/K | 50 K | 60 C target reached, slow |
| 8 W/K | 37 K | about 55 C |

The heated bed adds 100 to 150 W of its own at ABS temperatures, which is why the
U1 reaches 50 C passively with the official cover. Expect 60 C in 15 to 25 minutes
with the tote sealed reasonably (foam tape on the tote lip helps more than anything
else). The PTC self-limits: as the air warms its power drops, so the 300 W is a
cold-start number, not a continuous draw.

## Electrical

See `wiring.md` and `wiring.svg`. Summary:

- 120 V: cord > PG7 grip > terminal block > 5 A slow-blow fuse > 10 A zero-cross SSR >
  130 C thermal fuse (on the liner) > 150 C protector (bundled with the element) >
  PTC > neutral. PE bonded to the liner.
- 24 V from an HLK-10M24 runs the blower through a logic-level MOSFET at 25 kHz PWM.
- 5 V from a mini buck runs the XIAO ESP32-C3 and the WS2812.
- Three 100K/3950 NTCs in 100k dividers on the XIAO's three ADC1 pins.

## Firmware

`firmware/dragonbreath` is upstream DragonBreath with a `u1breath` board profile
(`firmware/UPSTREAM.md` lists every difference). Behaviour that matters to the build:

- **Safety layers kept from upstream**: duct sensor hard cutoff 105 C (latching, survives
  reboot), chamber cutoff 85 C, 70 C setpoint cap, fail-closed on any sensor fault
  while heating, comms-loss watchdog (default 5 min) for Klipper/web sessions,
  element foldback (soft cut below the hard trip), fan runs whenever heat runs and
  purges residual heat afterwards.
- **Bed-probe AUTO**: in AUTO mode the probe engages heat at `probe_on` (90 C) and
  releases below `probe_off` (70 C). A dead probe never starts heat. The probe also
  feeds the filtration band (`filter_temp`, 45 C), which runs the blower alone.
- **Klipper**: `M141`/`M191` take over with a heartbeat lease. `M141 S0` hands the
  unit back to AUTO if AUTO was armed, so a print without chamber G-code still
  gets heat from the probe.

## Mechanical and materials

- Shell in ASA or ABS. Nothing printed touches air above about 70 C: the heater
  section has a folded 1 mm aluminum liner with an 8 mm air gap to the shell, and the
  outlet slots are cut in the liner's own flange.
- M3 heat-set inserts in bosses; M2 inserts on the carbon cartridge lids.
- 3 mm silicone foam tape seals the filter grille, the liner flange, and the
  back plate to the rear wall so the blower pulls through the filters, not around them.
- Back plate hole pattern is parametric (`MOUNT_HOLES`) because the U1 rear wall
  has not been measured yet; see `measurements.md`.

## Known compromises

- Every electronic part lives at chamber temperature (60 to 65 C). All are rated
  70 C or better and the SSR is 4x oversized. A through-wall mount would avoid this,
  but you chose inside-chamber for a no-drill install.
- The duct NTC reads the liner wall, not the PTC ceramic. The upstream cutoffs were
  tuned for the Panda's element sensor, so bring-up includes measuring the liner
  temperature and placing the sensor where it reads 80 to 95 C at steady state.
- The Sterilite cover is less sealed than the official Top Cover. If the chamber
  stalls in the low 50s, seal the tote lip before blaming the heater.
