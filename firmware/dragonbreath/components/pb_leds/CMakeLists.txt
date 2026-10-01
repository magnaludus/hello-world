# Board-selected backend: the Panda's four GPIO panel LEDs, or the U1 Breath
# single WS2812 status pixel. Both implement the same pb_leds.h API.
#
# NOTE: ESP-IDF resolves REQUIRES/PRIV_REQUIRES in an early pass BEFORE sdkconfig
# is loaded, so the requirement list must not depend on CONFIG_*. Only SRCS may.
# led_strip is vendored in components/led_strip and is harmless to require on the
# Panda build (nothing there includes it).
if(CONFIG_PB_BOARD_U1BREATH)
    set(PB_LEDS_SRCS "pb_leds_ws2812.c")
else()
    set(PB_LEDS_SRCS "pb_leds.c")
endif()

idf_component_register(
    SRCS ${PB_LEDS_SRCS}
    INCLUDE_DIRS "include"
    REQUIRES pb_board driver nvs_flash
    PRIV_REQUIRES led_strip
)
