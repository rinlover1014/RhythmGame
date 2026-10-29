
import pygame
 
from lane import Lane
 
 
# 노트가 떨어지는 속도 (초당 픽셀)
NOTE_SPEED = 450
 
MISSED_COLOR = (70, 70, 80)
 
 
class Note:
    def __init__(self, lane, time):
        # 이 노트가 속한 레인
        self.lane = lane
 
        # 노트가 판정선에 도착해야 하는 시간 (초)
        self.time = time
 
        # 노트의 위치
        self.x = lane.x + lane.width // 2
        self.y = 0
 
        # 노트 크기
        self.width = 120
        self.height = 20
 
        # 이미 처리된 노트인지 (맞췄거나 놓쳤거나)
        self.done = False
        self.missed = False
 
    def update(self, song_time):
        # 위치를 '시간'으로 계산 -> 프레임이 느려져도 박자가 어긋나지 않음
        center_y = self.lane.judgement_y - (self.time - song_time) * NOTE_SPEED
        self.y = center_y - self.height // 2
 
    def draw(self, screen):
        if self.y < -self.height or self.y > screen.get_height():
            return
 
        color = MISSED_COLOR if self.missed else self.lane.color
        pygame.draw.rect(
            screen,
            color,
            (
                self.x - self.width // 2,
                int(self.y),
                self.width,
                self.height
            ),
            border_radius=8
        )
