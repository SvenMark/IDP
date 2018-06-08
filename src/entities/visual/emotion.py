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
        self.pixel_count = 32
        # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
        self.spi_port = 0
        self.spi_device = 0
        self.pixels = Adafruit_WS2801.WS2801Pixels(self.pixel_count, spi=SPI.SpiDev(self.spi_port, self.spi_device),
                                                   gpio=GPIO)

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

    def rainbow_cycle(self, wait=0.005):
        for j in range(256):  # one cycle of all 256 colors in the wheel
            for i in range(self.pixels.count()):
                self.pixels.set_pixel(i, self.wheel(((i * 256 // self.pixels.count()) + j) % 256))
            self.pixels.show()
            if wait > 0:
                time.sleep(wait)


if __name__ == '__main__':
    emotion = Emotion()
    emotion.sad()