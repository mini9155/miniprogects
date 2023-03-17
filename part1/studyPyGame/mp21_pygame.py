import pygame

pygame.init()
win = pygame.display.set_mode((1000,500))

bg_img = pygame.image.load('./studyPyGame/back.png')
BG = pygame.transform.scale(bg_img,(1000,500)) # 사이즈 업
pygame.display.set_caption('게임 만들기')
Icon = pygame.image.load('./studyPygame/game.png')
pygame.display.set_icon(Icon)

width = 1000
loop = 0
run = True
while run:
    win.fill((0,0,0)) # 전체 배경을 검은색으로
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # 배경을
    win.blit(BG,(loop,0))
    win.blit(BG, (width +loop, 0))
    if loop == -width:
        loop = 0

    loop -= 1

    pygame.display.update()