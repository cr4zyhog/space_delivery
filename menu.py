import sys

import pygame
import main
import csv

pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)


class Menu:
    def __init__(self):
        self.background = pygame.image.load('data/background.png')
        screen.blit(self.background, (0, 0))
        self.font = pygame.font.SysFont('MS Serif', 200, bold=True)
        self.font1 = pygame.font.SysFont('MS Serif', 100, bold=True)
        self.render = 0
        self.spis = []
        self.flag_stats = False
        self.level_count = 0
        self.levels = [['levels/level0.txt', 'levels/level0_space.txt'],
                       ['levels/level1.txt', 'levels/level1_space.txt'],
                       ['levels/level2.txt', 'levels/level2_space.txt'],
                       ['levels/level3.txt', 'levels/level3_space.txt'],
                       ['levels/level4.txt', 'levels/level4_space.txt'],
                       ['levels/level5.txt', 'levels/level5_space.txt']]
        self.clock = pygame.time.Clock()
        self.button_press = ''

    def update_main_menu(self):
        if self.flag_stats:
            screen.blit(self.background, (0, 0))
            self.render = self.font.render(f'Kills records:', 0, (100, 100, 255))
            screen.blit(self.render, (100, 200))
            c = 0
            for i in self.spis:
                self.render = self.font1.render(f'level{i[0]}:', 0, (255, 255, 255))
                screen.blit(self.render, (400, 400 + (100 * c)))
                self.render = self.font1.render(f'{i[1]}', 0, (255, 255, 255))
                screen.blit(self.render, (650, 400 + (100 * c)))
                c += 1
                if c == 6:
                    c = 0
            self.render = self.font1.render(f'Back', 0, (255, 255, 255))
            screen.blit(self.render, (100, 800))
            if self.button_press == 'Back':
                self.flag_stats = False
        else:
            screen.blit(self.background, (0, 0))
            if self.button_press == 'Exit':
                self.button_press = ''
                pygame.quit()
                sys.exit()
            elif self.button_press == 'Play':
                pygame.mixer.stop()
                main.main(self.levels[0], 'pistol', self.level_count)
            elif self.button_press == 'Stats':
                self.flag_stats = True
                with open('stats.csv', encoding="utf8") as csvfile:
                    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
                    rows = [(i[0], i[1]) for i in reader]
                    if rows:
                        self.spis = [i for i in rows]
            self.render = self.font.render('Space Delivery', 0, (100, 100, 255))
            screen.blit(self.render, (450, 200))
            self.render = self.font1.render('Play', 0, (255, 255, 255))
            screen.blit(self.render, (800, 400))
            self.render = self.font1.render('Stats', 0, (255, 255, 255))
            screen.blit(self.render, (800, 500))
            self.render = self.font1.render('Exit', 0, (255, 255, 255))
            screen.blit(self.render, (800, 600))

    def check_press(self, pos):
        if 800 < pos[0] < 950 and 400 < pos[1] < 475:
            self.button_press = 'Play'
        elif 800 < pos[0] < 980 and 500 < pos[1] < 575:
            self.button_press = 'Stats'
        elif 800 < pos[0] < 950 and 600 < pos[1] < 675:
            self.button_press = 'Exit'
        elif 100 < pos[0] < 300 and 800 < pos[1] < 875:
            self.button_press = 'Back'

    def check_press_sled(self, pos):
        if 100 < pos[0] < 450 and 800 < pos[1] < 875:
            self.button_press = 'Next level'
        elif 1600 < pos[0] < 1800 and 800 < pos[1] < 875:
            self.button_press = 'Menu'

    def sled_level(self, kills, weapon, level):
        if level != 5:
            self.level_count = level + 1
        else:
            self.level_count = level
        print(self.level_count)
        pygame.mixer.music.load('data/sounds/fon_menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.set_caption('Alien Crumbs')
        pygame.display.set_icon(pygame.image.load('data/aliens/alien1/alien_1.png'))
        with open('stats.csv', encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            rows = [[i[0], i[1]] for i in reader]
            self.spis = [i for i in rows]
            print(self.spis)
            if int(self.spis[level][1]) < kills:
                self.spis[level][1] = str(kills)
            with open('stats.csv', 'w', encoding='UTF-8', newline='') as fileik:
                writer = csv.writer(fileik, delimiter=';')
                writer.writerows(self.spis)
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen.blit(self.background, (0, 0))
                        self.run()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_press_sled(event.pos)
            self.render = self.font.render('Congratulations!', 0, (255, 255, 0))
            screen.blit(self.render, (100, 200))
            self.render = self.font1.render('Kills:', 0, (255, 255, 255))
            screen.blit(self.render, (100, 400))
            self.render = self.font1.render(f'{kills}', 0, (255, 255, 255))
            screen.blit(self.render, (350, 400))
            self.render = self.font1.render('Next level', 0, (255, 255, 255))
            screen.blit(self.render, (100, 800))
            self.render = self.font1.render('Menu', 0, (255, 255, 255))
            screen.blit(self.render, (1600, 800))
            if self.button_press == 'Menu':
                self.button_press = ''
                screen.blit(self.background, (0, 0))
                self.run()
            if self.button_press == 'Next level':
                if self.level_count < 6:
                    self.button_press = ''
                    main.main(self.levels[self.level_count], weapon, self.level_count)
                else:
                    self.button_press = ''
                    self.run()
            pygame.display.flip()
            self.clock.tick(60)

    def run(self):
        pygame.mixer.music.load('data/sounds/fon_menu.mp3')
        pygame.mixer.music.play(-1)
        pygame.display.set_caption('Space Delivery')
        pygame.display.set_icon(pygame.image.load('data/aliens/alien1/alien_1.png'))
        while True:
            for event in pygame.event.get():
                if event == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.check_press(event.pos)
            self.update_main_menu()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    menu = Menu()
    menu.run()
