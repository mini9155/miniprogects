# dinorun
import pygame
import os
import random

pygame.init()

ASSETS = 'C:/source/miniprogects/part1/studyPyGame/Assets/'
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,600))
Icon = pygame.image.load('C:/source/miniprogects/part1/studyPyGame/dino.png')
pygame.display.set_icon(Icon)

BG = pygame.image.load(os.path.join(f'{ASSETS}Other','Track.png'))
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png') 
BIRD =[ pygame.image.load(f'{ASSETS}Bird/Bird1.png'),
       pygame.image.load(f'{ASSETS}Bird/Bird2.png')]
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]
SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]
class Cloud:
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(300, 500)
        self.y = random.randint(50,100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width: # 화면 밖으로 벗어나면
            self.x = SCREEN_WIDTH + random.randint(1300,2000)
            self.y = random.randint(50, 100)
    def draw(self,SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

class Dino: # 공룡 클래스


    X_POS = 80; Y_POS = 310; Y_POS_DUCK = 340; JUMP_VEL = 9.0

    def __init__(self) -> None:
        self.run_img = RUNNING
        self.duck_img = DUCKING
        self.jump_img = JUMPING

        self.dino_run = True; self.dino_duck = False; self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userinput) -> None: # 리턴하는 게 없다
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10: self.step_index = 0

        if userinput[pygame.K_UP] and not self.dino_jump:# 점프
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
        elif userinput[pygame.K_DOWN] and not self.dino_jump: #수구리
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not(self.dino_jump or userinput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <- self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL


    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))
 

class Obstacle: # 장애물 클래스(부모클래스)
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH # 1100부터

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width: # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop() # 장애물리스트에 하나 꺼내오기

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle): # 장애물 클래스 상속 클래스
    def __init__(self, image) -> None:
        self.type = 0 # 새는 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0# 0이미지로 시작
    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)

class smallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0,2)
        super().__init__(image, self.type)
        self.rect.y = 300



def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    x_pos_bg = 0
    y_pos_bg = 380
    run = True
    points = 0
    clock = pygame.time.Clock()
    dino = Dino() # 공룡객체 생성
    cloud =Cloud()
    game_speed = 14
    obstacles = []

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20)


    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 10

        txtScore = font.render(f'score : {points}',True, (83,83,83))
        txtRect =  txtScore.get_rect()
        txtRect.center = (1000,40)
        SCREEN.blit(txtScore, txtRect)

    # 함수 내 함수(배경 그리기)
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0

        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255,255,255)) # 배경 흰색
        userinput = pygame.key.get_pressed()
        
        background()
        score()

        cloud.draw(SCREEN)
        cloud.update()

        dino.draw(SCREEN) # 공룡을 그려줘야 함
        dino.update(userinput)

        if len(obstacles) == 0:
            if random.randint(0,2) == 0:
                obstacles.append(smallCactus(SMALL_CACTUS)) 
            elif random.randint(0,2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0,2) == 2:   
                obstacles.append(Bird(BIRD))
        
        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            # collision Detection
            if dino.dino_rect.colliderect(obs.rect):
                pygame.draw.rect(SCREEN, (255,0,0), dino.dino_rect, 3)



        clock.tick(40) # 프레임 레이트
        pygame.display.update() # 초당 30번 화면을 갱신 해줌

if __name__ == '__main__':
    main()