#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speak
import speech_recognition as sr
from chatterbot import ChatBot
import sys
import subprocess
import pickle

chatbot = ChatBot(  
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
#chatbot.train("chatterbot.corpus.english.conversations")
#chatbot.train("chatterbot.corpus.english")


result = "Hello"

spoke = speak.Speak()
r = sr.Recognizer()

lang = True

def run():
    # obtain audio from the microphone
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Getting response from google audio to speech api..")
        shit = r.recognize_google(audio)
        print("Got a response!")

        language = 'en-AU'
        print("Google Speech Recognition thinks you said " + shit)

        if shit == 'spider':
            spoke.tts('yes?', language)
            recognition()
        else:
            run()
    except:
        print(sys.exc_info())
        run()

def recognition():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Getting response from google audio to speech api..")
        shit = r.recognize_google(audio)
        print("Got a response!")

        language = 'en-AU'

        print(language)
        print("Google Speech Recognition thinks you said " + shit)
        
        # Get a response to an input statement

        response = chatbot.get_response(shit)
        print(response)
        spoke.tts(str(response), language)
        run()
        
    except:
        print("can you say that again?")
        spoke.tts('can you say that again please?', 'en-AU')
        print(sys.exc_info())
        recognition()

run()
