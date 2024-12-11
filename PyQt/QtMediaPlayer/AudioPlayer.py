import pygame
import re, time
import random
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from PyQt5.QtCore import pyqtSignal, pyqtBoundSignal, QObject

class Communicator(QObject):
    update_signal = pyqtSignal(str)

class AudioPlayer(QObject):
    signal_playFinish = pyqtSignal(str)
    def __init__(self, playlist, mediaIndex, communicator, isRandom=False):
        pygame.init()
        pygame.mixer.init()
        self.playlist = playlist
        self.current_index = mediaIndex
        self.listLength = len(self.playlist)
        self.is_paused = False
        self.is_playing = False
        self.is_quit = False
        self.end_event = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.end_event)
   
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        system_volume = volume.GetMasterVolumeLevelScalar()
        pygame_volume = system_volume * 0.2
        pygame.mixer.music.set_volume(pygame_volume)
        self.communicator = communicator

        self._isRandom = isRandom

    def play_audio(self):
        if self.current_index >= self.listLength:
            return
        file_path = self.playlist[self.current_index]
        if file_path.endswith(".wma"):
            pass
        else:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
        self.is_playing = True

        self.communicator.update_signal.emit("n")
        # UpdateConfig()
        # ui.lineEdit.setText(GetMediaByIndex(g_playList ,g_audio_player.current_index))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == self.end_event:
                if self._isRandom:
                    randomIndex = random.randint(1, self.listLength)
                    self.current_index = randomIndex
                else:
                    self.current_index += 1
                self.play_audio()   
    
    def pause_audio(self):
        if not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.is_playing = False    

    def resume_audio(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
            self.is_playing = True

    def run(self):
        self.play_audio()
        while self.current_index < len(self.playlist):
            self.handle_events()
            time.sleep(0.1)
            if self.is_quit:
                break
        self.is_playing = False


def player_thread(player):
    player.run()
