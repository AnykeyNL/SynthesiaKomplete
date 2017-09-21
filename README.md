# SynthesiaKomplete
Python application to connect Synthesia to the Komplete Kontrol light guide

# How to install
You will need Python (on windows), Synthesia, Komplete Kontrol, loopbe1

Add the following libraries to python by using the pip command:

pip install pywinusb
pip install mido
pip python-rtmidi

Disable in Komplete Kontrol the Light Guide, you can find this option in the preference -> Hardware settings window

Install loopbe1 from www.nerds.de

In Synthesia settings set fot Music Output on the LoopBe internal MIDI interface:
Key Lights -> Ch8. Lights

You should now be all set to run Synthesia and have the Lights Guide you on the Komplete Kontrol keyboard.

(Tested with Komplete Kontrol S61)
