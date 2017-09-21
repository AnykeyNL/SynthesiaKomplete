"""
Synthesia to Komplete Control Light Control
you need to run a midi looping program to receive midi commands.
I have tested this with loopbe1 from www.nerds.de

Written by Richard Garsthagen - The.anykey@gmail.com

You will need the following 3 python libraries:
- pywinusb
- mido
- python-rtmidi

You can install these with pip install [library name]

Feel free to modify and distibute in anyway you like.

This is tested with the Komplete Kontrol S61 keyboard. If you use a different one,
you probably have to change the note offset.

Make sure that in the Komplete Kontrol software your DISABLE Light Guide in the Preference->Hardware settings.

"""

import pywinusb.hid as hid
import mido
import time

def Connect():
    global komplete_device
    global reports
    global bufferC
    kompleteVID = 0x17cc
    kompletePID = 0x1360
    all_devices = hid.HidDeviceFilter(vendor_id = kompleteVID, product_id = kompletePID).get_devices()
    found = False
    if len(all_devices) == 0:
        print ("No komplete device found!")
        found = False
    else:
        print ("Komplete found :-)" )
        komplete_device = all_devices[0]
        komplete_device.open()
        found = True
     
        reports = komplete_device.find_output_reports()

        # Initialize else the light control does not seem to work
        bufferI = [0x00] * 249
        bufferI[0] = 0xa0

        reports[3].set_raw_data(bufferI)
        reports[3].send()

        # Set all keys to 0x00 - Black / no light
        bufferC = [0x00] * 249
        bufferC[2] = 0x82

        reports[2].set_raw_data(bufferC)
        reports[2].send()
   
    return found

def CoolDemoSweep(loopcount):
    speed = 0.01
    for loop in range(0,loopcount):
        for x in range(0, 61):
            bufferC = [0x00] * 249
            bufferC[0] = 0x82
            bufferC[x*3-2] = 0xFF
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
        for x in range(61, 0,-1):
            bufferC = [0x00] * 249
            bufferC[0] = 0x82
            bufferC[x*3-2] = 0xFF
            reports[2].set_raw_data(bufferC)
            reports[2].send()
            time.sleep(speed)
    bufferC = [0x00] * 249
    bufferC[0] = 0x82
    reports[2].set_raw_data(bufferC)
    reports[2].send()
   

def accept_notes(port, channel):
    """Only let note_on and note_off messages through."""
    for message in port:
        if message.type in ('note_on', 'note_off'):
             if message.channel == channel:
                    yield message

def SetNote(note, status):
    bufferC[0] = 0x82
    offset = -36
    key = ((note + offset)*3) + 1
    if status == 'note_on':
        bufferC[key] = 0xff      # Set color to white (RGB)
        bufferC[key+1] = 0xff
        bufferC[key+2] = 0xff
    if status == 'note_off':
        bufferC[key] = 0x00      # Set color to black (RGB)
        bufferC[key+1] = 0x00
        bufferC[key+2] = 0x00
    reports[2].set_raw_data(bufferC)
    reports[2].send()
    

if __name__ == '__main__':
    connected = Connect()
    if connected:
        CoolDemoSweep(2)  # Sweep 2x Red on the keys for fun
        light_channel = 7 # Channel 8 in Synthesia!
        print ("Listening to MIDI")
        with mido.open_input(None) as port:
            for message in accept_notes(port, light_channel):
                print('Received {}'.format(message))
                SetNote(message.note, message.type)
        




        
    
