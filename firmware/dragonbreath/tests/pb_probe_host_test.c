// SPDX-License-Identifier: MIT
// U1 Breath bed-probe AUTO: host test. Reuses the upstream pb_policy host-test
// fixture (stubs, fake NVS, fake heater) by including it with its main() renamed,
// and is compiled with CONFIG_PB_BOARD_U1BREATH so the board defaults apply.
#define main upstream_policy_main
#include "pb_policy_host_test.c"
#undef main

static void test_probe_decide_hysteresis(void)
{
    CHECK(pb_probe_decide(true, 95.0f, 90.0f, 70.0f, false) == true);    // reaches on
    CHECK(pb_probe_decide(true, 80.0f, 90.0f, 70.0f, true)  == true);    // inside band, holds
    CHECK(pb_probe_decide(true, 80.0f, 90.0f, 70.0f, false) == false);   // inside band, holds
    CHECK(pb_probe_decide(true, 69.9f, 90.0f, 70.0f, true)  == false);   // drops below off
    CHECK(pb_probe_decide(false, 95.0f, 90.0f, 70.0f, false) == false);  // dead probe never starts
    CHECK(pb_probe_decide(false, 95.0f, 90.0f, 70.0f, true)  == true);   // dead probe holds
    CHECK(pb_probe_decide(true, NAN, 90.0f, 70.0f, true) == true);       // NaN == not readable
}

static void test_u1_defaults(void)
{
    reset_fixture();
    pb_policy_snapshot_t snap = snapshot();
    CHECK(snap.params.probe_auto_enable);
    CHECK(snap.params.probe_on_c == 90.0f);
    CHECK(snap.params.probe_off_c == 70.0f);
    CHECK(snap.params.filter_auto_enable);
    CHECK(snap.params.filter_temp_c == 45.0f);
    CHECK(snap.mode == PB_MODE_OFF);
    CHECK(!snap.probe_heat);
}

// AUTO armed, no printer link at all: the probe alone starts and stops heat.
static void test_probe_drives_auto_without_printer(void)
{
    reset_fixture();
    CHECK(pb_policy_set_auto(60.0f, 100.0f, DB_SOURCE_WEB, 1) == PB_POLICY_OK);
    pb_policy_set_env(0.0f, 0.0f, false, 0.0f, NAN);

    bed_probe_c = 85.0f;                       // below on
    pb_policy_tick();
    pb_policy_snapshot_t snap = snapshot();
    CHECK(snap.mode == PB_MODE_AUTO);
    CHECK(!snap.auto_engaged);
    CHECK(heater_target == 0.0f);

    bed_probe_c = 91.0f;                       // reaches on
    unsigned pets = heater_link_pets;
    pb_policy_tick();
    snap = snapshot();
    CHECK(snap.auto_engaged);
    CHECK(snap.probe_heat);
    CHECK(heater_target == 60.0f);             // the AUTO card target
    CHECK(heater_link_pets > pets);            // autonomous heat feeds the comms deadman
    CHECK(fan_level == 100);                   // heat airflow

    bed_probe_c = 75.0f;                       // inside the band: still heating
    pb_policy_tick();
    snap = snapshot();
    CHECK(snap.auto_engaged);

    bed_probe_c = 69.0f;                       // below off: releases
    pb_policy_tick();
    snap = snapshot();
    CHECK(!snap.auto_engaged);
    CHECK(!snap.probe_heat);
    CHECK(heater_target == 0.0f);
}

// The Klipper helper blocks the Moonraker-fed AUTO but not the physical probe.
static void test_probe_not_blocked_by_klipper_helper(void)
{
    reset_fixture();
    CHECK(pb_policy_set_auto(55.0f, 100.0f, DB_SOURCE_WEB, 1) == PB_POLICY_OK);
    pb_policy_set_env(100.0f, 100.0f, true, 60.0f, NAN);   // zone says 60
    pb_policy_set_klipper_helper(true);
    bed_probe_c = 25.0f;
    pb_policy_tick();
    CHECK(!snapshot().auto_engaged);                        // zone path blocked by helper
    bed_probe_c = 95.0f;
    pb_policy_tick();
    pb_policy_snapshot_t snap = snapshot();
    CHECK(snap.auto_engaged);
    CHECK(heater_target == 55.0f);                          // probe path: AUTO card target
}

// A reported filament zone is more specific than the AUTO card: it wins.
static void test_zone_target_wins_over_probe_target(void)
{
    reset_fixture();
    CHECK(pb_policy_set_auto(55.0f, 100.0f, DB_SOURCE_WEB, 1) == PB_POLICY_OK);
    pb_policy_set_env(100.0f, 100.0f, true, 62.0f, NAN);
    pb_policy_set_klipper_helper(false);
    bed_probe_c = 95.0f;
    pb_policy_tick();
    CHECK(snapshot().auto_engaged);
    CHECK(heater_target == 62.0f);
}

