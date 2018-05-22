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

response = chatbot.get_response("Are you gay")
print(response)
spoke = speak.Speak()
spoke.tts(str(response))

# Train based on the english corpus
#chatbot.train("chatterbot.corpus.english.conversations")
#chatbot.train("chatterbot.corpus.english")


def run():
    # obtain audio from the microphone
    r = sr.Recognizer()
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
        
        
        print("Google Speech Recognition thinks you said " + shit)

        # Get a response to an input statement
        response = chatbot.get_response(shit)
        print(response)
        spoke = speak.Speak()
        spoke.tts(str(response))

        run()
    except:
        print(sys.exc_info())
        run()
        
run()

