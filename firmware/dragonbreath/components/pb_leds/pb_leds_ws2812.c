// SPDX-License-Identifier: MIT
// pb_leds — U1 Breath backend: ONE WS2812 status pixel stands in for the Panda's
// four panel LEDs. pb_policy keeps driving the same four logical LEDs (Power /
// On / Auto / Dry) with the same patterns; this backend folds them into a single
// colour each 50 ms tick:
//
//   fault (Power blinking)          red, blinking
//   drying                          blue
//   manual POWER_ON                 amber
//   AUTO engaged / AUTO waiting     green solid / green slow blink
//   idle, device alive              dim white
//   master-enable off               dark
#include "pb_leds.h"

#include <stdatomic.h>

#include "pb_board.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "nvs.h"

#ifndef CONFIG_PB_DEVBOARD_SAFE
#include "led_strip.h"
#endif

static const char *TAG = "pb_leds";

#define NVS_NS            "app_nvs"
#define KEY_LEDS_ENABLED  "leds_enabled"   // u32: 0 = off, nonzero = on

static _Atomic bool s_enabled = true;

#define TICK_MS           50
#define BLINK_TICKS        4    // 200 ms half-period  (~2.5 Hz)
#define BLINK_SLOW_TICKS  10    // 500 ms half-period  (~1 Hz)
#define CODE_ON_TICKS      3
#define CODE_OFF_TICKS     3
#define CODE_GAP_TICKS    16

#define PB_LED_BRIGHTNESS 48    // 0..255 — a status pixel, not a work light

static _Atomic pb_led_pattern_t s_pat[PB_LED_COUNT];
static _Atomic unsigned         s_code[PB_LED_COUNT];
static TaskHandle_t             s_task;

#ifndef CONFIG_PB_DEVBOARD_SAFE
static led_strip_handle_t s_strip;
#endif

typedef struct { uint8_t r, g, b; } rgb_t;
typedef struct { unsigned pulse; unsigned sub; } code_seq_t;   // CODE-pattern phase

static const rgb_t COLOR_FAULT  = { 255,   0,   0 };
static const rgb_t COLOR_DRY    = {   0,  60, 255 };
static const rgb_t COLOR_MANUAL = { 255, 120,   0 };
static const rgb_t COLOR_AUTO   = {   0, 255,  40 };
static const rgb_t COLOR_IDLE   = {  40,  40,  40 };

static void write_pixel(rgb_t c, bool on)
{
#ifndef CONFIG_PB_DEVBOARD_SAFE
    if (!s_strip) return;
    uint32_t k = on ? PB_LED_BRIGHTNESS : 0;
    led_strip_set_pixel(s_strip, 0, c.r * k / 255, c.g * k / 255, c.b * k / 255);
    led_strip_refresh(s_strip);
#else
    (void)c; (void)on;
#endif
}

// Evaluate one logical LED's pattern for this tick (same sequencing as the
// Panda backend, so the policy's indication semantics are unchanged).
static bool pattern_on(int i, uint32_t tick, code_seq_t *cs)
{
    pb_led_pattern_t p = atomic_load(&s_pat[i]);
    switch (p) {
    case PB_LED_SOLID:      return true;
    case PB_LED_BLINK:      return ((tick / BLINK_TICKS) & 1u) == 0;
    case PB_LED_BLINK_SLOW: return ((tick / BLINK_SLOW_TICKS) & 1u) == 0;
    case PB_LED_CODE: {
        unsigned n = atomic_load(&s_code[i]);
        bool on = false;
        if (n == 0) { cs->pulse = 0; cs->sub = 0; return false; }
        if (cs->pulse < n) {
            on = (cs->sub < CODE_ON_TICKS);
            if (++cs->sub >= CODE_ON_TICKS + CODE_OFF_TICKS) { cs->sub = 0; cs->pulse++; }
        } else {
            if (++cs->sub >= CODE_GAP_TICKS) { cs->sub = 0; cs->pulse = 0; }
        }
        return on;
    }
    case PB_LED_OFF:
    default:
        cs->pulse = 0; cs->sub = 0;
        return false;
    }
}

static void led_task(void *arg)
{
    (void)arg;
    uint32_t tick = 0;
    code_seq_t cs[PB_LED_COUNT] = {0};

    for (;;) {
        bool on[PB_LED_COUNT];
        for (int i = 0; i < PB_LED_COUNT; i++) on[i] = pattern_on(i, tick, &cs[i]);

        rgb_t color = COLOR_IDLE;
        bool lit = on[PB_LED_POWER];                      // "device alive" baseline
        if (atomic_load(&s_pat[PB_LED_POWER]) == PB_LED_BLINK) {
            color = COLOR_FAULT; lit = on[PB_LED_POWER];  // fault: red, blinking
        } else if (atomic_load(&s_pat[PB_LED_DRY]) != PB_LED_OFF) {
            color = COLOR_DRY; lit = on[PB_LED_DRY];
        } else if (atomic_load(&s_pat[PB_LED_ON]) != PB_LED_OFF) {
            color = COLOR_MANUAL; lit = on[PB_LED_ON];
        } else if (atomic_load(&s_pat[PB_LED_AUTO]) != PB_LED_OFF) {
            color = COLOR_AUTO; lit = on[PB_LED_AUTO];
        }
        if (!atomic_load(&s_enabled)) lit = false;
        write_pixel(color, lit);

        tick++;
        vTaskDelay(pdMS_TO_TICKS(TICK_MS));
    }
}

