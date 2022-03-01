# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
pygame.init()

SURFACE_WIDTH = 500
SURFACE_HEIGHT = 500
# Set up the drawing window
screen = pygame.display.set_mode([SURFACE_WIDTH, SURFACE_HEIGHT])

pygame.display.set_caption("игра")

"""
"""
# surface = pygame.display.get_surface() # Получаем информацию об окне (игровой поверхности)
# SURFACE_WIDTH, SURFACE_HEIGHT = size = surface.get_width(), surface.get_height() # получаем ширину и высоту окна

pygame.font.init()
comic_font = pygame.font.SysFont('Comic Sans MS', 30)

player_width = 86  # Ширина овечки
player_height = 68  # Высота овечки

speed = 5  # Скорость передвижения овечки

border = 5  # Границы по краям за которые нельзя выходить


direction_left = False
direction_right = False
animCount = 0

clock = pygame.time.Clock()

walkRight = [pygame.image.load('assets/right_2.png'), pygame.image.load('assets/right_3.png'), pygame.image.load('assets/right_4.png'),
             pygame.image.load('assets/right_2.png'), pygame.image.load('assets/right_3.png'), pygame.image.load('assets/right_4.png')]

sheepStand = pygame.image.load('assets/right_1.png')

background = pygame.image.load('assets/bg.jpg')

strawberry = pygame.image.load('assets/strawberry.png')
blukberry = pygame.image.load('assets/blukberry.png')

score = 0
berry_speed = 10

basket = []


class Berry():
    def __init__(self, image):
        self.image = image  # Изображение ягоды
        self.rect = self.image.get_rect()
        self.rect.y = 10  # Начальное положение ягоды по Y
        self.rect.x = random.randint(20, 420)  # Начальное положение ягоды по X

    def update(self):
        self.rect.y = self.rect.y + berry_speed
        if self.rect.y > 500:
            basket.pop()

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Sheep():
    def __init__(self):
        self.speed = 5  # Скорость передвижения овечки
        self.image = sheepStand
        self.rect = self.image.get_rect()
        self.rect.y = 430  # Начальное положение овечки по Y
        self.rect.x = 50  # Начальное положение овечки по X

        self.animCount = 0
        self.isJump = False
        self.jumpCount = 10

    def update(self, keys):
        self.animCount += 1

        if self.animCount >= 10:
            self.animCount = 0

        if keys[pygame.K_LEFT] and self.rect.x > border:
            self.rect.x -= speed
            self.image = walkRight[self.animCount // 5]
        elif keys[pygame.K_RIGHT] and self.rect.x < SURFACE_WIDTH - player_width - border:
            self.rect.x += speed
            self.image = walkRight[self.animCount // 5]
        else:
            self.animCount = 0

        if not(self.isJump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                self.isJump = True
        else:
            if self.jumpCount >= -10:
                if self.jumpCount < 0:
                    self.rect.y += (self.jumpCount ** 2) / 2
                else:
                    self.rect.y -= (self.jumpCount ** 2) / 2
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10

    def draw(self, screen):
        screen.blit(self.image, self.rect)


our_sheep = Sheep()
"""
"""


def drawWindow():
    global animCount
    global score
    global basket

    if score >= 100:
        screen.fill((250, 250, 250))
        textsurface = comic_font.render(
            "Вы выграли. "+"Очки: "+str(int(score)), False, (0, 0, 0))
        screen.blit(textsurface, (100, 250))

    else:
        # score += 10.0

        if animCount + 1 >= 30:
            animCount = 0

        screen.blit(background, (0, 0))
        # if(score>20):

        keys = pygame.key.get_pressed()
        our_sheep.draw(screen)
        our_sheep.update(keys)

        if len(basket) == 0:
            if random.randint(0, 1) == 0:
                basket.append(Berry(strawberry))
            elif random.randint(0, 1) == 1:
                basket.append(Berry(blukberry))

        for idx, berry in enumerate(basket):

            berry.draw(screen)
            berry.update()

            if our_sheep.rect.colliderect(berry.rect):
                basket.pop(idx)
                score += 5

        # screen.blit(walkRight[animCount // 5], (player_x, player_y))
        # animCount += 1

        textsurface = comic_font.render(
            "Накорми овечку! Сытость: "+str(int(score))+"%", False, (0, 0, 0))
        screen.blit(textsurface, (10, 0))

    pygame.display.update()


# Run until the user asks to quit
run = True
while run:
    clock.tick(30)
    # pygame.time.delay(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    drawWindow()

# Done! Time to quit.
pygame.quit()
