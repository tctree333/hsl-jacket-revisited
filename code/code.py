import board
import digitalio
import analogio
import neopixel
import colorsys
import time

hue_button = digitalio.DigitalInOut(board.GP16)
hue_button.direction = digitalio.Direction.INPUT
hue_button.pull = digitalio.Pull.DOWN
sat_button = digitalio.DigitalInOut(board.GP17)
sat_button.direction = digitalio.Direction.INPUT
sat_button.pull = digitalio.Pull.DOWN
light_button = digitalio.DigitalInOut(board.GP18)
light_button.direction = digitalio.Direction.INPUT
light_button.pull = digitalio.Pull.DOWN

pot = analogio.AnalogIn(board.GP26)

pixels = neopixel.NeoPixel(board.GP15, 30, brightness=0.1)
pixels.fill((0, 255, 255))

num_pixels = 30

hue = .5
sat = 1
light = 0.5


min_pot = 17800
max_pot = 45700
def avg_pot():
    total = 0
    for _ in range(15000):
        total += pot.value
    return 1 - min(1, max(0, ((total / 15000) - min_pot) / (max_pot - min_pot)))
    
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b)


def rainbow_cycle(j):
    for i in range(num_pixels):
        pixel_index = (i * 256 // num_pixels) + j
        pixels[i] = wheel(pixel_index & 255)
    pixels.show()

led_change = False
rainbow = True
last_press = 0
j = 0
while True:
    t = time.monotonic()
    if last_press != 0 and hue_button.value and (t-last_press) < .5:
        last_press = 0
        rainbow = not rainbow
    elif hue_button.value:
        last_press = t

    if rainbow:
        rainbow_cycle(j)
        j += 1
        j = j % 255
    else:
        current_pot = avg_pot()
    
        if hue_button.value:
            hue = avg_pot()
            led_change = True
        if sat_button.value:
            sat = avg_pot()
            led_change = True
        if light_button.value:
            light = avg_pot()
            led_change = True
    
        if led_change:
            pixels.fill(tuple(map(lambda x: int(x), ((255, 255, 255) if sat == 0 else colorsys.hsv_to_rgb(hue, sat, 1)))))
            pixels.brightness = light
            pixels.show()
            led_change = False
