# -*- coding: utf-8 -*-
#python的基本思想1：万物皆对象（解释器给每一个对象都分配了一个ID），变量即引用（类的变量也是引用），对象中只有字典和列表可以修改（也就是说相同的ID可以对应不同的对象）!!!
#python的基本思想2，修改变量分为两种，一种是把引用给了另一个对象，另一种是把对象修改掉了，
#表现出来，函数的参数为列表或字典、类！！修改形参实参也变，函数的参数为其他时修改形参实参不变（用全局变量才能解决）

#飞机越来越小，屏幕横线，飞机越来越快，飞机发射子弹，对子弹 ,隐形飞机,子弹没打着
#帧数,暂停,私有成员

import pygame #导入pygame库
from sys import exit #向sys模块借一个exit函数用来退出程序
import random
import threading #多线程
import time

#宏
MACRO_WINSIZE_X = 450
MACRO_WINSIZE_Y = 600
NORMAL = 0
SPE = 1

#-----------------函数-------------------------------------------
#显示文字 
# Input：surface_handle：surface句柄 
# pos：文字显示位置 
# color:文字颜色 
# font_bold:是否加粗 
# font_size:字体大小 
# font_italic:是否斜体 
# Output: NONE 
def show_text(surface_handle, pos, text, color, font_bold = False, font_size = 32, font_italic = False):            
    #获取系统字体，并设置文字大小  
    cur_font = pygame.font.SysFont('SimHei', font_size)       
    #设置是否加粗属性  
    cur_font.set_bold(font_bold)     
    #设置是否斜体属性  
    cur_font.set_italic(font_italic)     
    #设置文字内容  
    text_fmt = cur_font.render(text, 1, color)    
    #绘制文字  
    surface_handle.blit(text_fmt, pos) 
    
#-----------------数据结构-------------------------------------------
class background : #背景类
    def __init__(self):
        self.pic = pygame.image.load('back1.jpg').convert()
    def draw(self) :
        screen.blit(self.pic, (0,0)) #将背景图画上去
        
class timer (threading.Thread): #计时器线程类
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.fpscounter = 0
        self.fpsmem = 0
        self.stop_flag = False
    def run(self):
        while True:
            if self.stop_flag == True:
                return
            else:
                time.sleep(1)
                self.fpsmem = self.fpscounter  
                self.fpscounter = 0
    def fps_count(self):
        self.fpscounter += 1
    def draw_fps(self):
        show_text(screen, (350, 20), "fps: {0:d}".format(self.fpsmem), (90, 110, 130), False, 18) 
    def stop_thread(self):
        self.stop_flag = True
        
class refree : #裁判类
    def __init__(self):
        self.goal = 0
        self.status = 0
        self.mouse_pic = pygame.image.load('hand.png').convert_alpha()
        self.line_pic = pygame.image.load('line.png').convert_alpha()
        self.y_line = 100
    def move_line(self):
        self.y_line += 0.02
    def add_goal(self, bullet_box, enemy_box):
        if self.status == 3:
            self.goal += 1
        elif self.status == 1:
            self.goal += 8
        else:
            self.goal += 5
        if self.goal >= 100:
            self.next(bullet_box, enemy_box)
    def remove_goal(self):
        self.goal -= 50
    def explode_or_not(self, bullet_box, enemy_box) :
        for bullet in bullet_box.list :
            for enemy in enemy_box.list:
                if bullet.x > enemy.x and bullet.x < enemy.x + enemy_box.pic.get_width() and bullet.y > enemy.y and bullet.y < enemy.y + enemy_box.pic.get_height() : #击中敌机  
                    bullet_box.del_bullet(bullet)
                    enemy_box.del_enemy(enemy)
                    self.add_goal(bullet_box, enemy_box)
                    return
    def lose_or_not(self, plane, enemy_box):
        for enemy in enemy_box.list:
            if plane.x > enemy.x - plane.pic.get_width() + 12 and \
            plane.x < enemy.x + enemy_box.pic.get_width() - 12 and \
            plane.y > enemy.y - plane.pic.get_height() + 12 and \
            plane.y < enemy.y + enemy_box.pic.get_height() - 12:#相撞
                self.status = 7
                background.pic = pygame.image.load('back7.jpg').convert()
        if (self.status == 3 or self.status == 4 or self.status == 5) and plane.y < self.y_line - 3 :#越过白线
            self.status = 7
            background.pic = pygame.image.load('back7.jpg').convert()
    def display(self):
        show_text(screen, (12, MACRO_WINSIZE_Y - 60), " 得分：{0:d}".format(self.goal), (90, 110, 130))      
    def draw_line(self):
        screen.blit(self.line_pic, (0, self.y_line))
    def next(self, bullet_box, enemy_box):
        self.status += 1
        if self.status > 7:
            self.status = 1
        bullet_box.set_to_zero()
        enemy_box.set_to_zero()
        self.goal = 0
        if self.status < 4:
            enemy_box.pic = pygame.image.load('enemy.png').convert_alpha()
        if self.status == 4 or self.status == 5:
            self.y_line = 400
            enemy_box.pic = pygame.image.load('enemy2.png').convert_alpha()
        if self.status == 6:
            background.pic = pygame.image.load('back6.jpg').convert()
            
