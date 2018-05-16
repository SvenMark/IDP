#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speak
import speech_recognition as sr
from chatterbot import ChatBot
import sys
import subprocess

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)


# Train based on the english corpus
#chatbot.train("chatterbot.corpus.english.conversations")

def run(chatbot):
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
        
        spoke = speak.Speak()
        spoke.tts(str(response))

        run(chatbot)
    except:
        print(sys.exc_info())
        run(chatbot)
        
run(chatbot)

