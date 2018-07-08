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
    def add_time(self,hour, min, sub):
        obj = {}
        obj['h'] = hour
        obj['m'] = min
        obj['sub'] = sub
        obj['tag'] = ''
        self.times.append(obj)
    def add_tag_t(self, str):
        self.times[-1]['tag'] += str;
    def __init__(self, draw_string,w,h):
        delay = 0
        self.font3 = pygame.font.Font('NanumSquareRoundEB.ttf',self.font_size//2)
        self.font = pygame.font.Font('NanumSquareRoundEB.ttf',self.font_size)
        self.font2 = pygame.font.Font('NanumSquareRoundEB.ttf',int(self.font_size * 1.5))
        self.draw_string = draw_string

        self.add_time(6,20,'기상')
        self.add_time(6,40,"스트레칭")
        self.add_time(7,40,'아침 식사')
        self.add_tag_t('{아침}')
        self.add_time(8,15,'조례')
        self.add_time(8,40,'시험장 이동')
        self.add_time(9,00,'1교시')
        self.add_time(9,50,'쉬는시간')
        self.add_time(10,5,'2교시')
        self.add_time(10,55,'쉬는시간')
        self.add_time(11,10,'3교시')
        self.add_time(12,00,'점심시간')
        self.add_tag_t('{점심}')
        self.add_time(13,00,'')
        self.add_time(18,40,'져녁시간')
        self.add_tag_t('{저녁}')
        self.add_time(19,30,'')
        pygame.mixer.music.load('track 01.mp3')

        print(self.times)
    
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
        #set_color(dt)
        
        string = None
        next_time = None

        
        t_t = 0
        t_i = -1
        
        for t in self.times:
            if t['h'] * 60 + t['m'] < dt.hour * 60 + dt.minute:
                if t_t < t['h'] * 60 + t['m']:
                    string = t['sub']
                    t_i = t
                    t_t = t['h'] * 60 + t['m']
        t_tt = 24 * 60
        for t in self.times:
            if t_t < t['h'] * 60 + t['m'] < t_tt:
                t_tt = t['h'] * 60 + t['m']

        if self.space != 1:
            self.space += (1 - self.space) * 0.2
        if t_i != -1:
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
                        self.draw_string(self.font3,surf, s, y = (self.space - 1)*0.5*self.font_size*(-len(self.data)/2 +1 + i),  color = self.text_color)
                        i += 1
                    if self.space != 2.85:
                        self.space += (2.85 - self.space) * 0.4
            if t_i['tag'].find('{저녁}') < 0:
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(1)
            else:
                pygame.mixer.music.stop()
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
