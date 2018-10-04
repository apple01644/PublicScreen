import pygame, time, datetime
from pygame.locals import *
import re, random
import urllib.request
import get_food
from firebase import firebase
import moviepy.editor
from pygame.locals import *
import threading, time, pytube, os, shutil
import numpy as np
from moviepy.decorators import requires_duration

class timer:
    FONT_SIZE =  100
    times = []
    dates = []
    back_color = (5,5,0)
    text_color = (255,255,255)
    fb = None
    W = 0
    H = 0

    lt_life = 1

    food = None

    wait_image = None

    movie = None
    movie_start = 0
    movie_run = False
    movie_play = False
    movie_buf = None
    movie_title = ''
    
    right_text = ''
    rt_life = 0
    rt_cursor = 0
    
    tube_list = ''
    tube_key = ''
    tube_csr = 0
    tube_busy = False
    tube_queue = False
    tube_title = ''
    
    force_play_movie = False

    def get_youtube(self, link):
        self.tube_busy = True
        try:
            yt = pytube.YouTube(link)
            self.tube_title = yt.title
            flt = yt.streams.filter(mime_type='video/mp4', audio_codec='mp4a.40.2')
            flt.first().download('',filename='queue')
        except:
            self.tube_busy = False
            print('Failed download')
            return
        self.tube_queue = True
        self.tube_busy = False
        
        
    def add_time(self,hour, minute, sub,tag=''):
        obj = {'h' : hour, 'm' : minute, 'sub' : sub, 'tag' : tag}
        self.times.append(obj)
    def add_tag_t(self, str):
        self.times[-1]['tag'] += str
    def __init__(self, draw_string,w,h):
        self.W, self.H = w, h

        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        random.seed(int(time.time() * 10000000 % 100000))

        self.wait_image = pygame.image.load("dgsw.png")

        self.fb = firebase.FirebaseApplication('https://public-screen.firebaseio.com', None)
        
        delay = 0
        self.font3 = pygame.font.Font('NanumSquareRoundEB.ttf',self.FONT_SIZE//2)
        self.font4 = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE//4)
        self.font6 = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE//3)
        self.font = pygame.font.Font('NanumSquareRoundEB.ttf',self.FONT_SIZE)
        self.font5 = pygame.font.Font('NanumSquareRoundEB.ttf',self.FONT_SIZE * 4 // 5)
        self.font2 = pygame.font.Font('NanumSquareRoundEB.ttf',int(self.FONT_SIZE * 1.5))
        self.draw_string = draw_string

        self.add_time(6,20,'기상',tag='{평일}{아침}')
        self.add_time(6,30,"아침점호",tag='{평일}{아침}')
        self.add_time(7,20,'아침 식사',tag='{평일}{아침}')
        self.add_time(7,50,'등교',tag='{평일}{자율}')
        self.add_time(8,30,'조례',tag='{평일}')
        
        self.add_time(8,40,'1교시',tag='{평일}')
        self.add_time(9,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(9,40,'2교시',tag='{평일}')
        self.add_time(10,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(10,40,'3교시',tag='{평일}{점심}')
        self.add_time(11,30,'쉬는시간',tag='{평일}{점심}{자율}')
        self.add_time(11,40,'4교시',tag='{평일}{점심}')
        self.add_time(12,30,'점심시간',tag='{평일}{점심}{자율}')
        
        
        self.add_time(13,20,'5교시',tag='{평일}')
        self.add_time(14,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(14,20,'6교시',tag='{평일}')
        self.add_time(15,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(15,20,'7교시',tag='{평일}')
        
        self.add_time(16,10,'종례 및 청소',tag='{평일}{저녁}')
        
        self.add_time(16,30,'8교시',tag='{평일}{저녁}')
        self.add_time(17,20,'쉬는시간',tag='{평일}{저녁}{자율}')
        self.add_time(17,30,'9교시',tag='{평일}{저녁}')
        
        self.add_time(18,20,'저녁시간',tag='{평일}{저녁}{자율}')
        self.add_time(19,10,'자율1교시',tag='{평일}')
        self.add_time(20,00,'쉬는시간',tag='{평일}{자율}')
        self.add_time(20,10,'자율2교시',tag='{평일}')

        self.add_time(21,00,'기숙사 이동',tag='{평일}{자율}')
        self.add_time(21,20,'개인시간',tag='{평일}{자율}')
        self.add_time(22,20,'저녁점호',tag='{평일}')
        self.add_time(22,30,'',tag='{평일}')

        self.add_time(8,10,'아침점호',tag='{휴일}{아침}')
        self.add_time(8,30,'오전일과',tag='{휴일}{자율}{점심}')
        self.add_time(12,40,'점심시간',tag='{휴일}{자율}{점심}')
        self.add_time(13,20,'오후일과',tag='{휴일}{자율}{저녁}')
        self.add_time(18,00,'저녁시간',tag='{휴일}{자율}{저녁}')
        self.add_time(19,10,'야간일과',tag='{휴일}{자율}')
        self.add_time(21,20,'개인시간',tag='{휴일}{자율}')
        self.add_time(21,40,'저녁점호',tag='{휴일}')
        self.add_time(21,50,'',tag='{휴일}')
    def tag_cond(self, t, dt):
        r = False
        if t['tag'].find('{평일}')>=0 and dt.weekday() < 5:
            r = True
        if t['tag'].find('{휴일}')>=0 and dt.weekday() >= 5:
            r = True
        return r

    def play_audio(self, clip, fps=22050,  buffersize=4000, nbytes=2, audioFlag=None,videoFlag=None):
                 
        pygame.mixer.quit()
        
        pygame.mixer.init(fps, -8 * nbytes, clip.nchannels, 1024)
        totalsize = int(fps*clip.duration)
        pospos = np.array(list(range(0, totalsize,  buffersize))+[totalsize])
        tt = (1.0/fps)*np.arange(pospos[0], pospos[1])
        sndarray = clip.to_soundarray(tt, nbytes=nbytes, quantize=True)
        chunk = pygame.sndarray.make_sound(sndarray)
        
        if (audioFlag is not None) and (videoFlag is not None):
            audioFlag.set()
            videoFlag.wait()
            
        channel = chunk.play()
        i = 1
        while i < len(pospos)-1:
            while not self.movie_play:
                i = 1 + int((len(pospos)-3) * (time.time() - self.movie_start) / clip.duration)
            tt = (1.0/fps)*np.arange(pospos[i], pospos[i+1])
            sndarray = clip.to_soundarray(tt, nbytes=nbytes, quantize=True)
            chunk = pygame.sndarray.make_sound(sndarray)
            while channel.get_queue():
                time.sleep(0.003)
                if videoFlag is not None:
                    if not videoFlag.is_set():
                        channel.stop()
                        del channel
                        return
            channel.queue(chunk)
            i += 1

    def play_tube(self):
        if self.movie.audio != None:
            videoFlag = threading.Event()
            audioFlag = threading.Event()
            audiothread = threading.Thread(target=self.play_audio, args=(self.movie.audio, 22050, 3000, 2, audioFlag, videoFlag))
            audiothread.start()
            videoFlag.set()
            audioFlag.wait()
        self.movie_run = True
        self.movie_start = time.time()

    def next_tube(self):
        self.tube_csr += 1
        if self.tube_csr >= len(self.tube_key):
            self.tube_list = self.fb.get('tube', None)
            self.tube_key = list(self.tube_list.keys())
            random.shuffle(self.tube_key, random.random)
            for _ in self.tube_key:
                print(_)
            self.tube_csr = 0
        j = 0
        for _ in self.tube_key:
            if j == self.tube_csr:
                threading.Thread(target=self.get_youtube,args=(self.tube_list[_],)).start()
                break
            j += 1

    def env_set(self, t_i):
        if 6 < t_i['h'] <= 18:
            r,g,b = self.text_color
            if r > 0:
                r -= 1
            if g > 0:
                g -= 1
            if b > 0:
                b -= 1
            self.text_color = (r,g,b)
            r,g,b = self.back_color
            if r < 250:
                r += 1
            if g < 250:
                g += 1
            if b < 250:
                b += 1
            self.back_color = (r,g,b)
        else:
            r,g,b = self.text_color
            if r < 250:
                r += 1
            if g < 250:
                g += 1
            if b < 250:
                b += 1
            self.text_color = (r,g,b)
            r,g,b = self.back_color
            if r > 0:
                r -= 1
            if g > 0:
                g -= 1
            if b > 0:
                b -= 1
            self.back_color = (r,g,b)


    def step(self, surf):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.force_play_movie = not self.force_play_movie
                    print('PRESS Space')
                if event.key == K_q:
                    return False
                    break
        
        surf.fill(self.back_color)
        
        dt = datetime.datetime.now() + datetime.timedelta(seconds=29 + 5)        
        string = None
        next_time = None

        t_t = 0
        t_i = -1
        for t in self.times:
            if t['h'] * 60 + t['m'] <= dt.hour * 60 + dt.minute:
                if t_t < t['h'] * 60 + t['m']:
                    if self.tag_cond(t, dt):
                        string = t['sub']
                        t_i = t
                        t_t = t['h'] * 60 + t['m']
        
        t_tt = 24 * 60
        for t in self.times:
            if t_t < t['h'] * 60 + t['m'] < t_tt:
                if self.tag_cond(t, dt):
                    t_tt = t['h'] * 60 + t['m']

        if self.lt_life != 1:
            self.lt_life += (1 - self.lt_life) * 0.2

        if t_i != -1:
            self.env_set(t_i)
            if t_i['tag'].find('{아침}') >= 0 or t_i['tag'].find('{점심}') >= 0 or t_i['tag'].find('{저녁}') >= 0:
                if self.food == None:
                    if t_i['tag'].find('{아침}') >= 0:
                        self.food = get_food.get_food(0)
                    elif t_i['tag'].find('{점심}') >= 0:
                        self.food = get_food.get_food(1)
                    elif t_i['tag'].find('{저녁}') >= 0:
                        self.food = get_food.get_food(2)
                else:
                    i = 0
                    for s in self.food:
                        self.draw_string(self.font3,surf, s,x=-self.FONT_SIZE*3.5, y = (self.lt_life - 1)*0.5*self.FONT_SIZE*(-len(self.food)/2 + 0.5 + i),  color = self.text_color)
                        i += 1
                    if self.lt_life != 2.85:
                        self.lt_life += (2.85 - self.lt_life) * 0.4
            else:
                self.food = None
            if string != '' and string != None:
                self.draw_string(self.font5,surf,string,x=-self.FONT_SIZE*3.5,y=-self.FONT_SIZE*self.lt_life,  color = self.text_color)
                ddt = datetime.datetime(year = dt.year, month = dt.month, day = dt.day,hour = t_tt // 60, minute = t_tt % 60) - dt
                if ddt.seconds // 60 >= 60:
                    string = "%s:%s:%s"%("{:02d}".format(ddt.seconds // 3600),"{:02d}".format((ddt.seconds // 60) % 60), "{:02d}".format(ddt.seconds % 60))
                else:
                    string = "%s:%s"%("{:02d}".format((ddt.seconds // 60)), "{:02d}".format(ddt.seconds % 60))
                self.draw_string(self.font,surf,string,x=-self.FONT_SIZE*3.5,y=self.FONT_SIZE*self.lt_life,  color = self.text_color)
                temp_y = -self.H // 4
                if self.rt_life < 200:
                    temp_y+=self.FONT_SIZE*(((200 - self.rt_life) / (200)) ** 2 * 6)
                elif self.rt_life > 1000 - 200:
                    temp_y-=self.FONT_SIZE*(((1000 - 200 - self.rt_life) / (200)) ** 2 * 6)

                if self.right_text != None:
                    j = 0
                    for _ in self.right_text:
                        if j == self.rt_cursor:
                            i = 0
                            lines = self.right_text[_].split('\\n')
                            for s in lines:
                                self.draw_string(self.font3,surf, s,x=self.W // 4, y = temp_y+0.5*self.FONT_SIZE*(i - (len(lines) - 1) / 2),  color = self.text_color)
                                i += 1
                            break
                        j += 1
                self.draw_string(self.font6,surf,'http://대소고.oa.to/',x=-self.W * 0.25,y = self.H / 2 - self.FONT_SIZE / 2, color = self.text_color)
                
                if self.movie == None:
                    self.movie_play = False
                    if self.tube_queue:
                        if t_i['tag'].find('{자율}') >= 0 or self.force_play_movie:
                            shutil.copy2('queue.mp4','play.mp4')
                            self.movie = moviepy.editor.VideoFileClip('play.mp4')
                            self.movie_title = self.tube_title
                            self.tube_quere = False
                            self.play_tube()
                        else:
                            pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                            surf.blit(self.wait_image, (640,360))
                    else:
                        pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                        surf.blit(self.wait_image, (640,360))
                        if not self.tube_busy:
                            self.next_tube()
                elif t_i['tag'].find('{자율}') >= 0 or self.force_play_movie:
                    if self.movie_run:
                        #Video run
                        if time.time() - self.movie_start < self.movie.duration-.001:
                            pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                            self.movie_buf = pygame.transform.scale(pygame.surfarray.make_surface(self.movie.get_frame(time.time() - self.movie_start).swapaxes(0, 1)), (640 * (360 - self.FONT_SIZE // 2) // 360,360 - self.FONT_SIZE // 2))
                            if self.movie_buf != None:
                                surf.blit(self.movie_buf, (640 + 640 * self.FONT_SIZE // 4 // 360, 360))
                            
                            pygame.draw.rect(surf, self.back_color, (640,720-self.FONT_SIZE // 4- self.FONT_SIZE / 4,640,self.FONT_SIZE // 4 + self.FONT_SIZE / 4))
                            PADD = 2
                            pygame.draw.rect(surf, self.text_color,(640 + PADD, 720 - self.FONT_SIZE // 2 + PADD,max(int(640 * (time.time() - self.movie_start) / self.movie.duration + 1) - PADD * 2,0), self.FONT_SIZE // 4 + self.FONT_SIZE / 4 - PADD * 2))
                            self.draw_string(self.font4,surf,self.movie_title,x=self.W * 0.25,y = self.H / 2 - self.FONT_SIZE / 3, color = self.text_color, max_len = 60, back_color = self.back_color)
                            self.movie_play = True
                        else: #Video End
                            self.movie_play = False
                            if self.tube_queue:
                                self.movie.close()
                                try:
                                    os.remove('play.mp4')
                                    shutil.copy2('queue.mp4','play.mp4')
                                    self.movie = moviepy.editor.VideoFileClip('play.mp4')
                                    self.movie_title = self.tube_title
                                    self.tube_queue = False
                                    self.movie_run = False
                                except:
                                    print('failed remove')
                            else:
                                pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                                surf.blit(self.wait_image, (640,360))
                    else:
                        self.play_tube()
                        self.movie_play = False
                    if not (self.tube_queue or self.tube_busy):
                        self.next_tube()
                else:
                    pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                    surf.blit(self.wait_image, (640,360))
                    self.movie_play = False
            else:
                surf.blit(self.wait_image, (320,180))
            
        if self.rt_life == 0:
            self.rt_life = 1000
            self.rt_cursor += 1
            if self.rt_cursor >= len(self.right_text):
                self.right_text = self.fb.get('notice', None)
                self.rt_cursor = 0
                

        self.rt_life -= 1
        return True     
