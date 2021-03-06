from mss import mss
import cv2
import numpy as np
import speech_recognition as sr
import pyautogui as pag
import datetime
import sys
from pycaw.pycaw import AudioUtilities

verbose = '--verbose' in sys.argv
video = '--video' in sys.argv

processNameForVolume = "LogiCapture.exe"


sct = mss()
#monitor = sct.monitors[0]
monitor = {'top': 0, 'left': 0, 'width':2560, 'height': 1440}
p = 60
w_test = int(p * monitor['width'] / 100)
h_test = int(p * monitor['height'] / 100)


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
    if verbose:
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
    

def volume_up():
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.name() == processNameForVolume:
            currentVolume = volume.GetMasterVolume();
            if verbose:
                print("Setting volume from", currentVolume, "to", min(1.0, currentVolume + 0.1))
            volume.SetMasterVolume(min(1.0, currentVolume + 0.1), None)

def volume_down():
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
#cap = cv2.VideoCapture(0)
hand_cascade = cv2.CascadeClassifier('Hand.Cascade.1.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

if verbose:
    print("Done calibration")

consecutive_frames = 0

while(True):
    img = np.array(sct.grab(monitor))
    frame = cv2.resize(img, (w_test, h_test))
    #ret, frame = cap.read()
   
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    hands = hand_cascade.detectMultiScale(gray, 1.1, 10)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    shouldListen = False
    if video:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    for (x, y, w, h) in hands:
        toShow = True
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
        if consecutive_frames >= 3:
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
            execute_voice_cmd(voice_cmd)

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
        
#cap.release()
cv2.destroyAllWindows()