from enum import Enum


class Judgement(Enum):
    PERFECT = "PERFECT"
    GREAT = "GREAT"
    GOOD = "GOOD"
    BAD = "BAD"
    MISS = "MISS"


class JudgementSystem:
    def judge(self, note_time, input_time):
        difference = abs(note_time - input_time)

        if difference <= 0.05:
            return Judgement.PERFECT

        elif difference <= 0.10:
            return Judgement.GREAT

        elif difference <= 0.15:
            return Judgement.GOOD

        elif difference <= 0.20:
            return Judgement.BAD

        else:
            return Judgement.MISS

if __name__ == "__main__":
    judgement_system = JudgementSystem()

    note_time = 10.0

    print(judgement_system.judge(note_time, 10.01).value)
    print(judgement_system.judge(note_time, 10.08).value)
    print(judgement_system.judge(note_time, 10.13).value)
    print(judgement_system.judge(note_time, 10.18).value)
    print(judgement_system.judge(note_time, 10.50).value)
