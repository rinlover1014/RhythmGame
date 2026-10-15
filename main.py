
import pygame
from lane import lanes

# 게임 초기화
pygame.init()

# 화면 설정
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")

clock = pygame.time.Clock()
running = True

# 게임 루프
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 배경 초기화
    screen.fill((0, 0, 0))

    # 레인 그리기
    for lane in lanes:
        lane.draw(screen)

    # 화면 갱신
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
