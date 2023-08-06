play music in python gui
takes a cue from pygame for a simpler version

#for start need GUI (recommend tkinter)
music = Musica('song.mp3')

music.setVolume(0.3) #set volume

music.start_song(loop=2) #repet 2 times

#music.start_song(loop='CONTINUO') for infinity loop


music.stop_song #stop music  