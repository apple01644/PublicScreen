import pygame, time, datetime
from pygame.locals import *
import re
import urllib.request
import get_food

class timer:
    font = 0
    draw_string = 0
    font_size =  130
    times = []
    dates = []
    back_color = (5,5,0)
    text_color = (255,255,255)
    tick = 0
    space = 1
    change = 0
    last_t = -1
    data = -1
    def add_time(self,hour, min, sub,tag=''):
        obj = {}
        obj['h'] = hour
        obj['m'] = min
        obj['sub'] = sub
        obj['tag'] = tag
        self.times.append(obj)
    def add_tag_t(self, str):
        self.times[-1]['tag'] += str;
    def __init__(self, draw_string,w,h):
        delay = 0
        self.font3 = pygame.font.Font('NanumSquareRoundEB.ttf',self.font_size//2)
        self.font = pygame.font.Font('NanumSquareRoundEB.ttf',self.font_size)
        self.font2 = pygame.font.Font('NanumSquareRoundEB.ttf',int(self.font_size * 1.5))
        self.draw_string = draw_string

        self.add_time(6,20,'기상',tag='{평일}{아침}')
        self.add_time(6,30,"스트레칭",tag='{평일}{아침}')
        self.add_time(7,20,'아침 식사',tag='{평일}{아침}')
        self.add_time(7,50,'등교',tag='{평일}')
        self.add_time(8,20,'조례',tag='{평일}')
        self.add_time(8,30,'쉬는 시간',tag='{평일}')
        self.add_time(8,35,'1교시',tag='{평일}')
        self.add_time(9,25,'쉬는시간',tag='{평일}')
        self.add_time(9,40,'2교시',tag='{평일}')
        self.add_time(10,30,'쉬는시간',tag='{평일}')
        self.add_time(10,45,'3교시',tag='{평일}{점심}')
        self.add_time(11,35,'쉬는시간',tag='{평일}{점심}')
        self.add_time(11,50,'4교시',tag='{평일}{점심}')
        self.add_time(12,40,'점심시간',tag='{평일}{점심}')
        
        
        self.add_time(13,30,'5교시',tag='{평일}')
        self.add_time(14,20,'쉬는시간',tag='{평일}')
        self.add_time(14,35,'6교시',tag='{평일}')
        self.add_time(15,25,'쉬는시간',tag='{평일}')
        self.add_time(15,40,'7교시',tag='{평일}')
        
        self.add_time(16,30,'종례 및 청소',tag='{평일}')
        
        self.add_time(16,50,'8교시',tag='{평일}')
        self.add_time(17,40,'쉬는시간',tag='{평일}{저녁}')
        self.add_time(17,50,'9교시',tag='{평일}{저녁}')
        
        self.add_time(18,40,'져녁시간',tag='{평일}{저녁}')
        self.add_time(19,30,'자율1교시',tag='{평일}')
        self.add_time(20,20,'쉬는시간',tag='{평일}')
        self.add_time(20,30,'자율2교시',tag='{평일}')

        self.add_time(21,20,'기숙사 이동',tag='{평일}')
        self.add_time(21,30,'개인시간',tag='{평일}')
        self.add_time(22,20,'점호',tag='{평일}')
        self.add_time(22,30,'',tag='{평일}')

        pygame.mixer.music.load('track 01.mp3')

    def tag_cond(self, t, dt):
        r = False
        if t['tag'].find('{평일}')>=0 and dt.weekday() < 5:
            r = True
        if t['tag'].find('{휴일}')>=0 and dt.weekday() >= 5:
            r = True
        return r
    def env_set(self, t_i):
        if t_i['tag'].find('{아침}') >= 0 or t_i['tag'].find('{점심}') >= 0  or t_i['tag'].find('{저녁}') >= 0 :
            if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(1)
        elif pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
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
            if r < 255:
                r += 1
            if g < 255:
                g += 1
            if b < 255:
                b += 1
            self.back_color = (r,g,b)
        else:
            r,g,b = self.text_color
            if r < 255:
                r += 1
            if g < 255:
                g += 1
            if b < 255:
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
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                return False
                break
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.swit0 = not self.swit0
                    break
                elif event.key == K_ESCAPE:
                    return False
                    break
        
        surf.fill(self.back_color)
        
        dt = datetime.datetime.now()        
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

        if self.space != 1:
            self.space += (1 - self.space) * 0.2
        if t_i != -1:
            self.env_set(t_i)
            if t_i['tag'].find('{아침}') >= 0 or t_i['tag'].find('{점심}') >= 0 or t_i['tag'].find('{저녁}') >= 0:
                if self.change > 290:
                    if t_i['tag'].find('{아침}') >= 0:
                        self.data = get_food.get_food(0)
                        self.change = 0
                    elif t_i['tag'].find('{점심}') >= 0:
                        self.data = get_food.get_food(1)
                        self.change = 0
                    elif t_i['tag'].find('{저녁}') >= 0:
                        self.data = get_food.get_food(2)
                        self.change = 0
                if self.change == 0 and self.data != -1:
                    i = 0
                    for s in self.data:
                        self.draw_string(self.font3,surf, s, y = (self.space - 1)*0.5*self.font_size*(-len(self.data)/2 + 0.5 + i),  color = self.text_color)
                        i += 1
                    if self.space != 2.85:
                        self.space += (2.85 - self.space) * 0.4

        if string != '':
            self.draw_string(self.font,surf,string,y=-self.font_size*self.space,  color = self.text_color)
            ddt = datetime.datetime(year = dt.year, month = dt.month, day = dt.day,hour = t_tt // 60, minute = t_tt % 60) - dt
            if ddt.seconds // 60 >= 60:
                string = "%s:%s:%s"%("{:02d}".format(ddt.seconds // 3600),"{:02d}".format((ddt.seconds // 60) % 60), "{:02d}".format(ddt.seconds % 60))
            else:
                string = "%s:%s"%("{:02d}".format((ddt.seconds // 60)), "{:02d}".format(ddt.seconds % 60))
            self.draw_string(self.font,surf,string,y=self.font_size*self.space,  color = self.text_color)
        else:
            string = 'Sleep'
            if self.tick % 80 < 20:
                string += '.'
            elif self.tick % 80 < 40:
                string += '..'
            elif self.tick % 80 < 60:
                string += '...'
            self.draw_string(self.font,surf,string,  color = self.text_color)
        if self.last_t != t_i:
            self.change = 300
            self.data = -1
        self.last_t = t_i
        if self.change > 0:
            self.change -= 1
            
        self.tick = (self.tick + 1) % (32768)
        return True     
