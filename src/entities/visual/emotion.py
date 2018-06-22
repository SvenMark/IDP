import sys
import time
import RPi.GPIO as GPIO
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI
from threading import Thread

sys.path.insert(0, '../../../src')

from entities.audio.audio import Audio
from entities.threading.utils import SharedObject


class Emotion(object):

    def __init__(self, audio):
        self.audio = audio

        self.pixel_count = 18  # Configure the count of pixels:
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.spi_port = 0
        self.spi_device = 0
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.pixel_count, spi=SPI.SpiDev(self.spi_port, self.spi_device),
                                                   gpio=GPIO)
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!
        self.playing = False

    def set_emotion(self, emotion):
        """
        Set the correct emotion based on the input.
        This includes lights and sounds
        :param emotion: string with the kind of emotion you want
        :return:
        """
        time.sleep(0.01)
        if emotion == "neutral":
            # Boston University Red
            self.set_color(205, 0, 0)
        elif emotion == "anthem":
            memes = Thread(target=self.play_sound('russiananthem.mp3')).start()
            time.sleep(1)
            print(self.playing)
            while self.playing:
                print("Blink")
                self.blink_color(205, 0, 0, 1, 0.3)
            memes.join()
        elif emotion == "success":
            self.set_color(0, 205, 0)
            self.play_sound('success.mp3')
        elif emotion == "mad":
            self.set_brightness(-255)
            Thread(target=self.play_sound('cyka.mp3')).start()
        elif emotion == "happy":
            self.rainbow_colors()
        elif emotion == "confused":
            Thread(target=self.play_sound('heya.mp3')).start()
            time.sleep(1)
            while self.playing:
                self.blink_color(255, 105, 180, 0, 0.2)
        elif emotion == "confirmed":  # Used for building detection
            self.set_color(0, 205, 0)
        elif emotion == "searching":  # Used for building detection
            Thread(target=self.rotate_color(255, 165, 0, 0)).start()

    def play_sound(self, file):
        print("Starting audio file")
        self.playing = True
        self.audio.speak.play(file)
        self.playing = False
        self.set_emotion("neutral")
        print("Audio file finished.")

    def set_color(self, r, b, g):
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

    def blink_color(self, r, b, g, blink_times, blinkdelay):
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

    def rainbow_colors(self, wait=0.1):
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

    def appear_from_back(self, color=(0, 255, 0)):
        pos = 0
        for i in range(self.pixels.count()):

            for j in reversed(range(i, self.pixels.count())):
                self.pixels.clear()
                # first set all pixels at the begin
                for k in range(i):
                    self.pixels.set_pixel(k, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
                # set then the pixel at position j
                self.pixels.set_pixel(j, Adafruit_WS2801.RGB_to_color(color[0], color[1], color[2]))
                self.pixels.show()
                time.sleep(0.01)

    def rotate_color(self, r, g, b, rotate_times):
        for j in range(rotate_times):
            self.pixels.clear()
            for i in range(self.pixels.count()):
                if i > 1:
                    self.pixels.set_pixel(i - 2, Adafruit_WS2801.RGB_to_color(0, 0, 0))
                self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(r, b, g))
                time.sleep(0.05)
                self.pixels.show()


if __name__ == '__main__':
    audio = Audio()
    emote = Emotion(audio)

    # emote.rotate_color(0, 0, 255, 5)

    # emote.appear_from_back()
    # emote.blink_color(0, 0, 255, 5, 0.2)

    #Thread(target=emote.set_emotion("anthem"))
    #time.sleep(20)
    #emote.set_emotion("mad")
    while True:
        emote.rainbow_colors()
    # emote.set_emotion("mad")
    # emote.set_emotion("neutral")
    # emote.rainbow_colors()
    # emote.set_emotion("neutral")
