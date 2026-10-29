import pygame
 
 
# 화면 크기
WIDTH = 800
HEIGHT = 600
 
# 레인 색상
LANE_COLOR = (40, 40, 40)
PRESSED_COLOR = (75, 75, 105)   # 키를 누르고 있을 때
LINE_COLOR = (100, 100, 100)
JUDGEMENT_COLOR = (255, 255, 255)
 
# 레인별 노트 색 (D, F, J, K 순서)
NOTE_COLORS = [(255, 77, 141), (255, 184, 77), (77, 227, 255), (164, 123, 255)]
 
 
class Lane:
    def __init__(self, x, width, height, key, color=(255, 255, 255)):
        self.x = x
        self.width = width
        self.height = height
 
        # 이 레인에 대응하는 키 ("D" -> pygame.K_d)
        self.key = key
        self.key_code = getattr(pygame, "K_" + key.lower())
 
        # 이 레인 노트의 색
        self.color = color
 
        # 지금 키가 눌려 있는지
        self.pressed = False
 
        # 판정선의 y 위치
        self.judgement_y = height - 100
 
    def draw(self, screen):
        # 레인 배경 (키를 누르면 밝아짐)
        pygame.draw.rect(
            screen,
            PRESSED_COLOR if self.pressed else LANE_COLOR,
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
    Lane(0, lane_width, HEIGHT, "D", NOTE_COLORS[0]),
    Lane(lane_width, lane_width, HEIGHT, "F", NOTE_COLORS[1]),
    Lane(lane_width * 2, lane_width, HEIGHT, "J", NOTE_COLORS[2]),
    Lane(lane_width * 3, lane_width, HEIGHT, "K", NOTE_COLORS[3])
]
