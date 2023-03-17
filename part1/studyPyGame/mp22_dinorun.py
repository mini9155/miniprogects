# dinorun
import pygame
import os

pygame.init()

ASSETS = './studyPyGame/Assets/'

SCREEN = pygame.display.set_mode((1100,600))
Icon = pygame.image.load('./studyPygame/dinoRun.png')
pygame.display.set_icon(Icon)

BG = pygame.image.load(os.path.join(f'{ASSETS}Other','Track.png'))
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoRun2.png')]
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'),
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

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

def main():
    run = True
    clock = pygame.time.Clock()
    dino = Dino()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        SCREEN.fill((255,255,255)) # 배경 흰색
        userinput = pygame.key.get_pressed()

        dino.draw(SCREEN) # 공룡을 그려줘야 함
        dino.update(userinput)

        clock.tick(30) # 프레임 레이트
        pygame.display.update() # 초당 30번 화면을 갱신 해줌

if __name__ == '__main__':
    main()