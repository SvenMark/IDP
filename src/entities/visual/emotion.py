import sys
from threading import Thread

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
            lights = Thread(target=self.blink_color(205, 0, 0, 5, 500))
            yellowlights = Thread(target=self.blink_color(255, 255, 0, 5, 750))
            lights.start()
            yellowlights.start()
            self.audio.get_file_path('russiananthem.mp3')
            lights.join()
            yellowlights.join()
        elif emotion == "success":
            self.set_color(0, 205, 0)
            self.audio.get_file_path('success.mp3')
        elif emotion == "sad":
            self.set_brightness(-255)
            self.audio.get_file_path('sad.mp3')
        elif emotion == "happy":
            self.rainbow_colors()
        elif emotion == "confused":
            self.blink_color(255, 105, 180, 20, 500)

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


if __name__ == '__main__':
    emote = Emotion("TrashIdontNeed")
    emote.set_emotion("anthem")
    #time.sleep(1)
    #for i in range(0, 255):
    #    emote.set_brightness(-1)
    #    time.sleep(0.01)
