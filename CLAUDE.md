# Working in this repo (U1 Breath)

Keep sessions cheap. This project has a long firmware tree and slow builds; most
of the cost comes from re-reading large things and from idle wakes.

## Cost rules

- Use `model: "haiku"` for mechanical worker agents (doc edits, log triage, file
  moves, CAD re-exports) and `model: "sonnet"` for ordinary code changes. Reserve
  the session's default model for firmware safety logic and design decisions.
- Do not subscribe to PR activity unless the user asks. CI runs on `pull_request`
  only; check results with one `get_check_runs` call when needed.
- Never read a whole CI log. Pull it to a file and grep for `error:` / `FAILED`.
- Never cat upstream firmware files wholesale. `firmware/dragonbreath/` is a vendored
  subtree (`firmware/UPSTREAM.md` lists exactly what this fork changes); grep for the
  symbol you need and read 50 lines around it.
- One validated push per round. Build locally before pushing; a failing CI run
  emails the owner twice.

## Build facts (save the rediscovery)

- Firmware host tests: `cd firmware/dragonbreath && for t in tests/run_*.sh; do sh $t; done`
  (seconds, no toolchain). `tests/run_probe_host_test.sh` is the U1 Breath one.
- ESP-IDF v5.3.5. U1 Breath image:
  `idf.py -B build-u1breath -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.u1breath" build`.
  Plain `idf.py build` is the stock Panda image; never flash it to a U1 Breath board.
- In the cloud container the Espressif package mirror and component registry are
  blocked. Offline recipe: `IDF_PYTHON_CHECK_CONSTRAINTS=no ./install.sh esp32c3`,
  then build with `IDF_COMPONENT_MANAGER=0` and
  `-DEXTRA_COMPONENT_DIRS="<dragon-core clone>/components-subset;<dir with esp_websocket_client and mdns from espressif/esp-protocols>"`.
  Only the dc_* components named in `main/idf_component.yml` go in the subset
  (dc_lighting needs an older led_strip and must be excluded). `led_strip` itself is
  vendored in `components/led_strip`.
- ESP-IDF resolves `REQUIRES`/`PRIV_REQUIRES` before sdkconfig exists: never gate a
  requirement on `CONFIG_*`; gate only `SRCS`.
- CAD: `python cad/build.py` (about 65 s) and `python -m pytest cad/tests -q`
  (about 30 s). Dimensions live in `cad/u1breath/params.py`.

## Conventions

- Commits: plain imperative subject, body explains why. No model names in commits,
  PR text, or code comments.
- Docs are the deliverable for the owner: keep `docs/measurements.md` and
  `docs/bringup.md` in sync with any CAD or firmware behaviour change.
