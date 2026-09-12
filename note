import pygame

from lane import Lane


NOTE_COLOR = (255, 255, 255)


class Note:
    def __init__(self, lane, y=0):
        # 이 노트가 속한 레인
        self.lane = lane

        # 노트의 위치
        self.x = lane.x + lane.width // 2
        self.y = y

        # 노트 크기
        self.width = 60
        self.height = 20

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            NOTE_COLOR,
            (
                self.x - self.width // 2,
                self.y,
                self.width,
                self.height
            )
        )
