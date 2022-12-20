import pygame
from pygame import *
import sys
import random
import time
import pygame_menu

pygame.init()
surface = pygame.display.set_mode((600, 400))


class Game():
    def __init__(self):
    # задаем размеры экрана
        self.screen_width = 720
        self.screen_height = 460
        pygame.mixer.init()
        self.play_background_music()

        # необходимые цвета
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.brown = pygame.Color(165, 42, 42)
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        # будет задавать количество кадров в секунду
        self.fps_controller = pygame.time.Clock()

        # переменная для оторбражения результата
        # (сколько еды съели)
        self.score = 0


    def init_and_check_for_errors(self):
   # """Начальная функция для инициализации и
   #    проверки как запустится pygame"""
        check_errors = pygame.init()
        if check_errors[1] > 0:
            sys.exit()
        else:
            print('Ok')

    def set_surface_and_title(self):
    #"""Задаем surface(поверхность поверх которой будет все рисоваться)
    #   и устанавливаем загаловок окна"""

        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = pygame.image.load('grass.png').convert()
        self.background = pygame.transform.smoothscale(self.background, self.play_surface.get_size())
        pygame.display.set_caption('Змейка')

    def event_loop(self, change_to):
    # """Функция для отслеживания нажатий клавиш игроком"""

        # запускаем цикл по ивентам
        for event in pygame.event.get():
        # если нажали клавишу
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = "DOWN"
                # нажали escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return change_to

    def refresh_screen(self):
     # """обновляем экран и задаем фпс"""
        pygame.display.flip()
        game.fps_controller.tick(23)

    def show_score(self, choice=1):
       #"""Отображение результата"""
        s_font = pygame.font.SysFont("verdana", 24)
        s_surf = s_font.render('Счёт: {0}'.format(self.score), True, self.black)
        s_rect = s_surf.get_rect()
        # дефолтный случай отображаем результат слева сверху
        if choice == 1:
            s_rect.midtop = (80, 10)
        # при game_overe отображаем результат по центру
        # под надписью game over
        else:
            s_rect.midtop = (360, 120)
        # рисуем прямоугольник поверх surface
        self.play_surface.blit(s_surf, s_rect)
    def play_background_music(self):
        pygame.mixer.music.load("81cebf7e45fdef7.mp3")
        pygame.mixer.music.play()
    def game_over(self):
      #"""Функция для вывода надписи Game Over и результатов
      #    в случае завершения игры и выход из игры"""
        go_font = pygame.font.SysFont('monaco', 72)
        go_surf = go_font.render('Game over...', True, self.red)
        go_rect = go_surf.get_rect()
        go_rect.midtop = (360, 15)
        self.play_surface.blit(go_surf, go_rect)
        self.show_score(0)
        pygame.display.flip()
        pygame.mixer.music.pause()
        time.sleep(2)


#
# class Menu():
#     def __init__(self):
#         self._option_surfaces = []
#         self._callbacks = []
#         self._current_option_index = 0
#     def append_option(self, option, callback):
#         self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))
#         self._callbacks.append(callback)
#
#     def swich(self, direction):
#         self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))
#
#     def select(self):
#         self._callbacks[self._current_option_index]()
#
#     def draw(self, surf, x, y, option_y_padding):
#         for i, option in enumerate(self._option_surfaces):
#             option_rect = option.get_rect()
#             option_rect.topleft = (x, y + i * option_y_padding)
#             if i == self._current_option_index:
#                 draw.rect(surf, (0, 100, 0), option_rect)
#             surf.blit(option, option_rect)


