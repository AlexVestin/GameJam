
from librosa.onset import onset_detect, onset_strength 
from librosa import load, frames_to_time, stft
from librosa.beat import beat_track
import numpy as np
import pygame
import pickle

def play_sound(file_path):
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(-1)

def find_nearest(array, value):
    return (np.abs(array - value)).argmin()

def analyze_audio(file_path):
    data, fs = load(file_path)
    tempo, beats = beat_track(y=data, sr=fs)
    strength   = onset_strength(data, fs)
    timestamps = frames_to_time(beats, sr=fs)
    times = frames_to_time(np.arange(len(strength)))    
    MAX_STRENGTH = np.amax(strength)

    audio_info = []
    for timestamp in timestamps:
        idx = find_nearest(times, timestamp)
        alpha = strength[idx] / MAX_STRENGTH 
        audio_info.append((timestamp, alpha))
    
    return audio_info, tempo


class Analyzer:
    def __init__(self, file_path):
        """audio_info, tempo = analyze_audio(file_path)
        with open("audio.txt", "wb") as f:
            f.write(pickle.dumps(audio_info))
        """
        tempo = 112.3471
        f = open("audio.txt", "rb")
        self.timestamps = pickle.load(f)
        f.close()

    
    def get_beat(self, time):
        sec = time / 1000.0
        if sec > self.timestamps[0][0]:
            ts, strength = self.timestamps.pop(0)
            return True, strength
        
        return False, 0
