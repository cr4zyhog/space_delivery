import pygame
import sys

import map
import menu

pygame.init()
tile_width = tile_height = 175
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)

MYEVENTTYPE = pygame.USEREVENT + 1
pygame.time.set_timer(MYEVENTTYPE, 250)

tile_images = {
    'stone': pygame.transform.scale(pygame.image.load('data/Space/Stone/stone.png'),
                                    (tile_width - 30, tile_height - 30)).convert_alpha(),
    'alien': pygame.image.load('data/Space/alien/alien_ship.png').convert_alpha(),
    'space': pygame.image.load('data/Space/space.png').convert_alpha()
}

ship = pygame.transform.scale(pygame.image.load('data/Space/ship/ship.png'),
                              (tile_width - 15, tile_height - 15)).convert_alpha()

ship_die = [pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy0.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy1.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy2.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy3.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy4.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy5.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy6.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha(),
            pygame.transform.scale(pygame.image.load('data/Space/ship/destroy/destroy7.png'),
                                   (tile_width - 10, tile_height - 10)).convert_alpha()]

alien_group = pygame.sprite.Group()
stone_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
engine_group = pygame.sprite.Group()


class End(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(end_group)
        self.image = tile_images[tile_type]
        self.orig = self.image
        self.angle = 0
        self.rect = self.image.get_rect(center=(pos_x * tile_width, pos_y * tile_height))

    def update(self, dvizh):
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + dvizh))


class Stone(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(stone_group)
        self.image = tile_images[tile_type]
        self.orig = self.image
        self.angle = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        fps = int(clock.get_fps())
        if fps == 0:
            fps = 1000
        self.angle += 300 / fps
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + dvizh))


class Alien(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(alien_group)
        self.image = tile_images[tile_type]
        self.angle = 0
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, dvizh):
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + dvizh))


