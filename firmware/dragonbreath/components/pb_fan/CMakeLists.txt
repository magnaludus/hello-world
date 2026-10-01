# Board-selected backend: the Panda's AC TRIAC held-gate driver, or the U1 Breath
# DC blower PWM driver. Both implement the same pb_fan.h API.
if(CONFIG_PB_BOARD_U1BREATH)
    set(PB_FAN_SRCS "pb_fan_pwm.c" "pb_fan_zc_filter.c")
else()
    set(PB_FAN_SRCS "pb_fan.c" "pb_fan_zc_filter.c")
endif()

idf_component_register(
    SRCS ${PB_FAN_SRCS}
    INCLUDE_DIRS "include"
    REQUIRES pb_board driver esp_timer
)