class Snake():
    def __init__(self):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [100, 50]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова змеи - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        # направление движение змеи, изначально
        # зададимся вправо
        self.direction = "RIGHT"
        # куда будет меняться напрвление движения змеи
        # при нажатии соответствующих клавиш
        self.change_to = self.direction
        self.head_right = pygame.image.load("vupsen.png")
        self.head_left = pygame.image.load("vupsen2.png")
        self.head_up = pygame.image.load("вуп.png")
        self.head_down = pygame.image.load("вуп.png")


    def validate_direction_and_change(self):
    #"""Изменияем направление движения змеи только в том случае,
    #   если оно не прямо противоположно текущему"""
        if any((self.change_to == "RIGHT" and not self.direction == "LEFT",
                self.change_to == "LEFT" and not self.direction == "RIGHT",
                self.change_to == "UP" and not self.direction == "DOWN",
                self.change_to == "DOWN" and not self.direction == "UP")):
            self.direction = self.change_to

    def change_head_position(self):
    #"""Изменияем положение головы змеи"""
        if self.direction == "RIGHT":
            self.snake_head_pos[0] += 5
        elif self.direction == "LEFT":
            self.snake_head_pos[0] -= 5
        elif self.direction == "UP":
            self.snake_head_pos[1] -= 5
        elif self.direction == "DOWN":
            self.snake_head_pos[1] += 5

    def snake_body_mechanism(self, score, food_pos, food_pos1, kaka_pos, kaka_pos1, screen_width, screen_height):
        # если вставлять просто snake_head_pos,
        # то на всех трех позициях в snake_body
        # окажется один и тот же список с одинаковыми координатами
        # и мы будем управлять змеей из одного квадрата
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if ((self.snake_head_pos[0] >= food_pos[0] - 10 and self.snake_head_pos[0] <= food_pos[0] + 10) and (self.snake_head_pos[1] >= food_pos[1] - 10 and self.snake_head_pos[1] <= food_pos[1] + 10)):
        # если съели еду то задаем новое положение еды случайным
        # образом и увеличивем score на один
            food_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]
            sound_f = pygame.mixer.Sound("igrovaya-sreda-audio-energoobespechenie-audio-material-39368.mp3")
            pygame.mixer.Sound.play(sound_f)
            score += 1

        elif((self.snake_head_pos[0] >= food_pos1[0] - 10 and self.snake_head_pos[0] <= food_pos1[0] + 10) and (self.snake_head_pos[1] >= food_pos1[1] - 10 and self.snake_head_pos[1] <= food_pos1[1] + 10)):
            food_pos1 = [random.randrange(1, screen_width/5)*5, random.randrange(1, screen_height/5)*5]
            sound_f2 = pygame.mixer.Sound("upali-dengi-na-igrovoy-schet.mp3")
            pygame.mixer.Sound.play(sound_f2)
            score += 2
        elif ((self.snake_head_pos[0] >= kaka_pos[0] - 10 and self.snake_head_pos[0] <= kaka_pos[0] + 10) and (self.snake_head_pos[1] >= kaka_pos[1] - 10 and self.snake_head_pos[1] <= kaka_pos[1] + 10)):
        # если съели еду то задаем новое положение еды случайным
        # образом и увеличивем score на один
            kaka_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]
            sound_ka = pygame.mixer.Sound("zvuk-oshibki-vyibora.mp3")
            pygame.mixer.Sound.play(sound_ka)
            score -= 1

        elif((self.snake_head_pos[0] >= kaka_pos1[0] - 10 and self.snake_head_pos[0] <= kaka_pos1[0] + 10) and (self.snake_head_pos[1] >= kaka_pos1[1] - 10 and self.snake_head_pos[1] <= kaka_pos1[1] + 10)):
            kaka_pos1 = [random.randrange(1, screen_width/5)*5, random.randrange(1, screen_height/5)*5]
            sound_ka2 = pygame.mixer.Sound("vyibor-nujnoy-igrovoy-kategorii.mp3")
            pygame.mixer.Sound.play(sound_ka2)
            score -= 2

        else:
        # если не нашли еду, то убираем последний сегмент,
        # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return score, food_pos, food_pos1, kaka_pos, kaka_pos1

    def draw_snake(self, play_surface, background):
       # """Отображаем все сегменты змеи"""
        play_surface.blit(game.background, (0, 0))
        for pos in self.snake_body:
            pygame.draw.rect(play_surface, (248,58,62), pygame.Rect(pos[0], pos[1], 10, 10))


        if self.direction == "RIGHT":
            play_surface.blit(self.head_right, (self.snake_head_pos[0], self.snake_head_pos[1] - 8))
        elif self.direction == "LEFT":
            play_surface.blit(self.head_left, (self.snake_head_pos[0] -5, self.snake_head_pos[1] - 8))
        elif self.direction == "UP":
            play_surface.blit(self.head_up, (self.snake_head_pos[0] - 5, self.snake_head_pos[1] - 8))
        elif self.direction == "DOWN":
            play_surface.blit(self.head_down, (self.snake_head_pos[0] - 5, self.snake_head_pos[1] - 8))

    def check_for_boundaries(self, score, game_over, screen_width, screen_height):
        # """Проверка, что столкунлись с концами экрана или сами с собой
        #    (змея закольцевалась)"""
        if any((
                self.snake_head_pos[0] > screen_width-10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height-10
                or self.snake_head_pos[1] < 0
                or score < -5)):
            game_over()
            return True
        for block in self.snake_body[1:]:
             # проверка на то, что первый элемент(голова) врезался в
             # любой другой элемент змеи (закольцевались)
            if (block[0] == self.snake_head_pos[0] and block[1] == self.snake_head_pos[1]):
                game_over()
                return True



