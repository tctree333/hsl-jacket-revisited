import board
import digitalio
import analogio
import neopixel
import colorsys

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

pixels = neopixel.NeoPixel(board.GP15, 15, brightness=0.1)
pixels.fill((0, 255, 255))

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

led_change = False
while True:
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