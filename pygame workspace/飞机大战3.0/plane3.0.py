# -*- coding: utf-8 -*-
#飞机大战第三版
#python的基本思想1：万物皆对象（解释器给每一个对象都分配了一个ID），变量即引用（类的变量也是引用），对象中只有字典和列表可以修改（也就是说相同的ID可以对应不同的对象）!!!
#python的基本思想2，修改变量分为两种，一种是把引用给了另一个对象，另一种是把对象修改掉了，
#表现出来，函数的参数为列表或字典、类！！修改形参实参也变，函数的参数为其他时修改形参实参不变（用全局变量才能解决）

#------------------库-----------------------------------------------
import pygame #导入pygame库
from sys import exit #向sys模块借一个exit函数用来退出程序
import random
import time

#------------------常量---------------------------------------------
WINSIZE_X = 450 #窗口的宽
WINSIZE_Y = 600 #窗口的高
STRAIGHT = 0 #飞机类型
LEFTANDRIGHT = 1 #飞机类型,有一部分左右摆动
FPSLIMIT = 100 #帧数控制,可以直接修改
SMALL = 0 #敌机大小
LARGE = 1

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
class bullet : #子弹类
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed 
        
    def move(self, time):   
        self.y -= self.speed / 1000 * time
 
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
            bullet.move(refree.time_passed)
                
    def draw(self): 
        for bullet in self.list:
            screen.blit(self.pic, (bullet.x, bullet.y))
 
class enemy : #敌机类
    def __init__(self, pic_size_x, pic_size_y, speed, enemy_type): 
        self.x = random.randint(0, WINSIZE_X - pic_size_x)
        self.y = - pic_size_y
        self.speed = speed
        self.enemy_type = enemy_type #1代表特殊类型飞机
        self.count = random.uniform(1, int(1.7 * FPSLIMIT))#特殊飞机飞行轨迹需要的计数器
    def move(self, time):
        if self.enemy_type == LEFTANDRIGHT:
            self.count += 1
            if self.count % (1.7 * FPSLIMIT) < (0.85 * FPSLIMIT):
                self.x += random.uniform(304 / FPSLIMIT, 320 / FPSLIMIT)
            else:
                self.x -= random.uniform(304 / FPSLIMIT, 320 / FPSLIMIT)            
        self.y += self.speed / 1000 * time
  
class enemy_set: #敌机容器类
    def __init__(self):
        self.list = []
        self.pic = pygame.image.load('enemy.png').convert_alpha() 
        self.count_time = 0 #产生飞机帧数间隔
        self.counter = 0 #出现飞机的个数
        
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
            enemy.move(refree.time_passed)
            
    def create_enemy(self, refree):
        self.count_time -= 1
        if self.count_time <= 0: #创建一个敌机
            #查表
            if "enemy_spe_divisor" in refree.level[refree.status] and \
            self.counter % refree.level[refree.status]["enemy_spe_divisor"] == refree.level[refree.status]["enemy_spe_remainder"]: #产生特殊飞机
                enemy_speed1 = refree.level[refree.status]["enemy_spe_speed"][0]
                enemy_speed2 = refree.level[refree.status]["enemy_spe_speed"][1]
                count_time1 = refree.level[refree.status]["enemy_spe_interval"][0] * FPSLIMIT
                count_time2 = refree.level[refree.status]["enemy_spe_interval"][1] * FPSLIMIT
                enemy_type = refree.level[refree.status]["enemy_type"]
            else: #普通飞机
                enemy_speed1 = refree.level[refree.status]["enemy_default_speed"][0]
                enemy_speed2 = refree.level[refree.status]["enemy_default_speed"][1]
                count_time1 = refree.level[refree.status]["enemy_default_interval"][0] * FPSLIMIT
                count_time2 = refree.level[refree.status]["enemy_default_interval"][1] * FPSLIMIT
                enemy_type = STRAIGHT
            #创建                
            self.add_enemy(enemy(self.pic.get_width(), self.pic.get_height(), random.uniform(enemy_speed1, enemy_speed2), enemy_type))
            self.count_time = random.randint(count_time1, count_time2)
                        
class plane : #飞机类
    def __init__(self): 
        self.x = 0
        self.y = 0
        self.pic = pygame.image.load('plane.png').convert_alpha() 
        
    def update(self): 
        x_mouse, y_mouse = pygame.mouse.get_pos()
        self.x = x_mouse - self.pic.get_width() / 2
        self.y = y_mouse - self.pic.get_height() / 2
        
    def fire(self, bullet_box, refree) :
        if refree.level[refree.status]["bullet_numberlimit"] == True and len(bullet_box.list) > 0: #有子弹个数限制
            pass
        else:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            x = x_mouse - bullet_box.pic.get_width() / 2
            y = y_mouse - bullet_box.pic.get_height() / 2 - self.pic.get_height() / 2 
            bullet_box.add_bullet(bullet(x, y, refree.level[refree.status]["bullet_speed"]))
            
    def draw(self) :
        screen.blit(self.pic, (self.x, self.y))
        
