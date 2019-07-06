"""NeoPixel LED Demo."""
from machine import Pin
from neopixel import NeoPixel
from time import sleep


def hsv_to_rgb(h, s, v):
    """
    Convert HSV to RGB (based on colorsys.py).

        Args:
            h (float): Hue 0 to 1.
            s (float): Saturation 0 to 1.
            v (float): Value 0 to 1 (Brightness).
    """
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i = i % 6

    v = int(v * 255)
    t = int(t * 255)
    p = int(p * 255)
    q = int(q * 255)

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


np = NeoPixel(Pin(13), 1)
spectrum = list(range(2048)) + list(reversed(range(2048)))


try:
    while True:
        for c in spectrum:
            hue = c / 2048.0
            np[0] = hsv_to_rgb(hue, 1, .15)
            np.write()
            sleep(.01)

except KeyboardInterrupt:
    print("\nCtrl-C pressed.  Cleaning up and exiting...")
finally:
    np[0] = (0, 0, 0)  # Turn off NeoPixel
    np.write()
