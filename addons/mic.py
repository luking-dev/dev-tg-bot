from email import message
import sounddevice as sd
from scipy.io.wavfile import write
#import os

def record(name="voice.wav", long=5, messages=False, samplerate=44100, channels=2):
    myrecording = sd.rec(int(long * samplerate), samplerate=samplerate, channels=channels)

    if messages:
        print("Record starting: speak now!")
    
    sd.wait()  # Wait until recording is finished

    if messages:
        print("Mic record finished")

    write(name, samplerate, myrecording)  # Save as WAV file
    #os.startfile("output.wav")

    return name


if "__main__" == __name__:
    record()