class refree : #裁判类
    def __init__(self):
        self.goal = 0 #得分
        self.status = 0 #游戏状态 0初始画面 1-5关卡 6通关 7撞毁
        self.time_passed = 0 #记录每一帧实际的时间
        #关卡设置，速度单位：像素/秒，间隔单位：秒，元组表示范围内取随机
        self.level = [0]
        #1
        self.level.append({"bullet_speed": WINSIZE_Y, "bullet_numberlimit": False, "line_exit": False, "enemy_default_speed": (100, 140), \
                            "enemy_default_interval": (2, 3.5), "enemy_spe_divisor": (10), "enemy_spe_remainder":(8), "enemy_spe_speed": (600, 600), \
                            "enemy_spe_interval": (2, 3.5), "enemy_type": STRAIGHT, "enemy_size": LARGE, "get_goal": 8, "id": "Ⅰ 随便玩玩"})
        #2
        self.level.append({"bullet_speed": WINSIZE_Y, "bullet_numberlimit": False, "line_exit": False, "enemy_default_speed": (100, 260), \
                            "enemy_default_interval": (0.5, 2.5), "enemy_spe_divisor": 5, "enemy_spe_remainder": 3, \
                            "enemy_spe_speed": (105, 180), "enemy_spe_interval": (0.6, 3.7), "enemy_type": LEFTANDRIGHT, "enemy_size": LARGE, "get_goal": 5, \
                            "id": "Ⅱ 好戏开始了"})
        #3
        self.level.append({"bullet_speed": 135, "bullet_numberlimit": True, "line_exit": True, "line_init_y": 100, "line_speed": 7.9, \
                            "enemy_default_speed": (20, 42), "enemy_default_interval": (0.25, 0.5), \
                            "enemy_type": STRAIGHT, "enemy_size": LARGE, "get_goal": 1, "id": "Ⅲ 去撞白线"})
        #4
        self.level.append({"bullet_speed": WINSIZE_Y, "bullet_numberlimit": False, "line_exit": True, "line_init_y": 400, "line_speed": 0, \
                            "enemy_default_speed": (40, 72), "enemy_default_interval": (0.5, 0.75), \
                            "enemy_type": STRAIGHT, "enemy_size": SMALL, "get_goal": 5, "id": "Ⅳ 我变大了"})
        #5
        self.level.append({"bullet_speed": WINSIZE_Y, "bullet_numberlimit": False, "line_exit": True, "line_init_y": 400, "line_speed": 0, \
                            "enemy_default_speed": (40, 68), "enemy_default_interval": (0.25, 2.5), "enemy_spe_divisor": 10, \
                            "enemy_spe_remainder": 1, "enemy_spe_speed": (40, 40), "enemy_spe_interval": (1.25, 3.7), "enemy_type": LEFTANDRIGHT, \
                            "enemy_size": SMALL, "get_goal": 10, "id": "Ⅴ 放松一下"})
        self.mouse_pic = pygame.image.load('hand.png').convert_alpha()
        
    def add_goal(self):
        self.goal += self.level[self.status]["get_goal"]
            
    def next_level(self, bullet_box, enemy_box, background, line):
        self.status += 1
        self.level_init(bullet_box, enemy_box, background, line)
    
    def remove_goal(self):
        self.goal -= 50

    def cal_goal(self, bullet_box, enemy_box, background, line, plane):
        for bullet in bullet_box.list :
            if bullet.y < - bullet_box.pic.get_height(): #子弹没打中
                self.remove_goal()
                bullet_box.del_bullet(bullet)
                break
            for enemy in enemy_box.list:                
                if bullet.x > enemy.x and bullet.x < enemy.x + enemy_box.pic.get_width() \
                and bullet.y > enemy.y and bullet.y < enemy.y + enemy_box.pic.get_height() : #击中敌机  
                    bullet_box.del_bullet(bullet)
                    enemy_box.del_enemy(enemy)
                    self.add_goal()
                    if self.goal >= 100:
                        self.next_level(bullet_box, enemy_box, background, line)
                    break       
        for enemy in enemy_box.list: 
            if enemy.y > WINSIZE_Y: #敌机没打中
                    self.remove_goal()
                    enemy_box.del_enemy(enemy)
                    break
            if plane.x > enemy.x - plane.pic.get_width() + 12 and plane.x < enemy.x + enemy_box.pic.get_width() - 12 and \
            plane.y > enemy.y - plane.pic.get_height() + 12 and plane.y < enemy.y + enemy_box.pic.get_height() - 12:#相撞
                self.status = 7
                self.level_init(bullet_box, enemy_box, background, line)
                break                   
        if plane.y < line.y - 3: #碰白线
            self.status = 7
            self.level_init(bullet_box, enemy_box, background, line)   
            
    def level_init(self, bullet_box, enemy_box, background, line):
        self.goal = 0
        bullet_box.set_to_zero()
        enemy_box.set_to_zero()
        #背景图
        if self.status == 0:
            background.pic = pygame.image.load('back1.jpg').convert()
        elif self.status == 6:
            background.pic = pygame.image.load('back6.jpg').convert()
        elif self.status == 7:
            background.pic = pygame.image.load('back7.jpg').convert()
        else:
            background.pic = pygame.image.load('back.jpg').convert()
        #敌机图
        try:
            if self.level[self.status]["enemy_size"] == LARGE:
                enemy_box.pic = pygame.image.load('enemy.png').convert_alpha()
            else:
                enemy_box.pic = pygame.image.load('enemy2.png').convert_alpha()
        except: #考虑首尾页例外
            pass
        #白线
        try:
            if self.level[self.status]["line_exit"] == False:
                line.set(-100, 0)
            else:
                line.set(self.level[self.status]["line_init_y"], self.level[self.status]["line_speed"])
        except: 
            pass
        #鼠标
            if self.status > 0 and self.status < 6:
                pygame.mouse.set_visible(False)

