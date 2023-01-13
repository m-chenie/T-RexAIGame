import random
import pygame
import os
import neat
import math

pygame.init()

HEIGHT = 600
WIDTH = 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Images", "DinoRun1.png")),
           pygame.image.load(os.path.join("Images", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Images", "DinoJump.png"))
DEAD = pygame.image.load(os.path.join("Images", "DinoDead.png"))
DEAD = pygame.transform.rotate(DEAD, 90)

CACTUS = [pygame.image.load(os.path.join("Images", "LargeCactus1.png")),
          pygame.image.load(os.path.join("Images", "SmallCactus1.png")),
          pygame.image.load(os.path.join("Images", "SmallCactus2.png"))]

BACKGROUND = pygame.image.load(os.path.join("Images", "Background.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (800, 20))

CLOUD = pygame.image.load(os.path.join("Images", "Cloud.png"))
cloud_group = pygame.sprite.Group()

global GAME_SPEED, POINTS, FONT, still_playing
GAME_SPEED = 8
POINTS = 0
FONT = pygame.font.Font('freesansbold.ttf', 20)
still_playing = True


class Button():
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw_button(self, outline):
        pygame.draw.rect(SCREEN, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height), 0)

        display_text = FONT.render(self.text, True, 'white')
        SCREEN.blit(display_text, (self.x + (self.width / 2 - display_text.get_width() / 2),
                                   self.y + (self.height / 2 - display_text.get_height() / 2)))

    # checks if button is pressed
    def pressed(self, mouse_pos):
        if self.x < mouse_pos[0] < self.x + self.width:
            if self.y < mouse_pos[1] < self.y + self.height:
                return True

        return False


class BG():

    def __init__(self):
        self.background_x = 0

    def draw(self):
        self.background_x -= GAME_SPEED
        SCREEN.blit(BACKGROUND, (self.background_x, 575))
        SCREEN.blit(BACKGROUND, (self.background_x + 800, 575))

        SCREEN.blit(BACKGROUND, (self.background_x, 275))
        SCREEN.blit(BACKGROUND, (self.background_x + 800, 275))

        if self.background_x <= -800:
            self.background_x = 0

    # displays and updates score
    def score(self):
        global POINTS, GAME_SPEED

        POINTS += 1
        if POINTS % 100 == 0:  # increase speed of game every 100 points
            GAME_SPEED += 0.25

        text = FONT.render("Your score: " + str(POINTS), True, 'grey')
        AItext = FONT.render("AI", True, 'grey')

        text_box_player = text.get_rect()
        text_box_player.topright = (575, 25)
        SCREEN.blit(text, text_box_player)

        text_box_AI = AItext.get_rect()
        text_box_AI.topright = (575, 320)
        SCREEN.blit(AItext, text_box_AI)


class Cloud():  # try to add more clouds, maybe find images of groups of clouds
    def __init__(self):
        self.x = WIDTH
        self.y = random.randint(300, 400)
        self.cloud_image = CLOUD
        self.cloud_width = self.cloud_image.get_width()

    def update(self):
        self.x -= GAME_SPEED
        if self.x < -self.cloud_width:
            self.x = WIDTH + random.randint(10, 30)
            self.y = random.randint(300, 400)

    def draw(self):
        SCREEN.blit(self.cloud_image, (self.x, self.y))
        SCREEN.blit(self.cloud_image, (self.x, self.y - 300))


class ObstaclesAI():

    def __init__(self):
        self.obstacle_image = CACTUS[random.randint(1, 2)]  # only small cacti will be the first obstacle
        self.rect_obstacle = self.obstacle_image.get_rect()

        self.rect_obstacle.y = HEIGHT - self.obstacle_image.get_height() - 10
        self.rect_obstacle.x = WIDTH

    def update(self):
        self.rect_obstacle.x -= GAME_SPEED

        if self.rect_obstacle.x < -self.obstacle_image.get_width():
            self.obstacle_image = CACTUS[random.randint(0, 2)]
            self.rect_obstacle.x = WIDTH
            self.rect_obstacle.y = HEIGHT - self.obstacle_image.get_height() - 5

    def get_mask(self):
        return pygame.mask.from_surface(self.obstacle_image)

    # checks if the obstacle and the dino collides using masks for pixel perfect collision
    def collide(self, dino):
        dino_mask = dino.get_mask()
        cactus_mask = self.get_mask()

        offset = (int(self.rect_obstacle.x - dino.rect_dino.x), int(self.rect_obstacle.y - dino.rect_dino.y))
        collision = cactus_mask.overlap(dino_mask, offset)

        return collision

    def draw(self):
        SCREEN.blit(self.obstacle_image, (self.rect_obstacle.x, self.rect_obstacle.y))

class ObstaclesPlayer():

    def __init__(self):
        self.obstacle_image = CACTUS[random.randint(1, 2)] # only small cacti will be the first obstacle
        self.rect_obstacle = self.obstacle_image.get_rect()

        self.rect_obstacle.y = HEIGHT - self.obstacle_image.get_height() - 310
        self.rect_obstacle.x = WIDTH

    def update(self):
        self.rect_obstacle.x -= GAME_SPEED

        if self.rect_obstacle.x < -self.obstacle_image.get_width():
            self.obstacle_image = CACTUS[random.randint(0, 2)]
            self.rect_obstacle.x = WIDTH
            self.rect_obstacle.y = HEIGHT - self.obstacle_image.get_height() - 310

    def get_mask(self):
         return pygame.mask.from_surface(self.obstacle_image)

    # checks if the obstacle and the dino collides using masks for pixel perfect collision
    def collide(self, dino):
        dino_mask = dino.get_mask()
        cactus_mask = self.get_mask()

        offset = (int(self.rect_obstacle.x - dino.rect_dino.x), int(self.rect_obstacle.y - dino.rect_dino.y))
        collision = cactus_mask.overlap(dino_mask, offset)

        return collision

    def draw(self):
        SCREEN.blit(self.obstacle_image, (self.rect_obstacle.x, self.rect_obstacle.y))


class Dino():
    x = 80
    y = 500
    jump_velocity = 6

    def __init__(self):
        self.player = False

        self.running_image = RUNNING
        self.jumping_image = JUMPING
        self.dead_image = DEAD

        self.index = 0
        self.dino_image = self.running_image[self.index]

        self.rect_dino = self.dino_image.get_rect()
        self.rect_dino.x = self.x
        self.rect_dino.y = self.y

        self.current_jump_vel = self.jump_velocity

        self.is_running = True
        self.is_jumping = False
        self.is_dead = False

    def animate(self):
        if self.player:
            self.y = 200

        if self.is_running and not self.is_dead:
            self.is_jumping = False
            self.run()

        if self.is_jumping and not self.is_dead:
            self.is_running = False
            self.jump()

        if self.is_dead:
            self.dead()

    def run(self):
        self.index += 0.25
        if self.index >= 2:
            self.index = 0

        self.dino_image = self.running_image[int(self.index)]
        self.rect_dino.x = self.x
        self.rect_dino.y = self.y

    def jump(self):
        self.dino_image = self.jumping_image

        self.rect_dino.y -= self.current_jump_vel * 4
        self.current_jump_vel -= 0.5

        if self.current_jump_vel < -self.jump_velocity:
            self.current_jump_vel = self.jump_velocity
            self.is_jumping = False
            self.is_running = True

    def get_mask(self):
        return pygame.mask.from_surface(self.dino_image)

    def dead(self):  # if the dino dies
        global still_playing
        self.dino_image = self.dead_image
        self.is_dead = True
        if self.player:
            self.rect_dino.y = 205
        else:
            self.rect_dino.y = 505

        self.rect_dino.x -= GAME_SPEED

        if self.rect_dino.x < -self.dino_image.get_width() and self.player:
            game_over('You lost :(')
            still_playing = False

    def draw(self):
        SCREEN.blit(self.dino_image, (self.rect_dino.x, self.rect_dino.y))


def draw_game(dinos, player, cactusAI, player_cactus, cloud, bg):
    bg.draw()
    bg.score()

    cloud.draw()
    cloud.update()

    cactusAI.update()
    cactusAI.draw()

    player_cactus.update()
    player_cactus.draw()

    for dino in dinos:
        dino.animate()
        dino.draw()

    player.animate()
    player.draw()


def euclidian_distance(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    return math.sqrt((dx ** 2) + (dy ** 2))


def game_over(messsage):
    SCREEN.fill('white')
    text = FONT.render(messsage + " Score: " + str(POINTS), True, 'red')

    text_box = text.get_rect()
    text_box.center = (WIDTH/2, HEIGHT/2)
    SCREEN.blit(text, text_box)


# fitness function for NEAT
def eval_genome(genomes, config):
    global GAME_SPEED, still_playing
    clock = pygame.time.Clock()
    cloud = Cloud()
    dinos = []
    player = Dino()
    player.player = True
    neural_nets = []
    ge = []
    background = BG()
    cactusAI = ObstaclesAI()
    player_cactus = ObstaclesPlayer()
    player_cactus.player = True

    for g_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        neural_nets.append(net)
        dinos.append(Dino())
        genome.fitness = 0
        ge.append(genome)

    still_playing = True
    while still_playing:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.is_jumping = True
                    player.is_running = False

        SCREEN.fill("white")

        draw_game(dinos, player, cactusAI, player_cactus, cloud, background)

        if len(dinos) == 0:
            game_over("You win!!!")
            still_playing = False

        for i, dino in enumerate(dinos):
            ge[i].fitness += 0.1
            output = neural_nets[i].activate((dino.rect_dino.y,
                                              euclidian_distance((dino.rect_dino.x, dino.rect_dino.y),
                                                                 cactusAI.rect_obstacle.midtop)))

            if output[0] > 0.5:
                dino.is_jumping = True
                dino.is_running = False

            if cactusAI.collide(dino):
                dino.is_dead = True
                dino.animate()
                dino.draw()
                ge[i].fitness -= 1
                dinos.pop(i)
                ge.pop(i)
                neural_nets.pop(i)

            else:
                ge[i].fitness += 5

        if player_cactus.collide(player):
            player.is_dead = True

        if POINTS > 10000:
            break

        clock.tick(30)
        pygame.display.update()

# changes the population in the NEAT config file to change the difficulty level of the AI
def change_file(pop):
    with open('neat_config.txt', 'r', encoding='utf-8') as file:
        file_data = file.readlines()

    file_data[3] = "pop_size              = " + pop + '\n'

    with open('neat_config.txt', 'w', encoding='utf-8') as file:
        file.writelines(file_data)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    best_dino = population.run(eval_genome, 1)


if __name__ == '__main__':

    local_directory = os.path.dirname(__file__)

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy.pressed(mouse_pos):
                    change_file('10')

                    config_path = os.path.join(local_directory, 'neat_config.txt')
                    run(config_path)
                    pygame.time.delay(2000)

                if normal.pressed(mouse_pos):
                    change_file('30')

                    config_path = os.path.join(local_directory, 'neat_config.txt')
                    run(config_path)
                    pygame.time.delay(2000)

                if hard.pressed(mouse_pos):
                    change_file('50')

                    config_path = os.path.join(local_directory, 'neat_config.txt')
                    run(config_path)
                    pygame.time.delay(2000)

        SCREEN.fill("white")

        text = FONT.render("Select difficulty of AI", True, 'black')

        text_box = text.get_rect()
        text_box.topleft = (200, 150)
        SCREEN.blit(text, text_box)

        easy = Button((227, 195, 154), 200, 200, 200, 50, "Easy")
        easy.draw_button((195, 217, 158))

        normal = Button((227, 195, 154), 200, 275, 200, 50, "Normal")
        normal.draw_button((195, 217, 158))

        hard = Button((227, 195, 154), 200, 350, 200, 50, "Hard")
        hard.draw_button((195, 217, 158))

        pygame.display.update()
