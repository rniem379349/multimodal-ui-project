# multimodal-ui-project

It is recommended to run this project using a python virtual environment (virtualenv). The requirements.txt file lists all the needed libraries for the project.

Additional requirements - can be installed with pip:
- opencv
- mss

----hand_up_speech_to_text.py----

Program that uses the webcam feed to detect faces and hands. 
When a hand is above the head (for a certain amount of phrames), the microphone is activated and waiting for the command. 

To start, just run "python hand_up_speech_to_text.py"
Additional params:
    --verbose  For getting prints about the state of the program.
    --video To show visually what the algorithm is detecting. It will draw red rectangles on the faces and green ones on hands higher than faces.
Note: the video feed will be interrupted while waiting for audio.


----screenshot.py----

Because the streaming program has access to the webcam feed (and getting opencv access to the same feed would result in an error) we could:
    - use a second webcam
    - take recording of the desktop and run recognition on that (high resolution monitors might have fps issues).
    
For desktop recording, use "python screenshot.py". Note that line 14 sets up the location of the screenshot. If you have only one monitor,
simple comment line 14 and un-comment line 13. Otherwise, re-define the monitor region using line 14.