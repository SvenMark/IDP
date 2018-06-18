import sys

sys.path.insert(0, '../../../src')

# Led imports
import time
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


class Emotion(object):

    def __init__(self, speak):
        self.audio = speak
        # Configure the count of pixels:
        self.pixel_count = 33
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.spi_port = 0
        self.spi_device = 0
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.pixel_count, spi=SPI.SpiDev(self.spi_port, self.spi_device),
                                                   gpio=GPIO)
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!

    def set_emotion(self, emotion):
        """
        Set the correct emotion based on the input.
        This includes lights and sounds
        :param emotion: string with the kind of emotion you want
        :return:
        """
        if emotion == "neutral":
            # Boston University Red
            self.set_color(205, 0, 0)
        elif emotion == "anthem":
            self.blink_color(205, 0, 0, 5, 500)
            self.audio.get_file_path('russiananthem.mp3')
        elif emotion == "success":
            pass
        elif emotion == "sad":
            self.brightness_off()
        elif emotion == "happy":
            self.rainbow_colors()

    def set_color(self, r, g, b):
        """
        Function to set the color of the leds
        :param r: red color value
        :param g: green color value
        :param b: blue color value
        :return: void
        """
        for i in range(self.pixels.count()):
            self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        self.pixels.show()

    def blink_color(self, r, g, b, blink_times, blinkdelay):
        for i in range(blink_times):
            # blink x times, then wait
            self.pixels.clear()
            for k in range(self.pixels.count()):
                self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(r, g, b))
            self.pixels.show()
            time.sleep(blinkdelay)
            self.pixels.clear()
            self.pixels.show()
            time.sleep(blinkdelay)

    @staticmethod
    def wheel(pos):
        """
        Wheel method to generate all the RGB colors for rainbow effects
        """
        if pos < 85:
            return Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Adafruit_WS2801.RGB_to_color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Adafruit_WS2801.RGB_to_color(0, pos * 3, 255 - pos * 3)

    def set_brightness(self, brightnessoffset):
        for i in range(self.pixels.count()):
            r, g, b = self.pixels.get_pixel_rgb(i)
            r = int(max(0, r + brightnessoffset))
            g = int(max(0, g + brightnessoffset))
            b = int(max(0, b + brightnessoffset))
            self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, g, b))
        self.pixels.show()

    def brightness_off(self, wait=0.01, step=1):
        """
        Function to decrease the brightness to 0
        :param wait: Time to wait after a color change, lower is faster animation.
        :param step: Amount to go down each loop, higher is faster animation but more choppy.
        :return:
        """
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
        """
        Function to make the leds display a rainbow cycling animation
        :param wait: Time to wait after a color change, lower is faster animation.
        :return: void
        """
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count()) + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)

    def rainbow_colors(self, wait=0.05):
        """
        Function to make the entire strip cycle rainbow colors at once
        :param wait:
        :return:
        """
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel((256 // self.pixels.count() + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)