class line: #白线类
    def __init__(self):
        self.y = 100
        self.pic = pygame.image.load('line.png').convert_alpha()
        self.speed = 0
    def set(self, y, speed):
        self.y = y
        self.speed = speed
    def move(self, refree):
        self.y += self.speed / 1000 * refree.time_passed
    def draw(self):
        screen.blit(self.pic, (0, self.y))
        
class background: #背景类
    def __init__(self):
        self.pic = pygame.image.load('back.jpg').convert()
        
    def draw(self, refree) :
        screen.blit(self.pic, (0,0)) #将背景图画上去
        if refree.status > 0 and refree.status < 6:
            show_text(screen, (230, WINSIZE_Y - 60), "{:s}".format(refree.level[refree.status]["id"]), (90, 110, 130))
            show_text(screen, (12, WINSIZE_Y - 60), " 得分：{0:d}".format(refree.goal), (90, 110, 130))  

class mouse: #鼠标类
    def __init__(self):
        self.pic = pygame.image.load('hand.png').convert_alpha()
        self.x = 0
        self.y = 0
        
    def get_position(self):
        self.x, self.y = pygame.mouse.get_pos()
    
    def update(self, refree):
        self.get_position()
        if refree.status == 0 or refree.status == 7:
            if self.x > 130 and self.y > 390 and self.x < 310 and self.y < 450:
                screen.blit(self.pic, (self.x - 4, self.y - 3))
                pygame.mouse.set_visible(False)
            else:
                pygame.mouse.set_visible(True) 
        elif refree.status == 6:
            pygame.mouse.set_visible(True) 
        else:
            pygame.mouse.set_visible(False)
        
#-----------------库初始化-------------------------------------------
pygame.init() #初始化pygame,为使用硬件做准备
screen = pygame.display.set_mode((WINSIZE_X, WINSIZE_Y), 0, 32) #创建了一个窗口,窗口大小和背景图片大小一样

#----------------变量初始化------------------------------------------                
background = background() #初始化背景图片       
plane = plane() #初始化飞机
bullet_box = bullet_set() #初始化子弹容器
enemy_box = enemy_set() #初始化敌机容器
refree = refree() #初始化裁判
clock = pygame.time.Clock()
line = line()
mouse = mouse()

#-----------------游戏运行模块-------------------------------------------
refree.level_init(bullet_box, enemy_box, background, line)
while True:
    refree.time_passed = clock.tick(FPSLIMIT)#帧数控制，获取两帧之间的实际时间，单位ms
    pygame.display.set_caption("[FPS: {:.1f}]".format(clock.get_fps())) #设置窗口标题
    for event in pygame.event.get():
        if event.type == pygame.QUIT:#接收到退出事件后退出程序
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.get_position()
            if (refree.status == 0 or refree.status == 7) and mouse.x > 130 and mouse.y > 390 and mouse.x < 310 and mouse.y < 450:
                refree.status = 1
                refree.level_init(bullet_box, enemy_box, background, line)
            elif refree.status > 0 and refree.status < 6:
                plane.fire(bullet_box, refree)
    
    background.draw(refree)
    if refree.status == 0 or refree.status == 6 or refree.status == 7:
        mouse.update(refree)
    else:
        line.move(refree)
        line.draw()
        plane.update()
        plane.draw()
        bullet_box.all_move(refree)
        bullet_box.draw()
        enemy_box.create_enemy(refree)
        enemy_box.all_move(refree)
        enemy_box.draw()
        refree.cal_goal(bullet_box, enemy_box, background, line, plane)

    pygame.display.update()#刷新一下画面
