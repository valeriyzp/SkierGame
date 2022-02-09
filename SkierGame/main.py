# Program for laboratory work 3, task a

import pygame
import random
from os import path
from datetime import datetime

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 720
HEIGHT = 480
FPS = 30
MAX_DISTANCE = 60000

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkierGame")
pygame.display.set_icon(pygame.image.load(path.join(img_dir, 'SkierGame.png')))
clock = pygame.time.Clock()

text_font = pygame.font.SysFont("Comic Sans MS", 30)
score_font = pygame.font.SysFont("Times New Roman", 15)

tree_img = [pygame.image.load(path.join(img_dir, "tree_01.png")), pygame.image.load(path.join(img_dir, "tree_02.png"))]
gate_img = pygame.image.load(path.join(img_dir, "gate.png"))


class Player():
    def __init__(self):
        skier_stay_img_name = ["skier_stay_01.png", "skier_stay_02.png", "skier_stay_03.png",
                               "skier_stay_04.png", "skier_stay_05.png", "skier_stay_06.png"]
        self.skier_stay_img = []
        for img in skier_stay_img_name:
            self.skier_stay_img.append(pygame.image.load(path.join(img_dir, img)))

        skier_down_img_name = ["skier_down_01.png", "skier_down_02.png", "skier_down_03.png",
                               "skier_down_04.png", "skier_down_05.png", "skier_down_06.png",
                               "skier_down_07.png", "skier_down_08.png", "skier_down_09.png",
                               "skier_down_10.png"]
        self.skier_down_img = []
        for img in skier_down_img_name:
            self.skier_down_img.append(pygame.image.load(path.join(img_dir, img)))

        skier_left_img_name = ["skier_left_01.png", "skier_left_02.png", "skier_left_03.png",
                               "skier_left_04.png", "skier_left_05.png", "skier_left_06.png"]
        self.skier_left_img = []
        for img in skier_left_img_name:
            self.skier_left_img.append(pygame.image.load(path.join(img_dir, img)))

        skier_right_img_name = ["skier_right_01.png", "skier_right_02.png", "skier_right_03.png",
                                "skier_right_04.png", "skier_right_05.png", "skier_right_06.png"]
        self.skier_right_img = []
        for img in skier_right_img_name:
            self.skier_right_img.append(pygame.image.load(path.join(img_dir, img)))

        self.skier_death_imgs = [pygame.image.load(path.join(img_dir, "skier_death_01.png")),
                                 pygame.image.load(path.join(img_dir, "skier_death_02.png"))]
        self.skier_death_img = self.skier_death_imgs[random.randint(0, 1)]

        self.skier_win_img = pygame.image.load(path.join(img_dir, "skier_win.png"))

        self.x = (WIDTH - 32) // 2
        self.y = HEIGHT // 4
        self.speed = 0
        self.speed_mul = 0
        self.corner_speed = 0
        self.corner_speed_mul = 0
        self.anim_count = 0
        self.left = False
        self.right = False
        self.hitbox = pygame.Rect(self.x + 8, self.y + 4, 15, 23)
        self.distance = 0
        self.score = 0
        self.stay = False
        self.win = False
        self.death = False
        self.ride_time = 0

    def get_score(self):
        return self.score

    def get_ride_time(self):
        return self.ride_time

    def play_intro(self):
        self.stay = True

    def play_death(self):
        self.death = True
        self.speed = 0
        self.ride_time = datetime.now() - self.ride_time

    def is_dead(self):
        return self.death

    def play_win(self):
        self.win = True
        self.speed = 0
        self.distance = MAX_DISTANCE
        self.ride_time = datetime.now() - self.ride_time

    def is_win(self):
        return self.win

    def start_ride(self):
        self.stay = False
        self.anim_count = 0
        self.speed = 5
        self.ride_time = datetime.now()

    def turn_left(self):
        if not self.left:
            self.left = True
            self.right = False
            self.anim_count = 0
            if self.corner_speed >= 0:
                self.corner_speed_mul = 0
            else:
                self.corner_speed_mul = (30 * -self.corner_speed - 3) // 19

        if self.corner_speed > 0:
            self.corner_speed -= 2
        else:
            self.corner_speed = -(3 + (self.corner_speed_mul//3) + (self.corner_speed_mul//5) + (self.corner_speed_mul//10))
            self.corner_speed_mul += 1
        self.speed_mul = max(0, self.speed_mul - (self.speed_mul // 30 + self.speed_mul // 75))

    def turn_right(self):
        if not self.right:
            self.right = True
            self.left = False
            self.anim_count = 0
            if self.corner_speed <= 0:
                self.corner_speed_mul = 0
            else:
                self.corner_speed_mul = (30 * self.corner_speed - 3) // 19

        if self.corner_speed < 0:
            self.corner_speed += 2
        else:
            self.corner_speed = (3 + (self.corner_speed_mul//3) + (self.corner_speed_mul//5) + (self.corner_speed_mul//10))
            self.corner_speed_mul += 1
        self.speed_mul = max(0, self.speed_mul - (1 + self.speed_mul // 30 + self.speed_mul // 75))

    def go_down(self):
        if self.right or self.left:
            self.right = False
            self.left = False
            self.anim_count = 0

        if self.corner_speed < 0:
            self.corner_speed += 1
        elif self.corner_speed > 0:
            self.corner_speed -= 1

        self.speed_mul = min(200, self.speed_mul + 1)

    def get_pos_x(self):
        return self.x

    def get_player_speed(self):
        return self.speed

    def get_player_distance(self):
        return self.distance

    def update(self):
        if self.x + self.corner_speed > WIDTH - 32:
            self.x = WIDTH - 32
            self.corner_speed = 0
        elif self.x + self.corner_speed < 0:
            self.x = 0
            self.corner_speed = 0
        else:
            self.x += self.corner_speed
        self.hitbox.x = self.x + 8
        self.speed = 5 + self.speed_mul // 20
        self.distance += self.speed

    def update_score(self, points):
        self.score += points

    def draw(self):
        if self.stay:
            win.blit(self.skier_stay_img[self.anim_count // 5], (self.x, self.y))
        elif self.death:
            win.blit(self.skier_death_img, (self.x, self.y))
        elif self.win:
            win.blit(self.skier_win_img, (self.x, self.y))
        elif self.left:
            win.blit(self.skier_left_img[self.anim_count // 5], (self.x, self.y))
        elif self.right:
            win.blit(self.skier_right_img[self.anim_count // 5], (self.x, self.y))
        else:
            win.blit(self.skier_down_img[self.anim_count // 3], (self.x, self.y))

        self.anim_count += 1
        if self.anim_count >= FPS:
            self.anim_count = 0
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)


class Tree():
    def __init__(self):
        self.x = random.randint(32, WIDTH - 64)
        self.y = HEIGHT + 32
        self.image = tree_img[random.randint(0, 1)]
        self.hitbox = pygame.Rect(self.x + 10, self.y + 17, 13, 15)
        self.hit = False

    def update(self, player_speed):
        self.y -= player_speed
        self.hitbox.y = self.y + 17

    def draw(self):
        win.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)


class Gate():
    def __init__(self, player_distance):
        self.width = max(300 - player_distance // 250, 100)
        self.x = random.randint(32, WIDTH - 32 - 2 * 22 - self.width)
        self.y = HEIGHT + 32
        self.hitbox = pygame.Rect(self.x + 10, self.y + 16, 12 + self.width + 12, 16)
        self.hitbox_left_gate = pygame.Rect(self.x + 10, self.y + 16, 12, 16)
        self.hitbox_right_gate = pygame.Rect(self.x + 22 + self.width, self.y + 16, 12, 16)
        self.check = False

    def is_check(self):
        return self.check

    def check_gate(self):
        self.check = True

    def draw(self):
        win.blit(gate_img, (self.x, self.y))
        pygame.draw.line(win, (0, 0, 255), (self.x + 22, self.y + 31), (self.x + 22 + self.width - 1, self.y + 31), 1)
        win.blit(gate_img, (self.x + 12 + self.width, self.y))
        # pygame.draw.rect(win, (255, 0, 0), self.hitbox, 1)

    def update(self, player_speed):
        self.y -= player_speed
        self.hitbox.y = self.y + 16
        self.hitbox_left_gate.y = self.y + 16
        self.hitbox_right_gate.y = self.y + 16


class Lift(pygame.sprite.Sprite):
    def __init__(self, picture):
        self.lift_images = [pygame.image.load(path.join(path.join(img_dir, "lift_02.png"))),
                            pygame.image.load(path.join(path.join(img_dir, "lift_01.png")))]
        self.image = self.lift_images[picture]
        self.rect = self.image.get_rect()
        if picture == 0:
            self.speed = -3
            self.rect.x = 200 + 32
            self.rect.y = HEIGHT + 1500
        else:
            self.speed = 3
            self.rect.x = 200
            self.rect.y = -500
        super().__init__()

    def update(self, *args):
        if self.speed < 0:
            self.rect.y += (-args[0] + self.speed)
            if self.rect.y <= -500:
                self.rect.y = HEIGHT + 1500
        else:
            if args[0] == 0:
                self.rect.y += self.speed
                if self.rect.y >= HEIGHT + 1500:
                    self.rect.y = -500
            else:
                self.rect.y += (-args[0] + self.speed)
                if self.rect.y <= -500:
                    self.rect.y = HEIGHT + 1500


def play_intro():
    intro = True
    player.play_intro()
    while intro:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.start_ride()
            break

        win.fill((255, 255, 255))
        pygame.draw.line(win, (0, 0, 255), (32, 0), (32, HEIGHT), 2)
        pygame.draw.line(win, (0, 0, 255), (WIDTH - 32, 0), (WIDTH - 32, HEIGHT), 2)
        all_sprites.update(player.get_player_speed())
        all_sprites.draw(win)
        text = text_font.render("Press space to start!", True, (0, 0, 255))
        win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2 - 15))
        player.draw()
        pygame.display.update()


def draw_score():
    pygame.draw.rect(win, (255, 255, 255), (WIDTH - 100, 0, 100, 90))
    pygame.draw.rect(win, (0, 0, 0), (WIDTH - 100, 0, 100, 90), 1)
    text = score_font.render("Score: {}".format(player.get_score()), True, (0, 0, 0))
    win.blit(text, (WIDTH - 100 + 5, 5))
    if player.is_dead() or player.is_win():
        time = datetime(2019, 5, 25, 00, 00, 00) + player.get_ride_time()
        text = score_font.render("Time: {}".format((time.strftime("%M:%S.%f"))[0:9]), True, (0, 0, 0))
    else:
        time = datetime(2019, 5, 25, 00, 00, 00) + (datetime.now() - player.get_ride_time())
        text = score_font.render("Time: {}".format((time.strftime("%M:%S.%f"))[0:9]), True, (0, 0, 0))
    win.blit(text, (WIDTH - 100 + 5, 25))
    text = score_font.render("Finish: {}m".format((MAX_DISTANCE - player.get_player_distance())//30), True, (00, 0, 0))
    win.blit(text, (WIDTH - 100 + 5, 45))
    text = score_font.render("Speed: {}m/s".format(player.get_player_speed()), True, (0, 0, 0))
    win.blit(text, (WIDTH - 100 + 5, 65))


def play_game_over():
    game_over = True
    while game_over:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
            break

        win.fill((255, 255, 255))
        pygame.draw.line(win, (0, 0, 255), (32, 0), (32, HEIGHT), 2)
        pygame.draw.line(win, (0, 0, 255), (WIDTH - 32, 0), (WIDTH - 32, HEIGHT), 2)
        for gate in gates_list:
            gate.draw()
        for tree in tree_list:
            tree.draw()
        all_sprites.draw(win)

        pygame.draw.rect(win, (255, 255, 255), (160, 170, 400, 140))
        pygame.draw.rect(win, (0, 0, 255), (160, 170, 400, 140), 2)
        if player.is_win():
            text = text_font.render("Your score: {}".format(player.get_score()), True, (0, 0, 255))
            win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2 - 3 * text.get_rect().height // 2))
            time = datetime(2019, 5, 25, 00, 00, 00) + player.get_ride_time()
            text = text_font.render("Your time: {}".format((time.strftime("%M:%S.%f"))[0:9]), True, (0, 0, 255))
            win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2 - text.get_rect().height // 2))
            text = text_font.render("Press enter to continue!", True, (0, 0, 255))
            win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2 + text.get_rect().height // 2))
        elif player.is_dead():
            text = text_font.render("Oops...", True, (0, 0, 255))
            win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2 - text.get_rect().height))
            text = text_font.render("Press enter to continue!", True, (0, 0, 255))
            win.blit(text, (WIDTH // 2 - text.get_rect().width // 2, HEIGHT // 2))
        player.draw()
        draw_score()
        pygame.display.update()


play = True
while play:
    player = Player()
    tree_list = list()
    distance_to_generate_tree = random.randint(5, 30)
    gates_list = list()
    distance_to_generate_gate = 500
    all_sprites = pygame.sprite.Group()
    all_sprites.add(Lift(0))
    all_sprites.add(Lift(1))

    play_intro()
    run = True
    while run:
        clock.tick(FPS)

        if distance_to_generate_tree <= 0:
            tree_list.append(Tree())
            distance_to_generate_tree = random.randint(25, 125)
        else:
            distance_to_generate_tree -= player.get_player_speed()

        if distance_to_generate_gate <= 0:
            gates_list.append(Gate(player.get_player_distance()))
            distance_to_generate_gate = 500
        else:
            distance_to_generate_gate -= player.get_player_speed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turn_left()
        elif keys[pygame.K_RIGHT]:
            player.turn_right()
        else:
            player.go_down()

        win.fill((255, 255, 255))
        pygame.draw.line(win, (0, 0, 255), (32, 0), (32, HEIGHT), 2)
        pygame.draw.line(win, (0, 0, 255), (WIDTH - 32, 0), (WIDTH - 32, HEIGHT), 2)

        for gate in gates_list:
            gate.update(player.get_player_speed())
            if gate.y <= -64:
                gates_list.pop(gates_list.index(gate))
            else:
                if gate.y + 32 < (HEIGHT // 4) and not gate.is_check():
                    gate.check_gate()
                    player.update_score(-15)
                else:
                    if not gate.is_check() and gate.hitbox.colliderect(player.hitbox):
                        gate.check_gate()
                        if gate.hitbox_left_gate.colliderect(player.hitbox) or gate.hitbox_right_gate.colliderect(player.hitbox):
                            player.update_score(5)
                        else:
                            player.update_score(15)
            gate.draw()

        player.update()
        if player.get_player_distance() >= MAX_DISTANCE:
            player.play_win()
            run = False
        player.draw()

        for tree in tree_list:
            tree.update(player.get_player_speed())
            if tree.y <= -64:
                tree_list.pop(tree_list.index(tree))
            else:
                if tree.hitbox.colliderect(player.hitbox):
                    player.play_death()
                    run = False
                tree.draw()

        if player.get_pos_x() <= 10 or player.get_pos_x() >= WIDTH - 32 - 10:
            player.play_death()
            run = False

        all_sprites.update(player.get_player_speed())
        all_sprites.draw(win)
        draw_score()
        pygame.display.update()

    play_game_over()

pygame.quit()
