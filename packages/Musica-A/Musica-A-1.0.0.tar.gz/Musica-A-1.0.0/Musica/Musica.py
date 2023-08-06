import pygame

class Musica():
    def __init__(self, song):
        pygame.mixer.init()
        pygame.mixer.music.load(str(song))
           
    def start_song(self, loop):
        if loop == 'CONTINUO':
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.play(loops=loop)

    def stop_song(self):
        pygame.mixer.music.stop()

    def setVolume(self, vol):
        pygame.mixer.music.set_volume(vol)