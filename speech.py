#!/usr/bin/env python3

import speech_recognition as sr
import pyautogui as pag


def execute_voice_cmd(command):
    command_matcher = COMMANDS
    func = command_matcher.get(command, lambda: "Invalid command")
    print(func())


# functions for all the voice commands
def hello():
    pag.hotkey('ctrl','f')

def world():
    pag.typewrite('black guns')

def man():
    pag.hotkey('enter')


# dictionary with the commands and their corresponding functions
COMMANDS = {
    'hello': hello, 
    'world': world, 
    'man': man
}


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

    # get lowercase voice command token
    voice_cmd = r.recognize_google(audio).lower()
    print("Your command: " + voice_cmd)

    # try to execute the command
    execute_voice_cmd(voice_cmd)


# exception handling
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))