import pyvjoy
import keyboard
j = pyvjoy.VJoyDevice(1)
#j=0
def xAxis(angle):
        print("angle",angle)
        bearing=16834-int((angle/90)*16384) 
        j.set_axis(pyvjoy.HID_USAGE_X,bearing)

def reCentre():
        print("reCentre")
	#j.set_button(2,0)
	#j.set_button(1,0)
        keyboard.release('w')
        keyboard.release('s')
	#j.set_axis(pyvjoy.HID_USAGE_Y,0x0000)
	#j.set_button(1,0)
def yAxis(speed):
        #keyboard.press('w')
        print("speed")
        keyboard.release('s')
        #j.set_button(2,0)
        acceleration=int((speed/100)*32678)
        #keyboard.press('w')
        j.set_axis(pyvjoy.HID_USAGE_Y,acceleration)
	
def Brake():
        keyboard.release('w')
        keyboard.press('s')
        print("Brake")
        #j.set_button(1,0)
        #j.set_button(2,1)
	
	
