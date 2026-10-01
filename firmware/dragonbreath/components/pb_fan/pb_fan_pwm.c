// SPDX-License-Identifier: MIT
// pb_fan — U1 Breath backend: a 24 V DC centrifugal blower driven low-side by a
// logic-level MOSFET with LEDC PWM at 25 kHz. There is no TRIAC and no mains on
// the fan path, so, unlike the Panda backend, the drive is a real duty cycle.
//
// Below PB_FAN_MIN_PERCENT a 7530 blower may not reliably start, so any non-zero
// request is floored there. 0 is always fully off.
#include "pb_fan.h"
#include "pb_board.h"

#include "esp_log.h"
#include <stdatomic.h>
#include <stdbool.h>

#ifndef CONFIG_PB_DEVBOARD_SAFE
#include "driver/ledc.h"
#endif

static const char *TAG = "pb_fan";

#define FAN_PWM_FREQ_HZ      25000
#define FAN_PWM_RESOLUTION   LEDC_TIMER_10_BIT
#define FAN_PWM_MAX_DUTY     1023U
#define FAN_LEDC_MODE        LEDC_LOW_SPEED_MODE
#define FAN_LEDC_TIMER       LEDC_TIMER_0
#define FAN_LEDC_CHANNEL     LEDC_CHANNEL_0

static _Atomic uint8_t s_percent;    // last requested level (0..100)
static bool            s_ready;

static uint8_t effective_percent(uint8_t percent)
{
    if (percent == 0) return 0;
    if (percent > 100) return 100;
    if (percent < PB_FAN_MIN_PERCENT) return PB_FAN_MIN_PERCENT;
    return percent;
}

esp_err_t pb_fan_init(void)
{
    atomic_store(&s_percent, 0);
#ifdef CONFIG_PB_DEVBOARD_SAFE
    s_ready = true;
    ESP_LOGW(TAG, "safe dev-board backend: fan PWM GPIO compiled out");
    return ESP_OK;
#else
    const ledc_timer_config_t timer = {
        .speed_mode      = FAN_LEDC_MODE,
        .duty_resolution = FAN_PWM_RESOLUTION,
        .timer_num       = FAN_LEDC_TIMER,
        .freq_hz         = FAN_PWM_FREQ_HZ,
        .clk_cfg         = LEDC_AUTO_CLK,
    };
    esp_err_t err = ledc_timer_config(&timer);
    if (err != ESP_OK) return err;

    const ledc_channel_config_t channel = {
        .gpio_num   = PB_GPIO_FAN_PWM,
        .speed_mode = FAN_LEDC_MODE,
        .channel    = FAN_LEDC_CHANNEL,
        .intr_type  = LEDC_INTR_DISABLE,
        .timer_sel  = FAN_LEDC_TIMER,
        .duty       = 0,                       // idle off
        .hpoint     = 0,
    };
    err = ledc_channel_config(&channel);
    if (err != ESP_OK) return err;

    s_ready = true;
    ESP_LOGI(TAG, "init: DC blower PWM on GPIO%d, %d Hz, floor %d%%",
             PB_GPIO_FAN_PWM, FAN_PWM_FREQ_HZ, PB_FAN_MIN_PERCENT);
    return ESP_OK;
#endif
}

void pb_fan_set_level(uint8_t percent)
{
    if (percent > 100) percent = 100;
    atomic_store(&s_percent, percent);
    uint8_t eff = effective_percent(percent);
#ifdef CONFIG_PB_DEVBOARD_SAFE
    (void)eff;
#else
    if (!s_ready) return;
    uint32_t duty = (uint32_t)eff * FAN_PWM_MAX_DUTY / 100U;
    ledc_set_duty(FAN_LEDC_MODE, FAN_LEDC_CHANNEL, duty);
    ledc_update_duty(FAN_LEDC_MODE, FAN_LEDC_CHANNEL);
#endif
}

uint8_t pb_fan_get_level(void) { return atomic_load(&s_percent); }

// No zero-cross detector on a DC fan: report "no edges" so diagnostics show a
// clean zero rather than a stale number.
void pb_fan_zc_diag(uint32_t *count_out, uint32_t *interval_us_out,
                    uint32_t *rejected_count_out)
{
    if (count_out) *count_out = 0;
    if (interval_us_out) *interval_us_out = 0;
    if (rejected_count_out) *rejected_count_out = 0;
}

#ifdef CONFIG_PB_DEVBOARD_SAFE
void pb_fan_hil_zero_cross(uint32_t count, uint32_t interval_us)
{
    (void)count;
    (void)interval_us;
}
#endif
