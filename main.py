import pygame
import pygame as pg
from math import *
import pygame_gui


WIDTH = 1500
HEIGHT = 750
FPS = 60


g = 10
h = 0
v = 50
a = 60

rad = 5
pc = 1.29
pt = 11300
sop = -1

games = 0
scale = 0

pg.init()
surface = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
pg.draw.rect(surface, (64, 86, 161), (20, 20, 100, 75))

start_img = pg.image.load('next.png')
back_img = pg.image.load('backg.png')

font = pg.font.SysFont(None, 48)
img = font.render('hello', True, 'BLUE')
info = font.render('hello', True, 'BLUE')
g_text = font.render('g =                               м/с^2', True, 'black')
h_text = font.render('h =                               м', True, 'black')
v_text = font.render('v =                               м/с', True, 'black')
a_text = font.render('a =', True, 'black')
cv_text = font.render('настройки сопротивления воздуха:', True, 'black')
ob_text = font.render('введите обязательные значения:', True, 'black')
r_text = font.render('радиус =                          см', True, 'black')
pc_text = font.render('плотность среды =                        кг/м^3', True, 'black')
pt_text = font.render('плотность тела =                         кг/м^3', True, 'black')
instruction = font.render('Эта программа построит траекторию полёта тела по заданным вами значениям.'
                          '\n 1. После перехода к меню настроек вам необходимо ввести обязательные значения.'
                          '\n    Где a - угол к горизонту, v - скорость тела, h - высота, с которой летит'
                          '\n    тело, а g - ускорение свободного падения.'
                          '\n 2. Для учёта сопротивления воздуха: введите 1 в поле'
                          '\n    "настройки сопротивления воздуха" и заполните необходимые значения.'
                          '\n 3. Если вы не хотите учитывать сопротивление, оставьте поля, '
                          '\n    относящиеся к нему, пустыми.'
                          '\n 4. Для перемещения между страницами используйте кнопки "вперёд" и "назад".'
                          '\n 5. Чтобы узнать координаты и скорость тела в определённой точке '
                          '\n    наведите на неё мышку.'
                          , True, 'black')

text_inp_s = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((750, 400), (200, 30)), manager=manager,
                                                 object_id='s_input')

text_inp_g = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 200), (200, 30)), manager=manager,
                                                 object_id='g_input')
text_inp_h = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((750, 200), (200, 30)), manager=manager,
                                                 object_id='h_input')
text_inp_v = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((200, 300), (200, 30)), manager=manager,
                                                 object_id='v_input')
text_inp_a = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((750, 300), (200, 30)), manager=manager,
                                                 object_id='a_input')

text_inp_r = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((270, 640), (200, 30)), manager=manager,
                                                 object_id='r_input')
text_inp_pc = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((420, 500), (200, 30)), manager=manager,
                                                 object_id='pc_input')
text_inp_pt = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((390, 570), (200, 30)), manager=manager,
                                                 object_id='pt_input')

class Body(pg.sprite.Sprite):
    def __init__(self, g, h, rad, col, speed, angle, sop, pt, pc, scale):
        super().__init__()
        self.pt = pt
        self.pc = pc
        self.sop = sop
        self.scale = scale
        self.h = h
        self.rad = rad
        self.speed = speed
        self.angle = angle
        self.g = g

        self.circle = pg.draw.circle(surface, col, (50, 700 - 5 - self.h), 5)
        self.circle.x = 50
        self.circle.y = 700 - 5 - self.h
        self.col = col

        self.x_speed = self.speed * cos(self.angle / 180 * pi)
        self.y_speed = self.speed * sin(self.angle / 180 * pi)
        if self.sop == 1:
            self.xa = (1.41 * self.pc * self.speed * self.x_speed) / (8 * self.pt * 5)
            self.ya = (1.41 * self.pc * self.speed * self.y_speed) / (8 * self.pt * 5) + self.g
        elif self.sop == -1:
            self.xa = 0
            self.ya = self.g

    def reset(self):
        if self.sop == 1:
            self.xa = (1.41 * self.pc * self.speed * self.x_speed) / (8 * self.pt * (self.rad/100))
            self.ya = (1.41 * self.pc * self.speed * self.y_speed) / (8 * self.pt * (self.rad/100)) + self.g
        elif self.sop == -1:
            self.xa = 0
            self.ya = self.g
        if self.h > 0:
            pg.draw.rect(surface, (64, 86, 161), (0, 700 - self.h, 55, self.h))
        pg.draw.circle(surface, self.col, (self.circle.x, self.circle.y), 5)

    # def finish_x(self):
    #     return ((2 * self.speed * sin(self.angle / 180 * pi)) / self.g) * self.x_speed


