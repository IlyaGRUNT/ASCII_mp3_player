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
    screen.print_at('■̅̅̅̅̅̅̅̅̅̅̅̅■',
                    2, 0, 7)
    screen.print_at('|',
                    1, 1, 0, 1)
    screen.print_at('|############|',
                    2, 1, 7)
    screen.print_at('|',
                    16, 1, 0, 1)
    screen.print_at('|',
                    1, 2, 0, 1)
    screen.print_at('|',
                    2, 2, 7)
    screen.print_at('( )====( )',
                    4, 2, 7, 1)
    screen.print_at('|',
                    15, 2, 7)
    screen.print_at('|',
                    16, 2, 0, 1)
    screen.print_at('|',
                   1, 3, 0, 1)
    screen.print_at('|############|',
                    2, 3, 7)
    screen.print_at('|',
                    16, 3, 0, 1)
    screen.print_at('■____________■',
                  2, 4, 7)
    screen.print_at('___________________________________',
                    1, 5, 2, 1)
    screen.print_at('#',
                    1, 7, 1)
    screen.print_at('NAME',
                    4, 7, 1)
    screen.print_at('TIME',
                    32, 7, 1)
    for i1 in range(len(song_list)):
        screen.print_at(' ' + str(i1+1) + '.',
                        0, 8+i1, 0, 1)
        if song_list[i1][0][1]:
            screen.print_at(song_list[i1][0][1],
                            4, 8+i1, 7, 1)
        else:
            screen.print_at(song_list[i1][0][0],
                            4, 8+i1, 7, 1)
        screen.print_at(f'{song_list[i1][1][0]}:{song_list[i1][1][1]}',
                        32, 8+i1, 7, 1)
    volume = 0.50
    pygame.mixer.music.set_volume(volume)
    mixer.music.play()
    playing = True
    while True:
        ev = screen.get_key()
        if ev in (ord('U'), ord('u')):
            mixer.music.unpause()
            playing = True
        elif ev in (ord('P'), ord('p')):
            mixer.music.pause()
            playing = False
        elif ev in (ord('Q'), ord('q')):
            return
        elif ev in (ord('W'), ord('w')):
            if volume < 100:
                screen.print_at('+',
                                20, 2, 7, 1)
                volume += 0.01
                pygame.mixer.music.set_volume(volume)
        elif ev in (ord('S'), ord('s')):
            if volume > 0:
                screen.print_at('-',
                                20, 2, 7, 1)
                volume -= 0.01
                pygame.mixer.music.set_volume(volume)
        if len(str(round(volume, 2))[2:]) == 1:
            screen.print_at(str(round(volume, 2)) + '0',
                            22, 2, 7, 1)
        else:
            screen.print_at(str(round(volume, 2)),
                            22, 2, 7, 1)
        i += 1
        if i % 40 == 0 and playing:
            screen.print_at('/',
                            5, 2, 7, 1)
            screen.print_at('/',
                            12, 2, 7, 1)
        elif i % 40 == 10 and playing:
            screen.print_at('-',
                            5, 2, 7, 1)
            screen.print_at('-',
                            12, 2, 7, 1)
        elif i % 40 == 20 and playing:
            screen.print_at('\\',
                            5, 2, 7, 1)
            screen.print_at('\\',
                            12, 2, 7, 1)
        elif i % 40 == 30 and playing:
            screen.print_at('|',
                            5, 2, 7, 1)
            screen.print_at('|',
                            12, 2, 7, 1)
        screen.refresh()
        time.sleep(0.04)

os.system('mode con: cols=37 lines=15')
Screen.wrapper(anim)
