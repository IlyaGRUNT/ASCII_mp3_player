import time
import os
import glob
import math
import eyed3
from mutagen.mp3 import MP3
from asciimatics.screen import Screen
import pygame
from pygame import mixer

i = 0
mpts = glob.glob('*.mp3')
dark_grey = '\033[1;30;40m'
light_grey = '\033[0;37;40m'
white = '\033[1;37;40m'
lime = '\033[1;32;40m'
red = '\033[0;31;40m'

song_list = []

pygame.init()
mixer.init()

for mpt in mpts:
    song = MP3(mpt)
    duration = math.ceil(song.info.length)
    m_duration = duration // 60
    s_duration = duration % 60
    song = eyed3.load(mpt)
    name = song.tag.title
    song_list.append([[mpt[:-4], name], [m_duration, s_duration]])
    mixer.music.load(mpt)
    mixer.music.queue(mpt)



def anim(screen):
    # 0-black 1-red 2-green 3-yellow 4-blue 5-purple 6-light_blue 7-white
    global song_list
    i = 0
    # cassette
    screen.print_at('■̅̅̅̅̅̅̅̅̅̅̅̅̅■',
                    2, 1, 7)
    screen.print_at('|',
                    1, 2, 0, 1)
    screen.print_at('|#############|',
                    2, 2, 7)
    screen.print_at('|',
                    17, 2, 0, 1)
    screen.print_at('|',
                    1, 3, 0, 1)
    screen.print_at('|',
                    2, 3, 7)
    screen.print_at('(/)=====(/)',
                    4, 3, 7, 1)
    screen.print_at('|',
                    16, 3, 7)
    screen.print_at('|',
                    17, 3, 0, 1)
    screen.print_at('|',
                   1, 4, 0, 1)
    screen.print_at('|#############|',
                    2, 4, 7)
    screen.print_at('|',
                    17, 4, 0, 1)
    screen.print_at('■_____________■',
                    2, 5, 7)
    # volume
    screen.print_at('VOL',
                    19, 0, 7, 1)
    screen.print_at('-+-',
                    19, 1, 0, 1)
    screen.print_at('-+-',
                    19, 2, 0, 1)
    screen.print_at('60%',
                    19, 3, 2, 1)
    screen.print_at('-+-',
                    19, 4, 0, 1)
    screen.print_at('-+-',
                    19, 5, 0, 1)
    screen.print_at('-+-',
                    19, 6, 0, 1)
    screen.print_at('___________________________________',
                    1, 7, 2, 1)
    # song list
    screen.print_at('#',
                    1, 9, 1)
    screen.print_at('NAME',
                    4, 9, 1)
    screen.print_at('TIME',
                    32, 9, 1)
    for i1, song in enumerate(song_list, start=1):
        screen.print_at(' ' + str(i1) + '.',
                        0, 9+i1, 0, 1)
        if song[0][1]:
            screen.print_at(song[0][1],
                            4, 9+i1, 7, 1)
        else:
            screen.print_at(song[0][0],
                            4, 9+i1, 7, 1)
        screen.print_at(f'{song[1][0]}:{song[1][1]}',
                        32, 9+i1, 7, 1)
    screen.print_at('-',
                    5, 6, 1)
    screen.print_at('#',
                    9, 6, 1)
    screen.print_at('+',
                    13, 6, 1)
    volume = 0.6
    pygame.mixer.music.set_volume(volume)
    mixer.music.play()
    playing = True
    p = 0
    while True:
        ev = screen.get_key()
        if ev in (ord('U'), ord('u'), ord('Г'), ord('г')):
            mixer.music.unpause()
            playing = True
        elif ev in (ord('P'), ord('p'), ord('З'), ord('з')):
            mixer.music.pause()
            playing = False
        elif ev in (ord('Q'), ord('q'), ord('Й'), ord('й')):
            return
        if ev in (ord('W'), ord('w'), ord('Ц'), ord('ц')):
            if volume < 1:
                p = 1
                screen.print_at('+',
                                13, 6, 1, 1)
                screen.print_at('-',
                                5, 6, 1)
                volume += 0.01
                pygame.mixer.music.set_volume(volume)
        elif ev in (ord('S'), ord('s'), ord('Ы'), ord('ы')):
            if volume > 0:
                p = 1
                volume -= 0.01
                pygame.mixer.music.set_volume(volume)
                screen.print_at('+',
                                13, 6, 1)
                screen.print_at('-',
                                5, 6, 1, 1)
        else:
            if p >= 2**13:
                p = 0
                screen.print_at('-',
                                5, 6, 1)
                screen.print_at('+',
                                13, 6, 1)

        i += 1
        p *= 2
        # spinning animation
        if i % 40 == 0 and playing:
            screen.print_at('/',
                            5, 3, 7, 1)
            screen.print_at('/',
                            13, 3, 7, 1)
        elif i % 40 == 10 and playing:
            screen.print_at('-',
                            5, 3, 7, 1)
            screen.print_at('-',
                            13, 3, 7, 1)
        elif i % 40 == 20 and playing:
            screen.print_at('\\',
                            5, 3, 7, 1)
            screen.print_at('\\',
                            13, 3, 7, 1)
        elif i % 40 == 30 and playing:
            screen.print_at('|',
                            5, 3, 7, 1)
            screen.print_at('|',
                            13, 3, 7, 1)
        # show volume
        if volume > 0.9:
            screen.print_at('100%',
                            19, 1, 2, 1)
            screen.print_at('-+-',
                            19, 2, 0, 1)
        if 0.9 >= volume > 0.7:
            screen.print_at('-+- ',
                            19, 1, 0, 1)
            screen.print_at('80%',
                            19, 2, 2, 1)
            screen.print_at('-+-',
                            19, 3, 0, 1)
        if 0.7 >= volume > 0.5:
            screen.print_at('-+-',
                            19, 2, 0, 1)
            screen.print_at('60%',
                            19, 3, 2, 1)
            screen.print_at('-+-',
                            19, 4, 0, 1)
        if 0.5 >= volume > 0.3:
            screen.print_at('-+-',
                            19, 3, 0, 1)
            screen.print_at('40%',
                            19, 4, 2, 1)
            screen.print_at('-+-',
                            19, 5, 0, 1)
        if 0.3 >= volume > 0.1:
            screen.print_at('-+-',
                            19, 4, 0, 1)
            screen.print_at('20%',
                            19, 5, 2, 1)
            screen.print_at('-+-',
                            19, 6, 0, 1)
        if 0.1 >= volume:
            screen.print_at('-+-',
                            19, 5, 0, 1)
            screen.print_at('0%',
                            19, 6, 2, 1)
        screen.refresh()
        time.sleep(0.04)

os.system('mode con: cols=37 lines=15')
Screen.wrapper(anim)
