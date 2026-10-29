from enum import Enum
 
 
class Judgement(Enum):
    PERFECT = "PERFECT"
    GREAT = "GREAT"
    GOOD = "GOOD"
    BAD = "BAD"
    MISS = "MISS"
 
 
class JudgementSystem:
    # 판정 범위 (초) - 숫자를 바꾸면 난이도가 바뀝니다
    PERFECT_WINDOW = 0.05
    GREAT_WINDOW = 0.10
    GOOD_WINDOW = 0.15
    BAD_WINDOW = 0.20
 
    # 부동소수점 오차 보정 (0.05초 딱 맞는 입력이 GREAT로 밀리는 것 방지)
    EPSILON = 1e-9
 
    def judge(self, note_time, input_time):
        difference = abs(note_time - input_time)
 
        if difference <= self.PERFECT_WINDOW + self.EPSILON:
            return Judgement.PERFECT
        elif difference <= self.GREAT_WINDOW + self.EPSILON:
            return Judgement.GREAT
        elif difference <= self.GOOD_WINDOW + self.EPSILON:
            return Judgement.GOOD
        elif difference <= self.BAD_WINDOW + self.EPSILON:
            return Judgement.BAD
        else:
            return Judgement.MISS
