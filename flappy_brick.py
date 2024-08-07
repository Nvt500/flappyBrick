import pygame, sys
import random, time

pygame.init()

screen = pygame.display.set_mode((1280, 720))
screen.fill("sky blue")
pygame.display.set_caption("Flappy Brick")

font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game Over!", True, "Black")
start1 = font.render("To start", True, "Black")
start2 = font.render("Press Space", True, "Black")

clock = pygame.time.Clock()

class Brick(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.rect = pygame.Rect(0, 0, 50, 40)
    self.rect.center = (100, screen.get_height()/2)
  
  def jump(self):
    keys = pygame.key.get_pressed()
    global accel
    if keys[pygame.K_SPACE] and accel > 0 and self.rect.centery > 0:
      accel = -15
  
  def move(self):
    self.rect.move_ip(0, accel)

  def draw(self):
    pygame.draw.rect(screen, (115, 78, 44), self.rect)

class Pipe(pygame.sprite.Sprite):
  
  def __init__(self):
    super().__init__()
    self.stop = False
    gap = random.randint(200, gap_change)
    offset = random.randint(offset_change, screen.get_height()-gap-(offset_change/5))
    self.top = pygame.Rect(0, 0, 100, offset)
    self.top.topleft = (screen.get_width(), 0)
    self.bottom = pygame.Rect(0, 0, 100, 720-offset-gap)
    self.bottom.bottomleft = (screen.get_width(), screen.get_height())
  
  def move(self):
    global score
    global speed
    global gap_change
    global offset_change
    self.top.move_ip(speed, 0)
    self.bottom.move_ip(speed, 0)
    if self.top.right < 0:
      self.__init__()
    if self.top.centerx <= 100 and not self.stop:
      score += 1
      if speed >= -19.5:
        speed -= 0.5
      if gap_change > 350:
        gap_change -= 12
      if offset_change < 200:
        offset_change += 5
      self.stop = True
  
  def draw(self):
    pygame.draw.rect(screen, (31, 156, 26), self.top)
    pygame.draw.rect(screen, (31, 156, 26), self.bottom)

  def check(self):
    return self.top.centerx
#FUCKIN HELL MATE
gap_change = 600
offset_change = 100
score = 0
speed = -5
accel = 0
game = True

Player = Brick()
P1 = Pipe()
P2 = Pipe()
P3 = Pipe()

Pipes = pygame.sprite.Group()
Pipes.add(P1, P2, P3)

while True:
  gap_change = 600
  offset_change = 100
  speed = -5
  accel = 0

  go = [True, False, False]

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
      if event.type == pygame.KEYUP:
        accel = -15
        running = False

    screen.fill("sky blue")

    scores = font.render(str(score), True, "Black")
    screen.blit(scores, (screen.get_width()/2-40, 40))


    Player.draw()
    P1.draw()

    if game:
      screen.blit(start1, (screen.get_width()/2-140, screen.get_height()/2-80))
      screen.blit(start2, (screen.get_width()/2-200, screen.get_height()/2))
    else:
      screen.blit(game_over, (screen.get_width()/2-180, screen.get_height()/2-40))

    pygame.display.flip()
    clock.tick(60)
  
  score = 0
  running = True
  while running:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()
    
    Player.jump()
    Player.move()
    if accel <= 15:
      accel += 1
    P1.move()
    if P1.check() <= screen.get_width()*(2/3):
      go[1] = True
    if P2.check() <= screen.get_width()*(2/3):
      go[2] = True
    if go[1]:
      P2.move()
    if go[2]:
      P3.move()

    screen.fill("sky blue")

    scores = font.render(str(score), True, "Black")
    screen.blit(scores, (screen.get_width()/2-40, 40))

    Player.draw()
    P1.draw()
    if go[1]:
      P2.draw()
    if go[2]:
      P3.draw()
    
    rects = []
    for pipe in Pipes:
      rects.extend([pipe.top, pipe.bottom])

    if Player.rect.collidelist(rects) != -1 or Player.rect.bottom >= screen.get_height():
      time.sleep(0.5)
      screen.blit(game_over, (screen.get_width()/2-180, screen.get_height()/2-40))
      screen.blit(scores, (screen.get_width()/2-40, 40))
      running = False
    
    pygame.display.flip()
    clock.tick(60)

  game = False
  Player.__init__()
  P1.__init__()
  P2.__init__()
  P3.__init__()
  time.sleep(0.5)