// Filtration band from the probe alone, in OFF mode, with hysteresis.
static void test_probe_filtration_band(void)
{
    reset_fixture();
    pb_policy_set_env(0.0f, 0.0f, false, 0.0f, NAN);
    bed_probe_c = 40.0f;
    pb_policy_tick();
    CHECK(!snapshot().auto_filtering);
    CHECK(fan_level == 0);
    bed_probe_c = 46.0f;                       // >= 45
    pb_policy_tick();
    CHECK(snapshot().auto_filtering);
    CHECK(fan_level == 100);
    CHECK(heater_target == 0.0f);              // fan only, never heat
    bed_probe_c = 43.0f;                       // inside hysteresis (45 - 3)
    pb_policy_tick();
    CHECK(snapshot().auto_filtering);
    bed_probe_c = 41.0f;
    pb_policy_tick();
    CHECK(!snapshot().auto_filtering);
    CHECK(fan_level == 0);
}

// A dead probe never starts anything, and the disable switch is honoured.
static void test_probe_fault_and_disable(void)
{
    reset_fixture();
    CHECK(pb_policy_set_auto(60.0f, 100.0f, DB_SOURCE_WEB, 1) == PB_POLICY_OK);
    pb_policy_set_env(0.0f, 0.0f, false, 0.0f, NAN);
    bed_probe_status = PB_NTC_OPEN;
    bed_probe_c = 95.0f;
    pb_policy_tick();
    CHECK(!snapshot().auto_engaged);
    CHECK(!snapshot().auto_filtering);

    bed_probe_status = PB_NTC_OK;
    CHECK(pb_policy_set_probe_config(false, 90.0f, 70.0f) == PB_POLICY_OK);
    pb_policy_tick();
    CHECK(!snapshot().auto_engaged);
    CHECK(!snapshot().auto_filtering);
}

static void test_probe_config_validation_and_persistence(void)
{
    reset_fixture();
    CHECK(pb_policy_set_probe_config(true, 85.0f, 83.0f) == PB_POLICY_INVALID);   // gap < 5
    CHECK(pb_policy_set_probe_config(true, 40.0f, 30.0f) == PB_POLICY_INVALID);   // on too low
    CHECK(pb_policy_set_probe_config(true, 130.0f, 70.0f) == PB_POLICY_INVALID);  // on too high
    CHECK(pb_policy_set_probe_config(true, 85.0f, 60.0f) == PB_POLICY_OK);
    CHECK(pb_policy_persist_pending());
    CHECK(nvs_read("md_prb_on") == 8500);
    CHECK(nvs_read("md_prb_off") == 6000);
    CHECK(nvs_read("md_prb_en") == 1);

    // Reboot: params come back, mode does not.
    CHECK(pb_policy_init() == ESP_OK);
    pb_policy_load_params();
    pb_policy_snapshot_t snap = snapshot();
    CHECK(snap.params.probe_on_c == 85.0f);
    CHECK(snap.params.probe_off_c == 60.0f);
    CHECK(snap.mode == PB_MODE_OFF);
}

// Klipper's M141 S0 at print end returns to a local AUTO session; web OFF does not.
static void test_klipper_off_restores_local_auto(void)
{
    reset_fixture();
    CHECK(pb_policy_set_auto(60.0f, 100.0f, DB_SOURCE_WEB, 1) == PB_POLICY_OK);
    uint32_t rev = snapshot().state_revision;
    pb_policy_lease_t lease;
    CHECK(pb_policy_set_power_on(50.0f, DB_SOURCE_KLIPPER, "u1-klippy", rev, &lease) == PB_POLICY_OK);
    CHECK(snapshot().mode == PB_MODE_POWER_ON);
    pb_policy_set_mode_off(DB_SOURCE_KLIPPER);
    pb_policy_snapshot_t snap = snapshot();
    CHECK(snap.mode == PB_MODE_AUTO);
    CHECK(!snap.auto_engaged);
    CHECK(heater_target == 0.0f);

    rev = snap.state_revision;
    CHECK(pb_policy_set_power_on(50.0f, DB_SOURCE_KLIPPER, "u1-klippy", rev, &lease) == PB_POLICY_OK);
    pb_policy_set_mode_off(DB_SOURCE_WEB);
    CHECK(snapshot().mode == PB_MODE_OFF);
}

// Single BOOT button: tap while OFF arms AUTO, tap again is master OFF.
static void test_single_button_toggles_auto(void)
{
    reset_fixture();
    pb_policy_on_button(PB_BUTTON_POWER, PB_BUTTON_SHORT);
    CHECK(snapshot().mode == PB_MODE_AUTO);
    pb_policy_on_button(PB_BUTTON_POWER, PB_BUTTON_SHORT);
    CHECK(snapshot().mode == PB_MODE_OFF);
    pb_policy_on_button(PB_BUTTON_POWER, PB_BUTTON_LONG);   // panic-off latches a fault
    CHECK(snapshot().fault_latched);
}

int main(void)
{
    test_probe_decide_hysteresis();
    test_u1_defaults();
    test_probe_drives_auto_without_printer();
    test_probe_not_blocked_by_klipper_helper();
    test_zone_target_wins_over_probe_target();
    test_probe_filtration_band();
    test_probe_fault_and_disable();
    test_probe_config_validation_and_persistence();
    test_klipper_off_restores_local_auto();
    test_single_button_toggles_auto();
    puts("pb_probe (U1 Breath) host tests: PASS");
    return 0;
}
