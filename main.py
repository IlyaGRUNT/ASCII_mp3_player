import os
os.system('pip install eyed3')
os.system('pip install mutagen')
os.system('pip install asciimatics')
os.system('pip install pygame')
os.system('pip install pydub')
import time
import shutil
import glob
import math
import eyed3
import subprocess
from mutagen.mp3 import MP3
from asciimatics.screen import Screen
import pygame
from pygame import mixer
from pydub import AudioSegment


def match_target_amplitude(sound, target_dBFS):
    # function that does the normalizing, courtesy https://github.com/jiaaro/pydub/issues/90
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


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
try:
    shutil.rmtree('cache')
except:
    pass
os.mkdir('cache')

queue = []
MUSIC_END = pygame.USEREVENT+1
pygame.mixer.music.set_endevent(MUSIC_END)
nps = []

for n, mpt in enumerate(mpts):
    song = MP3(mpt)
    duration = math.ceil(song.info.length)
    m_duration = duration // 60
    s_duration = duration % 60
    song = eyed3.load(mpt)
    name = None
    try:
        name = song.tag.title
    except:
        pass
    song_list.append([[mpt[:-4], name], [m_duration, s_duration]])
    if n == 0:
        mixer.music.load(mpt)
    queue.append(mpt)
    subprocess.call([r'C:\ffmpeg\ffmpeg\bin\ffmpeg.exe', '-i', f'{mpt}',
                    f'cache/{mpt[:-4]}.wav'],
                    stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    song = AudioSegment.from_file(f'cache/{mpt[:-4]}.wav', 'wav')
    splitsong = song.split_to_mono()
    left = splitsong[0]
    right = splitsong[1]
    normalized_left = match_target_amplitude(left, -20.0)
    normalized_right = match_target_amplitude(right, -20.0)
    np_left = normalized_left.get_array_of_samples()
    np_right = normalized_right.get_array_of_samples()
    chunk = len(np_left) / (duration / 0.08)
    nps.append([chunk, np_left, np_right, duration, max(max(np_right), -min(np_right)), max(max(np_left), -min(np_left))])


def anim(screen):
    # 0-black 1-red 2-green 3-yellow 4-blue 5-purple 6-light_blue 7-white
    global nps
    global song_list
    i = 0
    i2 = 0
    # main box
    screen.print_at('.̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅̅.',
                    2, 1, 2, 1)
    screen.print_at(':',
                    2, 2, 2, 1)
    screen.print_at(':',
                    68, 2, 2, 1)
    screen.print_at(':',
                    2, 3, 2, 1)
    screen.print_at(':',
                    68, 3, 2, 1)
    screen.print_at(':',
                    2, 4, 2, 1)
    screen.print_at(':',
                    68, 4, 2, 1)
    screen.print_at(':',
                    2, 5, 2, 1)
    screen.print_at(':',
                    68, 5, 2, 1)
    screen.print_at(':',
                    2, 6, 2, 1)
    screen.print_at(':',
                    68, 6, 2, 1)
    screen.print_at(':',
                    2, 7, 2, 1)
    screen.print_at(':',
                    68, 7, 2, 1)
    screen.print_at(':',
                    2, 8, 2, 1)
    screen.print_at(':',
                    68, 8, 2, 1)
    screen.print_at('._________________________________________________________________.',
                    2, 9, 2, 1)
    # cassette
    screen.print_at('■̅̅̅̅̅̅̅̅̅̅̅̅̅■',
                    4, 3, 7)
    screen.print_at('|',
                    3, 4, 0, 1)
    screen.print_at('|#############|',
                    4, 4, 7)
    screen.print_at('|',
                    19, 4, 0, 1)
    screen.print_at('|',
                    3, 5, 0, 1)
    screen.print_at('|',
                    4, 5, 7)
    screen.print_at('(/)=====(/)',
                    6, 5, 7, 1)
    screen.print_at('|',
                    18, 5, 7)
    screen.print_at('|',
                    19, 5, 0, 1)
    screen.print_at('|',
                    3, 6, 0, 1)
    screen.print_at('|#############|',
                    4, 6, 7)
    screen.print_at('|',
                    19, 6, 0, 1)
    screen.print_at('■_____________■',
                    4, 7, 7)
    # volume
    screen.print_at('VOL',
                    63, 2, 7, 1)
    screen.print_at('-+-',
                    63, 3, 0, 1)
    screen.print_at('-+-',
                    63, 4, 0, 1)
    screen.print_at('60%',
                    63, 5, 2, 1)
    screen.print_at('-+-',
                    63, 6, 0, 1)
    screen.print_at('-+-',
                    63, 7, 0, 1)
    screen.print_at('-+-',
                    63, 8, 0, 1)
    # audio visualizer and box
    screen.print_at('L ++++++++++',
                    24, 4, 0, 1)
    screen.print_at('R ++++++++++',
                    24, 5, 0, 1)
    screen.print_at('______________',
                    23, 3, 5)
    screen.print_at('|',
                    21, 4, 5, 1)
    screen.print_at('|',
                    38, 4, 5, 1)
    screen.print_at('|',
                    21, 5, 5, 1)
    screen.print_at('|',
                    38, 5, 5, 1)
    screen.print_at('|',
                    22, 4, 5)
    screen.print_at('|',
                    37, 4, 5)
    screen.print_at('|',
                    22, 5, 5)
    screen.print_at('|',
                    37, 5, 5)
    screen.print_at('̅̅̅̅̅̅̅̅̅̅̅̅̅̅',
                    23, 6, 5)
    # song list
    screen.print_at('#',
                    2, 11, 1)
    screen.print_at('NAME',
                    5, 11, 1)
    screen.print_at('TIME',
                    33, 11, 1)
    for i1, song in enumerate(song_list, start=1):
        screen.print_at(str(i1) + '.',
                        2, 11+i1, 0, 1)
        if song[0][1]:
            screen.print_at(song[0][1],
                            5, 11+i1, 7, 1)
        else:
            screen.print_at(song[0][0],
                            5, 11+i1, 7, 1)
        screen.print_at(f'{song[1][0]}',
                        33, 11 + i1, 7, 1)
        screen.print_at(':',
                        34, 11 + i1, 0, 1)
        if len(str(song[1][1])) == 1:
            screen.print_at('0' + str(song[1][1]),
                            35, 11 + i1, 7, 1)
        else:
            screen.print_at(str(song[1][1]),
                            35, 11 + i1, 7, 1)
    # control buttons
    screen.print_at('<<',
                    5, 8, 1)
    screen.print_at('-',
                    8, 8, 1)
    screen.print_at('#',
                    11, 8, 1)
    screen.print_at('+',
                    14, 8, 1)
    screen.print_at('>>',
                    17, 8, 1)
    volume = 0.6
    pygame.mixer.music.set_volume(volume)
    mixer.music.play()
    playing = True
    min_vol = 0
    max_vol = 0
    q = 0
    while True:
        # event listening
        event = pygame.event.get()
        if event:
            event = event[0]
            if event.type == MUSIC_END:
                i2 = 0
                q += 1
                pygame.event.clear()
                mixer.music.load(queue[q])
                mixer.music.play()
        ev = screen.get_key()
        if ev in (ord('U'), ord('u'), ord('Г'), ord('г')):
            mixer.music.unpause()
            playing = True
        elif ev in (ord('P'), ord('p'), ord('З'), ord('з')):
            mixer.music.pause()
            playing = False
        elif ev in (ord('Z'), ord('z'), ord('Я'), ord('я')):
            return
        if ev in (ord('W'), ord('w'), ord('Ц'), ord('ц')):
            if volume < 1:
                max_vol = 1
                screen.print_at('+',
                                14, 8, 1, 1)
                screen.print_at('-',
                                8, 8, 1)
                volume += 0.01
                pygame.mixer.music.set_volume(volume)
        elif ev in (ord('S'), ord('s'), ord('Ы'), ord('ы')):
            if volume > 0:
                min_vol = 1
                volume -= 0.01
                pygame.mixer.music.set_volume(volume)
                screen.print_at('+',
                                14, 8, 1)
                screen.print_at('-',
                                8, 8, 1, 1)
        elif ev in (ord('Q'), ord('q'), ord('Й'), ord('й')):
            if q > 0:
                i2 = 0
                q -= 1
                mixer.music.stop()
                pygame.event.clear()
                mixer.music.load(queue[q])
                mixer.music.play()
                screen.print_at('<<',
                                5, 8, 1, 1)
                playing = True
        elif ev in (ord('E'), ord('e'), ord('У'), ord('у')):
            if q < len(queue)-1:
                i2 = 0
                q += 1
                mixer.music.stop()
                pygame.event.clear()
                mixer.music.load(queue[q])
                mixer.music.play()
                screen.print_at('>>',
                                17, 8, 1, 1)
                playing = True
        else:
            if max_vol >= 2**13:
                max_vol = 0
                screen.print_at('+',
                                14, 8, 1)
            if min_vol >= 2**13:
                min_vol = 0
                screen.print_at('-',
                                8, 8, 1)
        # spinning animation
        if i % 40 == 0 and playing:
            screen.print_at('/',
                            7, 5, 7, 1)
            screen.print_at('/',
                            15, 5, 7, 1)
        elif i % 40 == 10 and playing:
            screen.print_at('-',
                            7, 5, 7, 1)
            screen.print_at('-',
                            15, 5, 7, 1)
        elif i % 40 == 20 and playing:
            screen.print_at('\\',
                            7, 5, 7, 1)
            screen.print_at('\\',
                            15, 5, 7, 1)
        elif i % 40 == 30 and playing:
            screen.print_at('|',
                            7, 5, 7, 1)
            screen.print_at('|',
                            15, 5, 7, 1)
        # show volume
        if volume > 0.9:
            screen.print_at('100%',
                            63, 3, 2, 1)
            screen.print_at('-+-',
                            63, 4, 0, 1)
        if 0.9 >= volume > 0.7:
            screen.print_at('-+- ',
                            63, 3, 0, 1)
            screen.print_at('80%',
                            63, 4, 2, 1)
            screen.print_at('-+-',
                            63, 5, 0, 1)
        if 0.7 >= volume > 0.5:
            screen.print_at('-+-',
                            63, 4, 0, 1)
            screen.print_at('60%',
                            63, 5, 2, 1)
            screen.print_at('-+-',
                            63, 6, 0, 1)
        if 0.5 >= volume > 0.3:
            screen.print_at('-+-',
                            63, 5, 0, 1)
            screen.print_at('40%',
                            63, 6, 2, 1)
            screen.print_at('-+-',
                            63, 7, 0, 1)
        if 0.3 >= volume > 0.1:
            screen.print_at('-+-',
                            63, 6, 0, 1)
            screen.print_at('20%',
                            63, 7, 2, 1)
            screen.print_at('-+-',
                            63, 8, 0, 1)
        if 0.1 >= volume:
            screen.print_at('-+-',
                            63, 7, 0, 1)
            screen.print_at('0% ',
                            63, 8, 2, 1)
        # visualizer animation
        left1 = round(abs(nps[q][1][math.floor(nps[q][0] * i2)+200] / nps[q][4] * 10))
        right1 = round(abs(nps[q][2][math.floor(nps[q][0] * i2)+200] / nps[q][5] * 10))
        if playing:
            screen.print_at('#' * left1,
                            26, 4, 7, 1)
            screen.print_at('+' * (10 - left1),
                            26 + left1, 4, 0, 1)
            screen.print_at('#' * right1,
                            26, 5, 7, 1)
            screen.print_at('+' * (10 - right1),
                            26 + right1, 5, 0, 1)
        screen.print_at('<<',
                        5, 8, 1)
        screen.print_at('>>',
                        17, 8, 1)

        if i % 2 == 1:
            i2 += 1
        i += 1
        min_vol *= 2
        max_vol *= 2
        screen.refresh()
        time.sleep(0.04)
# os.system('mode con: cols=37 lines=15')


Screen.wrapper(anim)
