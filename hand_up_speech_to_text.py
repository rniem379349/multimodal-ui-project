import cv2
import numpy as np
import speech_recognition as sr
import pyautogui as pag
import datetime
import sys
from pycaw.pycaw import AudioUtilities

verbose = '--verbose' in sys.argv
video = '--video' in sys.argv

now = datetime.datetime.now()
processNameForVolume = "LogiCapture.exe"

def write_to_file(message):
    output = now.isoformat() + ": " + message + '\n'
    f = open('debug.txt', 'a')
    f.write(output)
    f.close()

def execute_voice_cmd(command, *args, **kwargs):
    command_matcher = COMMANDS
    func = command_matcher.get(command, lambda _: "Invalid command")
    result = func(*args, **kwargs)
    if result is None:
        write_to_file(command)
    if verbose:
        print(result)


# functions for all the voice commands
def toggle_recording(*args, **kwargs):
    pag.hotkey('alt','r')

def toggle_microphone(*args, **kwargs):
    pag.hotkey('alt','n')

def toggle_system_sound(*args, **kwargs):
    pag.hotkey('alt','m')

def screenshot(*args, **kwargs):
    pag.hotkey('alt','s')

def switch_source(handOnTheLeft = None):
    if handOnTheLeft == True:
        print("hand on left")
        pag.hotkey('alt','1')
    elif handOnTheLeft == False:
        print("hand on right")
        pag.hotkey('alt','2')
    else:
        print("Sumthin else")
        pag.hotkey('alt','c')

def switch_source_one(*args, **kwargs):
    pag.hotkey('alt','1')

def switch_source_two(*args, **kwargs):
    pag.hotkey('alt','2')

def switch_source_one_two(*args, **kwargs):
    pag.hotkey('alt','3')

def switch_source_two_one(*args, **kwargs):
    pag.hotkey('alt','4')
    
def audio_test(*args, **kwargs):
    pag.typewrite('DEBUG OK')
    
def volume_up(*args, **kwargs):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == processNameForVolume:
            currentVolume = volume.GetMasterVolume();
            if verbose:
                print("Setting volume from", currentVolume, "to", min(1.0, currentVolume + 0.1))
            volume.SetMasterVolume(min(1.0, currentVolume + 0.1), None)

def volume_down(*args, **kwargs):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process:
            print(session.Process.name())
        if session.Process and session.Process.name() == processNameForVolume:
            currentVolume = volume.GetMasterVolume();
            if verbose:
                print("Setting volume from", currentVolume, "to", max(0.0, currentVolume - 0.1))
            volume.SetMasterVolume(max(0.0, currentVolume - 0.1), None)


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
    'audio test': audio_test,
    'volume up': volume_up,
    'volume down': volume_down
}

if verbose:
    print("Calibrating microphone")
r = sr.Recognizer()
m = sr.Microphone()
with m as source:
	r.adjust_for_ambient_noise(source)

if verbose:
    print("Calibrating camera")
cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier('Hand.Cascade.1.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

if verbose:
    print("Done calibration")

consecutive_frames = 0

while(True):
    ret, frame = cap.read()
   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    hands = hand_cascade.detectMultiScale(gray, 1.1, 10)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    # print (cap.get(3)) # x dimension of frame
    # print (cap.get(4)) # y dimension of frame

    # print(hands)

    handOnTheLeft = None # false - hand raised on the right side, true - left side
    shouldListen = False
    if video:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    for (x, y, w, h) in hands:
        toShow = True
        print("x: " + str(x))
        if x <= cap.get(3)/2:
            print("Hand on the left")
            handOnTheLeft = True
        elif x > cap.get(3)/2:
            print("Hand on the right")
            handOnTheLeft = False
        for (_, y2, _, h2) in faces:
            if y2 < y + h / 2:
                toShow = False

        if toShow and len(faces) > 0:
            if video:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            shouldListen = True
    

    if video:
        cv2.imshow('Frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    if shouldListen:
        consecutive_frames = consecutive_frames + 1
        if consecutive_frames >= 5:
            consecutive_frames = 0
        else:
            continue
    else:
        consecutive_frames = 0
        continue
        
    with sr.Microphone() as source:
        try:
            if verbose:
                print("Say something!")
            audio = r.listen(source, timeout=1, phrase_time_limit=5)
            if verbose:
                print("Done listening")
            voice_cmd = r.recognize_google(audio).lower()
            if verbose:
                print("Your command: " + voice_cmd)

            # try to execute the command
            execute_voice_cmd(voice_cmd, handOnTheLeft)

            # exception handling
        except sr.UnknownValueError:
            if verbose:
                print("Google Speech Recognition could not understand audio")
            write_to_file('Error in recognition')
        except sr.RequestError as e:
            if verbose:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except sr.WaitTimeoutError as e:
            if verbose:
                print("Error: {0}".format(e))
        
cap.release()
cv2.destroyAllWindows()