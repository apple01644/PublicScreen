#!usr/bin python
from random import randint
from pygame.locals import *
import pygame, os, time, sys, traceback


c_black = (0,0,0)
c_white = (255,255,255)

class main:
    W = 0
    H = 0
    MAX_C_IN_L = 70
    act = {'init' : 'INIT'}
    def __init__(self, w, h):
        self.W = w
        self.H = h
        self.game()
        pygame.quit()
    def draw_string(self, font, the_surf, t, x = 0, y = 0, color = (0,0,0),alias = False, max_len = 0, w = 1.0, h = 1.0, back_color = (78,79,111), space = 200):
        
        s = ""
        ss = []
        for c in t:
            if ord(c) == 10:
                ss.append(s)
                s = ""
            else:
                if max_len != 0 and len(s) >= max_len:
                    ss.append(s)
                    s = ""
                else:
                    s += c
        #print(s)
        if len(s) > 0:
            ss.append(s)
        if len(ss) > 1:
            i = 0
            for sss in ss:
                self.draw_line(font, the_surf, sss, x = x, y = y + ((i - len(ss) / 2) / (len(ss) - 1)) * space, color = color, alias = alias, w = w, h = h,back_color = back_color)
                i += 1
        else:
            self.draw_line(font, the_surf, t, x = x, y = y, color = color, alias = alias, w = w, h = h,back_color = back_color)
    def draw_line(self, font, the_surf, t, x = 0, y = 0, color = (0,0,0),alias = False, w = 1.0, h = 1.0, back_color = (78,79,111)):
        block = font.render(t, alias, color)
        rect = block.get_rect()
        rect.center = the_surf.get_rect().center
        rect[0] += x
        rect[1] += y
        if back_color != (78,79,111):
            the_surf.fill(back_color, rect)
        the_surf.blit(block, (rect[0],rect[1],rect[2],rect[3]))
    def game(self):
        w = 1920
        h = 1080
        
        is_full = 1
        if is_full != 0:
            surf = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.DOUBLEBUF)
        else:
            surf = pygame.display.set_mode((w,h))
        act_names = []
        act_names.append('timer')

        
        #Activison
        for s in act_names:
            self.act[s] = 0
        error = ""
        
        #Imports
        surfs = [(0,) * 100]

        acts= {}
        for s in act_names:
            exec("import %s"%(s))
            print("acts['%s'] = (%s.%s(self.draw_string,self.W,self.H))"%(s,s,s))
            exec("acts['%s'] = (%s.%s(self.draw_string,self.W,self.H))"%(s,s,s))
        surfs[0] = pygame.Surface((1920 ,1080))
        #Standard
        color_text = (0,0,0)
        color_back = (255,255,255)

        font = pygame.font.Font('NanumSquareRoundEB.ttf', 30) 
        self.act['timer'] = 1
        GAME_ON = True
        while GAME_ON:
            actived = False
            for s in act_names:
                if self.act[s] == 1:
                    actived = True
                    break
            if not actived:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        GAME_ON = False
                        break
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            GAME_ON = False
                            break
                        if pygame.key.get_mods() & pygame.KMOD_LALT:
                            if event.key == K_1:
                                self.act['timer'] = 1
                                break
                        elif pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                            if event.key == K_1:
                                pygame.display.quit()
                                pygame.display.init()
                                surf = pygame.display.set_mode((0,0),pygame.FULLSCREEN|pygame.DOUBLEBUF)
                                break
                            elif event.key == K_2:
                                pygame.display.quit()
                                pygame.display.init()
                                surf = pygame.display.set_mode((w,h))
                                break
                        
                if error == "":
                    surf.fill((150,150,255))
                    self.draw_string(font, surf, "PLEASE HIT ESC!", color = (255,255,255),back_color = (150,150,255))
                elif error != "":
                    surf.fill((150,150,255))
                    self.draw_string(font, surf, error, max_len = self.MAX_C_IN_L, color = (255,0,0),back_color = (0,0,0), space = 230)
                    self.draw_string(font, surf, "PLEASE HIT ESC!", color = (255,255,255),back_color = (150,150,255) , y=- 200)
            else:     
                surf.fill((0,0,0))
                try:
                    for s in act_names:
                        if self.act[s] != 0:
                            if not acts[s].step(surfs[0]):
                                self.act[s] = 0
                except Exception as e:
                    for s in act_names:
                        self.act[s] = 0
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    error = traceback.format_exc()
                    error = error.replace(os.path.dirname(os.path.realpath(__file__)), ".")
                        
                #surfs[0]=pygame.transform.scale(surfs[0], (1920,1080))
                surf.blit(surfs[0], (0,0))
            
            pygame.display.update()

def the_main():
    pygame.init()
    pygame.font.init()
    
    w = 1920
    h = 1080
        
    global FPS_C,surf, GAME_ON, surf1
    FPS_C = pygame.time.Clock()
    cls_main = main(w,h)

#----- ----- ----- ----- ----- 
#----- ----- ----- ----- ----- 
#----- ----- ----- ----- -----
if __name__ == "__main__":
    the_main()
#----- ----- ----- ----- ----- 
#----- ----- ----- ----- ----- 
#----- ----- ----- ----- -----

















