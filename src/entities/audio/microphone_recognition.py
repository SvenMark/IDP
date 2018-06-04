import sys
import speech_recognition as sr
from chatterbot import ChatBot

sys.path.insert(0, '../../../src')

from entities.audio.speak import Speak


chatbot = ChatBot(  
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
# chatbot.train("chatterbot.corpus.english.conversations")
# chatbot.train("chatterbot.corpus.english")


class Microphone_recognition:

    def __init__(self):
        self.result = "Hello"
        self.speak = Speak()
        self.r = sr.Recognizer()

        self.lang = True

    def run(self):
        # obtain audio from the microphone
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Getting response from google audio to speech api..")
            shit = self.r.recognize_google(audio)
            print("Got a response!")

            language = 'en-AU'
            print("Google Speech Recognition thinks you said " + shit)

            if shit == 'spider':
                self.speak.tts('yes?', language)
                self.recognition()
            else:
                self.run()

        except ValueError:
            print(sys.exc_info())
            self.run()

    def recognition(self):
        with sr.Microphone() as source:
            print("Say something!")
            audio = self.r.listen(source)
        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Getting response from google audio to speech api..")
            shit = self.r.recognize_google(audio)
            print("Got a response!")

            language = 'en-AU'

            print(language)
            print("Google Speech Recognition thinks you said " + shit)

            # Get a response to an input statement

            response = chatbot.get_response(shit)
            print(response)
            self.speak.tts(str(response), language)
            self.run()

        except ValueError:
            print("can you say that again?")
            self.speak.tts('can you say that again please?', 'en-AU')
            print(sys.exc_info())
            self.recognition()

