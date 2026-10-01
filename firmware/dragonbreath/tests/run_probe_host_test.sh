#!/bin/sh
# U1 Breath bed-probe policy test: the upstream pb_policy fixture compiled with
# the U1 Breath board selected.
set -eu

root="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
out="${TMPDIR:-/tmp}/dragonbreath-pb-probe-test"

cc -std=c11 -Wall -Wextra -Werror -DCONFIG_PB_BOARD_U1BREATH=1 \
  -I"$root/tests/stubs" \
  -I"$root/tests" \
  -I"$root/components/pb_policy/include" \
  -I"$root/components/pb_buttons/include" \
  "$root/components/pb_policy/pb_policy.c" \
  "$root/tests/pb_probe_host_test.c" \
  -lm -o "$out"

"$out"