class bullet : #子弹类
    def __init__(self, x, y, speed = 1):
        self.x = x
        self.y = y
        self.speed = speed
    def move(self):   
        self.y -= self.speed

class bullet_set : #子弹容器类
    def __init__(self):
        self.list = [];
        self.pic = pygame.image.load('bullet.png').convert_alpha()
    def set_to_zero(self):
        self.list = [];
    def add_bullet(self, new_bullet):
        self.list.append(new_bullet)
    def del_bullet(self, bullet):
        self.list.remove(bullet)
    def all_move(self, refree):
        for bullet in self.list:
            if bullet.y < - self.pic.get_height():
                self.del_bullet(bullet)
                refree.remove_goal()
            else : 
                bullet.move()
    def draw(self): 
        for bullet in self.list:
            screen.blit(self.pic, (bullet.x, bullet.y))
        
class plane : #飞机类,fire结构不是很好以后再说吧
    def __init__(self): 
        self.x = 0
        self.y = 0
        self.pic = pygame.image.load('plane.png').convert_alpha() 
    def update(self): 
        x_mouse, y_mouse = pygame.mouse.get_pos()
        self.x = x_mouse - self.pic.get_width() / 2
        self.y = y_mouse - self.pic.get_height() / 2
    def fire(self, bullet_box, status) :
        if status == 3 and len(bullet_box.list) > 0:
            return
        else:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = x_mouse - bullet_box.pic.get_width() / 2
            y = y_mouse - bullet_box.pic.get_height() / 2 - self.pic.get_height() / 2 
            if status == 3:
                bullet_box.add_bullet(bullet(x, y, 0.5))
            else:
                bullet_box.add_bullet(bullet(x, y))
            return
    def draw(self) :
        screen.blit(self.pic, (self.x, self.y))
        
class enemy : #敌机类
    def __init__(self, pic_size_x, pic_size_y, speed = random.uniform(0.25, 0.35), enemy_type = 0): 
        self.x = random.randint(0, MACRO_WINSIZE_X - pic_size_x)
        self.y = - pic_size_y
        self.speed = speed
        self.enemy_type = enemy_type #1代表特殊类型飞机
        self.count = random.uniform(1, 600)#特殊飞机飞行轨迹需要的计数器
    def move(self):
        if self.enemy_type == SPE:
            self.count += 1
            if self.count % 600 < 300:
                self.x += random.uniform(0.9, 1.1)
            else:
                self.x -= random.uniform(0.9, 1.1)            
        self.y += self.speed         

