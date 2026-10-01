# Board-selected backend: the Panda's four GPIO panel LEDs, or the U1 Breath
# single WS2812 status pixel. Both implement the same pb_leds.h API.
if(CONFIG_PB_BOARD_U1BREATH)
    set(PB_LEDS_SRCS "pb_leds_ws2812.c")
    set(PB_LEDS_PRIV_REQUIRES led_strip)
else()
    set(PB_LEDS_SRCS "pb_leds.c")
    set(PB_LEDS_PRIV_REQUIRES "")
endif()

idf_component_register(
    SRCS ${PB_LEDS_SRCS}
    INCLUDE_DIRS "include"
    REQUIRES pb_board driver nvs_flash
    PRIV_REQUIRES ${PB_LEDS_PRIV_REQUIRES}
)
