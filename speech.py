#!/usr/bin/env python3

import speech_recognition as sr
import pyautogui as pag
import datetime

now = datetime.datetime.now()

def write_to_file(message):
    output = now.isoformat() + ": " + message + '\n'
    f = open('debug.txt', 'a')
    f.write(output)
    f.close()

def execute_voice_cmd(command):
    command_matcher = COMMANDS
    func = command_matcher.get(command, lambda: "Invalid command")
    result = func()
    if result is None:
        write_to_file(command)
    print(result)


# functions for all the voice commands
def toggle_recording():
    pag.hotkey('alt','r')

def toggle_microphone():
    pag.hotkey('alt','n')

def toggle_system_sound():
    pag.hotkey('alt','m')

def screenshot():
    pag.hotkey('alt','s')

def switch_source():
    pag.hotkey('alt','c')

def switch_source_one():
    pag.hotkey('alt','1')

def switch_source_two():
    pag.hotkey('alt','2')

def switch_source_one_two():
    pag.hotkey('alt','3')

def switch_source_two_one():
    pag.hotkey('alt','4')
    
def audio_test():
    pag.typewrite('DEBUG OK')
    


# dictionary with the commands and their corresponding functions
COMMANDS = {
    'toggle recording': toggle_recording, 
    'toggle microphone': toggle_microphone, 
    'toggle system sound': toggle_system_sound,
    'screenshot': screenshot,
    'switch to source one': switch_source_one,
    'switch to source two': switch_source_two,
    'switch to source 1 and 2': switch_source_one_two,
    'switch to source 2 and 1': switch_source_two_one,
    'switch source': switch_source,
    'audio test': audio_test
}


# obtain audio from the microphone
r = sr.Recognizer()
m = sr.Microphone()

# First adjust for ambient noise before we listen.
with m as source:
    r.adjust_for_ambient_noise(source)
	
while True:
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
        write_to_file('Error in recognition')
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))