class enemy_set: #敌机容器类
    def __init__(self):
        self.list = []
        self.pic = pygame.image.load('enemy.png').convert_alpha() 
        self.count_time = 0
        self.counter = 0
    def set_to_zero(self):
        self.list = []
        self.count_time = 0
        self.counter = 0
    def draw(self):
        for enemy in self.list:
            screen.blit(self.pic, (enemy.x, enemy.y))
    def add_enemy(self, new_enemy):
        self.list.append(new_enemy)
        self.counter += 1
    def del_enemy(self, enemy):
        self.list.remove(enemy)
    def all_move(self, refree):
        for enemy in self.list:
            if enemy.y > MACRO_WINSIZE_Y:
                self.del_enemy(enemy)
                refree.remove_goal()
            else:
                enemy.move()
    def create_enemy(self, refree):
        self.count_time -= 1
        if self.count_time <= 0:
            if refree.status == 1:
                if self.counter % 10 == 8:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), 1.5))
                    self.count_time = random.randint(800, 1500)
                else:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height()))
                    self.count_time = random.randint(800, 1500)
            elif refree.status == 2:
                if self.counter % 9 == 7 or self.counter % 4 == 3 or self.counter % 25 == 24 or self.counter % 31 == 25:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), 0.3, SPE))
                    self.count_time = random.randint(100, 1500)
                else:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), random.uniform(0.3, 0.7)))
                    self.count_time = random.randint(100, 1000)
            elif refree.status == 3:
                self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), random.uniform(0.05, 0.13)))
                self.count_time = random.randint(100, 200)
            elif refree.status == 4:
                self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), random.uniform(0.1, 0.18)))
                self.count_time = random.randint(200, 250)
            elif refree.status == 5:
                if  self.counter % 9 == 7:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), 0.1, SPE))
                    self.count_time = random.randint(500, 1500)
                else:
                    self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), random.uniform(0.1, 0.17)))
                    self.count_time = random.randint(100, 1000) 
#-----------------库初始化-------------------------------------------
pygame.init() #初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((MACRO_WINSIZE_X, MACRO_WINSIZE_Y), 0, 32) #创建了一个窗口,窗口大小和背景图片大小一样
pygame.display.set_caption("Hello, World!") #设置窗口标题
# pygame.mouse.set_visible(False)

#----------------初始化fps子线程------------------------------------------
thread_fps = timer(1, "fps_test")
thread_fps.start()

#----------------变量初始化------------------------------------------                
background = background() #初始化背景图片       
plane = plane() #初始化飞机
bullet_box = bullet_set() #初始化子弹容器
enemy_box = enemy_set() #初始化敌机容器
refree = refree() #初始化裁判

#-----------------游戏主循环-------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#接收到退出事件后退出程序
            thread_fps.stop_thread()
            thread_fps.join()
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            if (refree.status == 0 or refree.status == 7) and x_mouse > 130 and y_mouse > 390 and x_mouse < 310 and y_mouse < 450:
                refree.next(bullet_box, enemy_box)
                background.pic = pygame.image.load('back.jpg').convert()
                refree.y_line = 100
            elif refree.status > 0 :
                plane.fire(bullet_box, refree.status)
    
    background.draw() 
    thread_fps.fps_count()
    thread_fps.draw_fps()
    if refree.status == 0 or refree.status == 7:   
        x_mouse, y_mouse = pygame.mouse.get_pos()
        if x_mouse > 130 and y_mouse > 390 and x_mouse < 310 and y_mouse < 450:
            screen.blit(refree.mouse_pic, (x_mouse - 4, y_mouse - 3))
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)
    elif refree.status == 1:
        show_text(screen, (240, MACRO_WINSIZE_Y - 60), "Ⅰ 随便玩玩", (90, 110, 130))
        refree.display()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.explode_or_not(bullet_box, enemy_box)
        refree.lose_or_not(plane, enemy_box)
    elif refree.status == 2:
        show_text(screen, (240, MACRO_WINSIZE_Y - 60), "Ⅱ 好戏开始了", (90, 110, 130))
        refree.display()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.explode_or_not(bullet_box, enemy_box)
        refree.lose_or_not(plane, enemy_box)
    elif refree.status == 3:
        show_text(screen, (240, MACRO_WINSIZE_Y - 60), "Ⅲ 去撞白线", (90, 110, 130))
        refree.display()
        refree.move_line()
        refree.draw_line()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.explode_or_not(bullet_box, enemy_box)
        refree.lose_or_not(plane, enemy_box)
    elif refree.status == 4:
        show_text(screen, (240, MACRO_WINSIZE_Y - 60), "Ⅳ 我变大了", (90, 110, 130))
        refree.display()
        refree.draw_line()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.explode_or_not(bullet_box, enemy_box)
        refree.lose_or_not(plane, enemy_box)
    elif refree.status == 5 :
        show_text(screen, (240, MACRO_WINSIZE_Y - 60), "Ⅴ 放松一下", (90, 110, 130))
        refree.display()
        refree.draw_line()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.explode_or_not(bullet_box, enemy_box)
        refree.lose_or_not(plane, enemy_box)
    pygame.display.update()#刷新一下画面
