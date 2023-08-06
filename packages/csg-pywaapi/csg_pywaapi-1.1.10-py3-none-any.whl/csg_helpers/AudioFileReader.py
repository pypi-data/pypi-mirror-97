#import wave as wv
import PyWave as wv

def OpenAudioFile(filename):
    #audiofile = sf.SoundFile(filename)
    audiofile = wv.open(filename,"r")
    return audiofile

def GetChannels(filename):
    audiofile = OpenAudioFile(filename)
    channels = audiofile.channels
    audiofile.close()
    return channels
    # return audiofile.getnchannels()

def GetSamplerate(filename):
    audiofile = OpenAudioFile(filename)
    SampleRate = audiofile.frequency
    audiofile.close()
    return SampleRate
    # return audiofile.getframerate()