class Way(pg.sprite.Sprite):
    def __init__(self, x, y, rad, x_speed, y_speed, info, col, time, scale):
        super().__init__()
        self.x = x
        self.y = y
        self.scale = scale
        self.time = time
        self.col = col
        self.rad = rad
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.info = info # x, y
        self.info1 = info # x_speed
        self.info2 = info # y_speed
        self.info3 = info  # time

        self.circle = pg.draw.circle(surface, self.col, (self.x, self.y), self.rad)

    def reset(self):
        pg.draw.circle(surface, self.col, (self.circle.x + 5, self.circle.y + 5), self.rad)

    def show_info(self):
        pos = pg.mouse.get_pos()
        if self.circle.collidepoint(pos):
            pg.draw.rect(surface, (73, 189, 22), (1100, 50, 350, 200))
            self.info = font.render('x: ' + str(round((self.circle.x - 45)*self.scale, 2)) + ' y: ' + str(round((690 - self.circle.y)*self.scale, 2 )), True, 'black')
            self.info1 = font.render('x_speed: ' + str(round(self.x_speed, 2)), True, 'black')
            self.info2 = font.render('y_speed: ' + str(round(self.y_speed, 2)), True, 'black')
            self.info3 = font.render('time: ' + str(self.time), True, 'black')
            surface.blit(self.info, (1110, 60))
            surface.blit(self.info1, (1110, 110))
            surface.blit(self.info2, (1110, 160))
            surface.blit(self.info3, (1110, 210))

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def action(self):
        action = False
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pg.mouse.get_pressed()[0] == 0:
                self.clicked = False
        return action


dots = []

backg = Button(50, 50, back_img, 0.2)

def game():
    global scale
    time = 0
    surface.fill((197, 203, 227))
    th = (v * sin(a / 180 * pi)) / g
    max_x = v * cos(a / 180 * pi) * th * 2
    max_y = v * sin(a / 180 * pi) * th - ((g * (th**2)) / 2)
    # if scale <= 0.4:
    #     scale = scale
    if games == 1:
        scale = max(max_y / 600, max_x / 1300)
        if scale > 1 and sop == -1:
            scale = ceil(scale)
        elif scale > 1 and sop == 1:
            scale = ceil(scale/3)
        else:
            scale = 1


    print(scale)
    ball = Body(g, h, rad, (255, 0, 0), v, a, sop, pt, pc, scale)
    dot1 = Way(ball.circle.x, ball.circle.y, 5, ball.x_speed, ball.y_speed, info, ball.col, time, scale)
    dots.append(dot1)

    while True:

        if backg.action():
            menu()
        backg.draw()

        for i in pg.event.get():
            if i.type == pg.QUIT:
                exit()

        pg.draw.rect(surface, (64, 86, 161), (0, 700, 1500, 50))
        ball.y_speed -= ball.ya
        ball.x_speed -= ball.xa
        ball.circle.y -= ball.y_speed/scale
        ball.circle.x += ball.x_speed/scale

        if ball.circle.y < 700:
            time += 1
            dot = Way(ball.circle.x, ball.circle.y, 5, ball.x_speed, ball.y_speed, info, ball.col, time, scale)
            dots.append(dot)
            ball.reset()
        else:
            for dot in dots:
                dot.reset()
                dot.show_info()

        pg.display.update()
        clock.tick(FPS)

next = Button(1150, 250, start_img, 0.2)
back = Button(1150, 400, back_img, 0.2)


def menu():
    global g, h, v, a, rad, pc, pt, sop, games
    surface.fill((197, 203, 227))
    while True:

        surface.blit(ob_text, (100, 100))

        surface.blit(g_text, (100, 200))
        surface.blit(h_text, (650, 200))
        surface.blit(v_text, (100, 300))
        surface.blit(a_text, (650, 300))

        surface.blit(cv_text, (100, 400))

        surface.blit(r_text, (100, 640))
        surface.blit(pc_text, (100, 500))
        surface.blit(pt_text, (100, 570))
        if next.action():
            games += 1
            game()
        next.draw()
        if back.action():
            main()
        back.draw()

        UI_REFRESH_RATE = clock.tick(60)/1000
        for i in pg.event.get():
            if i.type == pg.QUIT:
                exit()
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'g_input':
                if i.text != '':
                    g = float(i.text)
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'h_input':
                if i.text != '':
                    h = float(i.text)
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'a_input':
                if i.text != '':
                    a = float(i.text)
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'v_input':
                if i.text != '':
                    v = float(i.text)

            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 's_input':
                if i.text != '':
                    sop = int(i.text)

            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'r_input':
                if i.text != '':
                    rad = float(i.text)
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'pc_input':
                if i.text != '':
                    pc = float(i.text)
            if i.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and i.ui_object_id == 'pt_input':
                if i.text != '':
                    pt = float(i.text)

            manager.process_events(i)
        manager.update(UI_REFRESH_RATE)
        manager.draw_ui(surface)
        pg.display.update()

next1 = Button(630, 550, start_img, 0.2)

def main():
    surface.fill((197, 203, 227))
    surface.blit(instruction, (40, 100))
    while True:
        if next1.action():
            menu()
        next1.draw()
        for i in pg.event.get():
            if i.type == pg.QUIT:
                exit()
        pg.display.update()
        clock.tick(FPS)
main()
pg.quit()