class Food():
    def __init__(self, food, food1, screen_width, screen_height):
      #"""Инит еды"""
        self.food = pygame.image.load('apple.png')
        self.food1 = pygame.image.load('kl.png')
        self.food_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]
        self.food_pos1 = [random.randrange(1, screen_width/5)*5, random.randrange(1, screen_height/5)*5]
    def draw_food(self, play_surface):
    # """Отображение еды"""
        play_surface.blit(self.food, (self.food_pos[0] - 5 , self.food_pos[1] - 5))
        play_surface.blit(self.food1, (self.food_pos1[0] - 5 , self.food_pos1[1] - 5))
class Kaka():
    def __init__(self, kaka, kaka1, screen_width, screen_height):
      #"""Инит еды"""
        self.kaka = pygame.image.load('B.png')
        self.kaka1 = pygame.image.load('W.png')
        self.kaka_pos = [random.randrange(1, screen_width/10)*10, random.randrange(1, screen_height/10)*10]
        self.kaka_pos1 = [random.randrange(1, screen_width/5)*5, random.randrange(1, screen_height/5)*5]
    def draw_kaka(self, play_surface):
    # """Отображение еды"""
        play_surface.blit(self.kaka, (self.kaka_pos[0] - 5, self.kaka_pos[1] - 5))
        play_surface.blit(self.kaka1, (self.kaka_pos1[0] - 5, self.kaka_pos1[1] - 5))
game = Game()
snake = Snake()
food = Food(game.brown, game.brown, game.screen_width, game.screen_height)
kaka = Kaka(game.brown, game.brown, game.screen_width, game.screen_height)
def start_the_game():
    game.init_and_check_for_errors()
    game.set_surface_and_title()
    while True:
        snake.change_to = game.event_loop(snake.change_to)
        snake.validate_direction_and_change()
        snake.change_head_position()
        game.score, food.food_pos, food.food_pos1, kaka.kaka_pos, kaka.kaka_pos1 = snake.snake_body_mechanism(game.score, food.food_pos, food.food_pos1, kaka.kaka_pos, kaka.kaka_pos1, game.screen_width, game.screen_height)
        snake.draw_snake(game.play_surface, game.background)
        food.draw_food(game.play_surface)
        kaka.draw_kaka(game.play_surface)
        if snake.check_for_boundaries(game.score, game.game_over, game.screen_width, game.screen_height):
            break
        game.show_score()
        game.refresh_screen()


menu = pygame_menu.Menu('Welcome', 720, 460,  theme=pygame_menu.themes.THEME_BLUE)
menu.add.text_input('Name:', default='Player')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(surface)