class Player(pygame.sprite.Sprite):
    def __init__(self, clock, pos):
        super().__init__(player_group)
        self.clock = clock
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.image = ship
        self.kills = 0
        self.end = False
        self.boom = pygame.mixer.Sound('data/sounds/boom.mp3')
        self.perem = pygame.mixer.Sound('data/sounds/permesh.mp3')
        self.vistrel = pygame.mixer.Sound('data/sounds/vistrel.mp3')
        self.dvizh = 10
        self.count_move = 0
        self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
        self.count_time = 1
        self.count = 0
        self.is_die = False
        self.right = True
        self.count_image_die = 0
        self.count_engine = 0

    def update(self):
        fps = int(clock.get_fps())
        if fps == 0:
            fps = 1000
        if self.is_die:
            try:
                self.image = ship_die[self.count_image_die // 5]
                self.count_image_die += 1
                self.dvizh = 0
            except IndexError:
                self.count_image_die = 1000
        else:
            mouse_keys = pygame.mouse.get_pressed()
            if mouse_keys[0]:
                if pygame.time.get_ticks() - self.count >= 650:
                    self.count = pygame.time.get_ticks()
                    self.attack()
            keys = pygame.key.get_pressed()
            if pygame.time.get_ticks() - self.count_time > 150:
                if self.pos_x > 525:
                    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                        self.perem.play()
                        self.count_time = pygame.time.get_ticks()
                        self.pos_x -= tile_width
                if self.pos_x < 1225:
                    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                        self.perem.play()
                        self.count_time = pygame.time.get_ticks()
                        self.pos_x += tile_width
            for i in alien_group.sprites():
                if i.rect.centery >= 2300 or i.rect.centery <= -380:
                    continue
                if pygame.sprite.collide_mask(self, i):
                    # self.is_die = True
                    self.boom.play()
            for i in stone_group.sprites():
                if i.rect.centery >= 2300 or i.rect.centery <= -380:
                    continue
                if pygame.sprite.collide_mask(self, i):
                    self.is_die = True
                    self.boom.play()
            if pygame.sprite.spritecollideany(self, end_group):
                self.end = True

            self.rect = self.image.get_rect().move(self.pos_x, self.pos_y)
            self.dvizh += (0.007 * 60) / fps

    def attack(self):
        self.vistrel.play()
        if self.right:
            Bullets((self.rect.centerx + 40, self.rect.centery + 40))
        else:
            Bullets((self.rect.centerx - 40, self.rect.centery + 40))
        self.right = not self.right


class Bullets(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(bullets_group)
        self.collide_sound = pygame.mixer.Sound('data/sounds/boom.mp3')
        self.count = 0
        self.count_image = 0
        self.tick_from_death = 0
        self.death_count = 0
        self.image_list = [pygame.transform.scale(pygame.image.load('data/Space/ship/bullet/bl1.png'), (20 ,20)).convert_alpha(),
                           pygame.transform.scale(pygame.image.load('data/Space/ship/bullet/bl2.png'), (20 ,20)).convert_alpha()]
        self.image = self.image_list[0]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        fps = int(clock.get_fps())
        if fps == 0:
            fps = 1000
        if self.count_image % 5 == 0:
            if self.image == self.image_list[0]:
                self.image = self.image_list[1]
            else:
                self.image = self.image_list[0]
            self.count_image += 1
        x = self.rect.centerx
        y = self.rect.centery
        y -= 3000 / fps
        self.rect = self.image.get_rect(center=(x, y))
        self.count += 1
        for i in alien_group.sprites():
            if i.rect.centery >= 2300 or i.rect.centery <= -380:
                continue
            if self.rect.colliderect(i.rect):
                self.collide_sound.play()
                i.kill()
                player_group.sprites()[0].kills += 1
                self.kill()
                break
        for i in stone_group.sprites():
            if i.rect.centery >= 2300 or i.rect.centery <= -380:
                continue
            if pygame.sprite.collide_mask(self, i):
                self.collide_sound.play()
                self.kill()
                break


def generate_level(level):
    pos = 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 's':
                Stone('stone', x + 3, y - 96)
            if level[y][x] == 'a':
                Alien('alien', x + 3, y - 96)
            if level[y][x] == '@':
                pos = ((x + 3) * tile_width, (y - 93) * tile_height)
            if level[y][x] == '#':
                End('space', x + 3, y - 96)
    return pos


def check_press(pos):
    if 200 < pos[0] < 550 and 800 < pos[1] < 900:
        return 'restart'
    elif 1600 < pos[0] < 1800 and 800 < pos[1] < 875:
        return 'Menu'


clock = pygame.time.Clock()


def main(level):
    global screen, alien_group, player_group, stone_group, end_group, bullets_group, engine_group, clock
    screen = pygame.display.set_mode(size)
    end_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()
    stone_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    engine_group = pygame.sprite.Group()
    menu_ = menu.Menu()
    level_map = map.Map()
    pos = generate_level(level_map.load_level(level))
    clock = pygame.time.Clock()
    ship_player = Player(clock, pos)
    pygame.mixer.music.load('data/sounds/fon_space.mp3')
    pygame.mixer.music.play(-1)
    background = pygame.image.load('data/background.png')
    game_over = pygame.image.load('data/game_over.png').convert_alpha()
    font_game_over = pygame.font.SysFont('Arial', 100, bold=True)
    screen.blit(background, (0, 0))
    button_press = ''
    pygame.display.set_caption('Alien Crumbs')
    pygame.display.set_icon(pygame.image.load('data/aliens/alien1/alien_1.png'))
    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ship_player.is_die:
                    button_press = check_press(event.pos)
            if event.type == MYEVENTTYPE:
                engine_group.update((0, 0))
        ship_player.update()
        if ship_player.end:
            screen.blit(background, (0, 0))
            pygame.mixer.music.stop()
            return (True, ship_player.kills)
        if ship_player.count_image_die == 1000:
            pygame.draw.line(screen, (77, 77, 77), (520, 0), (520, 1080))
            pygame.draw.line(screen, (77, 77, 77), (695, 0), (695, 1080))
            pygame.draw.line(screen, (77, 77, 77), (870, 0), (870, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1045, 0), (1045, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1220, 0), (1220, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1395, 0), (1395, 1080))
            alien_group.draw(screen)
            stone_group.draw(screen)
            player_group.draw(screen)
            bullets_group.draw(screen)
            screen.blit(game_over, (0, 442))
            render = font_game_over.render('Restart', 0, (255, 255, 255))
            screen.blit(render, (200, 800))
            render = font_game_over.render('Menu', 0, (255, 255, 255))
            screen.blit(render, (1600, 800))
            pygame.display.flip()
            clock.tick(165)
            if button_press == 'restart':
                ship_player.kills = 0
                return (False, ship_player.kills)
            elif button_press == 'Menu':
                pygame.mixer.stop()
                screen.blit(background, (0, 0))
                menu_.run()
        else:
            fps = int(clock.get_fps())
            if fps == 0:
                fps = 1000
            end_group.update((ship_player.dvizh * 60) / fps)
            alien_group.update((ship_player.dvizh * 60) / fps)
            stone_group.update((ship_player.dvizh * 60) / fps)
            bullets_group.update()
            screen.blit(background, (0, 0))
            pygame.draw.line(screen, (77, 77, 77), (520, 0), (520, 1080))
            pygame.draw.line(screen, (77, 77, 77), (695, 0), (695, 1080))
            pygame.draw.line(screen, (77, 77, 77), (870, 0), (870, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1045, 0), (1045, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1220, 0), (1220, 1080))
            pygame.draw.line(screen, (77, 77, 77), (1395, 0), (1395, 1080))
            alien_group.draw(screen)
            stone_group.draw(screen)
            player_group.draw(screen)
            bullets_group.draw(screen)
            pygame.display.flip()
            clock.tick(165)