void pb_leds_flash_all(uint8_t times, uint16_t on_ms, uint16_t off_ms)
{
    if (s_task) vTaskSuspend(s_task);
    const rgb_t white = { 255, 255, 255 };
    for (uint8_t n = 0; n < times; n++) {
        write_pixel(white, true);
        vTaskDelay(pdMS_TO_TICKS(on_ms));
        write_pixel(white, false);
        vTaskDelay(pdMS_TO_TICKS(off_ms));
    }
}

esp_err_t pb_leds_start(void)
{
    if (s_task) return ESP_ERR_INVALID_STATE;

#ifndef CONFIG_PB_DEVBOARD_SAFE
    led_strip_config_t strip_cfg = {
        .strip_gpio_num = PB_GPIO_LED_WS2812,
        .max_leds = 1,
        .led_model = LED_MODEL_WS2812,
        .color_component_format = LED_STRIP_COLOR_COMPONENT_FMT_GRB,
        .flags = { .invert_out = false },
    };
    led_strip_rmt_config_t rmt_cfg = {
        .clk_src = RMT_CLK_SRC_DEFAULT,
        .resolution_hz = 10 * 1000 * 1000,
        .flags = { .with_dma = false },
    };
    esp_err_t err = led_strip_new_rmt_device(&strip_cfg, &rmt_cfg, &s_strip);
    if (err != ESP_OK) return err;
    led_strip_clear(s_strip);
#endif
    for (int i = 0; i < PB_LED_COUNT; i++) {
        atomic_store(&s_pat[i], PB_LED_OFF);
        atomic_store(&s_code[i], 0);
    }

    if (xTaskCreate(led_task, "pb_leds", 2560, NULL, 3, &s_task) != pdPASS) {
        s_task = NULL;
        return ESP_ERR_NO_MEM;
    }
#ifdef CONFIG_PB_DEVBOARD_SAFE
    ESP_LOGW(TAG, "safe dev-board backend: WS2812 output compiled out");
#else
    ESP_LOGI(TAG, "started: WS2812 status pixel on GPIO%d", PB_GPIO_LED_WS2812);
#endif
    return ESP_OK;
}

void pb_leds_set(pb_led_id_t id, pb_led_pattern_t pattern)
{
    if (id < 0 || id >= PB_LED_COUNT) return;
    atomic_store(&s_pat[id], pattern);
}

void pb_leds_set_code(pb_led_id_t id, uint8_t pulses)
{
    if (id < 0 || id >= PB_LED_COUNT) return;
    atomic_store(&s_code[id], pulses);
    atomic_store(&s_pat[id], PB_LED_CODE);
}

pb_led_pattern_t pb_leds_get(pb_led_id_t id)
{
    if (id < 0 || id >= PB_LED_COUNT) return PB_LED_OFF;
    return atomic_load(&s_pat[id]);
}

void pb_leds_load_config(void)
{
    bool enabled = true;
    nvs_handle_t h;
    if (nvs_open(NVS_NS, NVS_READONLY, &h) == ESP_OK) {
        uint32_t v;
        if (nvs_get_u32(h, KEY_LEDS_ENABLED, &v) == ESP_OK) enabled = (v != 0);
        nvs_close(h);
    }
    atomic_store(&s_enabled, enabled);
    ESP_LOGI(TAG, "status LED %s", enabled ? "enabled" : "disabled");
}

esp_err_t pb_leds_set_enabled(bool enabled)
{
    nvs_handle_t h;
    esp_err_t err = nvs_open(NVS_NS, NVS_READWRITE, &h);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "LED enable NOT saved: nvs_open %s", esp_err_to_name(err));
        return err;
    }
    err = nvs_set_u32(h, KEY_LEDS_ENABLED, enabled ? 1u : 0u);
    if (err == ESP_OK) err = nvs_commit(h);
    nvs_close(h);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "LED enable NOT saved: %s", esp_err_to_name(err));
        return err;
    }
    atomic_store(&s_enabled, enabled);
    ESP_LOGI(TAG, "status LED %s", enabled ? "enabled" : "disabled");
    return err;
}

bool pb_leds_get_enabled(void) { return atomic_load(&s_enabled); }
