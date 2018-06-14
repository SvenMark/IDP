import sys
sys.path.insert(0, '../../../src')

from entities.audio.speak import Speak
#Led imports
import time
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Emotion(object):

    def __init__(self):
        self.audio = Speak()
        # Configure the count of pixels:
        self.pixel_count = 17
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.spi_port = 10
        self.spi_device = 0
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.pixel_count, spi=SPI.SpiDev(self.spi_port, self.spi_device),
                                                   gpio=GPIO)
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!


    def neutral(self):
        raise NotImplementedError

    def anthem(self):
        self.audio.play("russiananthem.mp3")

    def success(self):
        self.audio.play("success.mp3")
        self.rainbow_cycle()

    def sad(self):
        self.audio.play("sad.mp3")

    def happy(self):
        raise NotImplementedError

    def depressed(self):
        raise NotImplementedError

    # Define wheel function to interpolate between different hues.
    @staticmethod
    def wheel(pos):
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

    def brightness_decrease(self, wait=0.01, step=1):
        for j in range(int(256 // step)):
            for i in range(self.pixels.count()):
                r, g, b = self.pixels.get_pixel_rgb(i)
                r = int(max(0, r - step))
                g = int(max(0, g - step))
                b = int(max(0, b - step))
                self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)

    def rainbow_cycle(self, wait=0.005):
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count()) + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)


if __name__ == '__main__':
    emotion = Emotion()
    emotion.success()