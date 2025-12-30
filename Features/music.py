import os
import random
import time

class MusicPlayer:
    def __init__(self, playlist_path):
        self.playlist_path = playlist_path
        self.music_files = [file for file in os.listdir(playlist_path) if file.endswith('.mp3')]
        if not self.music_files:
            print('No music files found in playlist path.')
        self.current_song_index = None
        self.paused = False
        self.pause_time = None

    def play_random_song(self):
        if not self.music_files:
            return False
        random_song = random.choice(self.music_files)
        self.current_song_index = self.music_files.index(random_song)
        music_path = os.path.join(self.playlist_path, random_song)
        os.startfile(music_path)
        self.paused = False
        self.pause_time = None
        return True
    
    def pause(self):
        if not self.paused:
            os.system('taskkill /F /IM wmplayer.exe') # Windows specific command to pause playback
            self.paused = True
            self.pause_time = time.time()

playlist_path = r"D:\\Music"
player = MusicPlayer(playlist_path)

