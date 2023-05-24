import time

from pioneer_sdk import piosdk
from pioneer_sdk import camera

cam = camera.VideoStream()
cam.start()
pioneer_mini = piosdk.Pioneer()
time.sleep(0.5)


def led():
    h = pioneer_mini.get_dist_sensor_data()
    if h is not None:
        if h <= 0.2:
            pioneer_mini.led_control(r=255)
        elif 0.2 < h <= 0.55:
            pioneer_mini.led_control(r=255, g=255)
        elif 0.55 < h <= 1.2:
            pioneer_mini.led_control(g=255)
        else:
            pioneer_mini.led_control(b=255)


def go_led(x, y, z, yaw):
    pioneer_mini.go_to_local_point(x, y, z, yaw)
    while not pioneer_mini.point_reached():
        led()


points = [
    [0, 0, 1, 0],
    [0.5, -0.3, 1.5, 3.14],
    [1, 0, 2, 3.14],
    [1, 1, 2, 0],
    [0.5, 1.3, 1.5, 3.14],
    [0, 1, 1, 3.14],
    [0, 0, 1, 0],
]
led()
pioneer_mini.arm()
pioneer_mini.takeoff()
time.sleep(2)
for p in points:
    go_led(*p)
pioneer_mini.land()
pioneer_mini.disarm()
pioneer_mini.led_control()
cam.stop()
