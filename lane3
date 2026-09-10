import pygame


# 화면 크기
WIDTH = 800
HEIGHT = 600

# 레인 색상
LANE_COLOR = (40, 40, 40)
LINE_COLOR = (100, 100, 100)
JUDGEMENT_COLOR = (255, 255, 255)


class Lane:
    def __init__(self, x, width, height, key):
        self.x = x
        self.width = width
        self.height = height

        # 이 레인에 대응하는 키
        self.key = key

        # 판정선의 y 위치
        self.judgement_y = height - 100

    def draw(self, screen):
        # 레인 배경
        pygame.draw.rect(
            screen,
            LANE_COLOR,
            (self.x, 0, self.width, self.height)
        )

        # 레인 오른쪽 경계선
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (self.x + self.width, 0),
            (self.x + self.width, self.height),
            2
        )

        # 판정선
        pygame.draw.line(
            screen,
            JUDGEMENT_COLOR,
            (self.x, self.judgement_y),
            (self.x + self.width, self.judgement_y),
            3
        )


# 4개의 레인
lane_width = WIDTH // 4

lanes = [
    Lane(0, lane_width, HEIGHT, "D"),
    Lane(lane_width, lane_width, HEIGHT, "F"),
    Lane(lane_width * 2, lane_width, HEIGHT, "J"),
    Lane(lane_width * 3, lane_width, HEIGHT, "K")
]
