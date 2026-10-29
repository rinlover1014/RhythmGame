
import array
import math
import os
import time
 
import pygame
 
from chart import BPM, CHARTS
from judgement_system import JudgementSystem
from lane import lanes
from note import Note
 
 
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
 
# 화면 설정
WIDTH = 802
HEIGHT = 600
 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rhythm Game")
 
clock = pygame.time.Clock()
 
FONT_NAMES = "malgungothic,applegothic,nanumgothic,arial"
font_big = pygame.font.SysFont(FONT_NAMES, 72, bold=True)
font = pygame.font.SysFont(FONT_NAMES, 32, bold=True)
font_small = pygame.font.SysFont(FONT_NAMES, 22)
 
# ---------------------------------------------------------------
# 곡 설정
# ---------------------------------------------------------------
SONG_TITLE = "끝났다는 것은 다시 시작된다는 것을"
MUSIC_FILE = "끝났다는 것은 다시 시작된다는 것을.mp3"  # 이 파일을 main.py와 같은 폴더에 넣어 주세요
LEAD_IN = 3.0                # 시작 전 카운트다운 (초)
LEVELS = ["EASY", "NORMAL", "HARD"]
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_PATH = os.path.join(BASE_DIR, MUSIC_FILE)
OFFSET_PATH = os.path.join(BASE_DIR, "offset.txt")
HAS_MUSIC = os.path.exists(MUSIC_PATH)
 
# 싱크 보정(초): 노트가 소리보다 빠르다고 느껴지면 + 쪽으로 (← → 키, 저장됨)
try:
    with open(OFFSET_PATH) as fh:
        offset = float(fh.read())
except (OSError, ValueError):
    offset = 0.0
 
# ---------------------------------------------------------------
# 판정 설정
# ---------------------------------------------------------------
judgement_system = JudgementSystem()
HIT_WINDOW = judgement_system.BAD_WINDOW   # 이 범위 안에서 누르면 판정
WEIGHT = {"PERFECT": 1.0, "GREAT": 0.7, "GOOD": 0.4, "BAD": 0.2, "MISS": 0.0}
JUDGE_COLOR = {
    "PERFECT": (255, 225, 77),
    "GREAT": (77, 227, 255),
    "GOOD": (157, 255, 157),
    "BAD": (255, 150, 100),
    "MISS": (150, 140, 175),
}
 
 
def make_click(freq, ms=60, volume=0.4):
    """음악 파일이 없을 때 쓰는 메트로놈 소리 (코드로 생성)."""
    init = pygame.mixer.get_init()
    if not init:
        return None
    rate, _, channels = init
    count = int(rate * ms / 1000)
    samples = array.array("h")
    for i in range(count):
        v = int(32767 * volume * math.sin(2 * math.pi * freq * i / rate) * (1 - i / count))
        for _ in range(channels):
            samples.append(v)
    return pygame.mixer.Sound(buffer=samples.tobytes())
 
 
click_high = make_click(1500)
click_low = make_click(1000, volume=0.25)
 
state = "select"      # select(곡 선택) / play / result
level = "NORMAL"
notes = []
start_clock = 0.0
points = 0.0
combo = max_combo = 0
counts = {}
popup, popup_time = "", -10.0
last_beat = -1
music_started = False
 
 
def song_time():
    """곡이 시작된 후 흐른 시간(초). 카운트다운 동안은 음수."""
    return time.perf_counter() - start_clock - LEAD_IN - offset
 
 
def start(level_name):
    global state, level, notes, start_clock, points, combo, max_combo
    global counts, popup, popup_time, last_beat, music_started
 
    level = level_name
    notes = [Note(lanes[lane], tm) for tm, lane in CHARTS[level]]
    points = 0.0
    combo = max_combo = 0
    counts = {"PERFECT": 0, "GREAT": 0, "GOOD": 0, "BAD": 0, "MISS": 0}
    popup, popup_time = "", -10.0
    last_beat = -1
    music_started = False
    for lane in lanes:
        lane.pressed = False
 
    # 음악은 미리 불러 두고(끊김 방지), 카운트다운이 끝나는 순간 재생
    if HAS_MUSIC:
        pygame.mixer.music.load(MUSIC_PATH)
    start_clock = time.perf_counter()
    state = "play"
 
 
def to_menu():
    global state
    pygame.mixer.music.stop()
    state = "select"
 
 
def register(name):
    global points, combo, max_combo, popup, popup_time
    counts[name] += 1
    points += WEIGHT[name]
    if name == "MISS":
        combo = 0
    else:
        combo += 1
        max_combo = max(max_combo, combo)
    popup = name
    popup_time = time.perf_counter()
 
 
def judge(lane, t):
    """키를 눌렀을 때: 그 레인에서 가장 가까운 노트를 찾아 판정."""
    for note in notes:
        if note.done or note.lane is not lane:
            continue
        delta = t - note.time
        if delta > HIT_WINDOW:      # 너무 늦음 (곧 MISS 처리됨)
            continue
        if delta < -HIT_WINDOW:     # 아직 너무 이름 -> 무시
            break
        result = judgement_system.judge(note.time, t)
        note.done = True
        register(result.value)
        break
 
 
def score():
    return round(points / len(notes) * 1_000_000)
 
 
def grade():
    acc = points / len(notes) * 100
    return "S" if acc >= 95 else "A" if acc >= 85 else "B" if acc >= 70 else "C"
 
 
def text(surface_font, msg, color, center):
    img = surface_font.render(msg, True, color)
    screen.blit(img, img.get_rect(center=center))
 
 
def change_offset(delta):
    global offset
    offset = round(offset + delta, 3)
    try:
        with open(OFFSET_PATH, "w") as fh:
            fh.write(str(offset))
    except OSError:
        pass
 
 
running = True
 
# 게임 루프
while running:
    clock.tick(60)
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                change_offset(-0.01)
            elif event.key == pygame.K_RIGHT:
                change_offset(0.01)
            elif state == "select":
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    start(LEVELS[event.key - pygame.K_1])
            elif state == "result":
                if event.key == pygame.K_r:
                    start(level)
                elif event.key == pygame.K_m:
                    to_menu()
            elif state == "play":
                for lane in lanes:
                    if event.key == lane.key_code:
                        lane.pressed = True
                        judge(lane, song_time())
        elif event.type == pygame.KEYUP:
            for lane in lanes:
                if event.key == lane.key_code:
                    lane.pressed = False
 
    t = song_time() if state != "select" else 0.0
 
    # --- 업데이트 ---
    if state == "play":
        # 카운트다운이 끝나는 순간 음악 시작 (시계를 그 순간에 맞춰 다시 고정)
        if t >= 0 and not music_started:
            music_started = True
            if HAS_MUSIC:
                pygame.mixer.music.play()
                start_clock = time.perf_counter() - LEAD_IN - offset
                t = song_time()
 
        # 음악 파일이 없으면 메트로놈
        beat = math.floor(t / (60 / BPM))
        if t >= 0 and beat > last_beat:
            last_beat = beat
            if not HAS_MUSIC:
                sound = click_high if beat % 4 == 0 else click_low
                if sound:
                    sound.play()
 
        # 놓친 노트 처리
        for note in notes:
            if note.done:
                continue
            if t - note.time > HIT_WINDOW:
                note.done = True
                note.missed = True
                register("MISS")
            elif note.time - t > 2:
                break
 
        if all(n.done for n in notes) and t > notes[-1].time + 1.0:
            state = "result"
            pygame.mixer.music.fadeout(1500)
 
    # --- 그리기 ---
    screen.fill((11, 8, 32))
 
    if state == "select":
        text(font_big, "RHYTHM GAME", (255, 255, 255), (WIDTH // 2, 120))
        text(font, SONG_TITLE, (255, 184, 77), (WIDTH // 2, 190))
        for i, name in enumerate(LEVELS):
            text(font, f"{i + 1}   {name}   ({len(CHARTS[name])} notes)",
                 (200, 190, 230), (WIDTH // 2, 280 + i * 55))
        text(font_small, "숫자 키로 난이도를 고르세요      D F J K 로 플레이", (255, 255, 255), (WIDTH // 2, 480))
        if not HAS_MUSIC:
            text(font_small, f"{MUSIC_FILE} 파일이 없어 메트로놈으로 시작합니다", (255, 120, 120), (WIDTH // 2, 520))
    else:
        for lane in lanes:
            lane.draw(screen)
            label = font.render(lane.key, True, lane.color if not lane.pressed else (255, 255, 255))
            screen.blit(label, label.get_rect(center=(lane.x + lane.width // 2, lane.judgement_y + 40)))
 
        for note in notes:
            if note.done and not note.missed:
                continue
            note.update(t)
            note.draw(screen)
 
        # 점수 / 콤보 / 진행도
        text(font, f"{score():07d}", (255, 255, 255), (WIDTH // 2, 36))
        progress = max(0, min(1, t / (notes[-1].time + 1)))
        pygame.draw.rect(screen, (255, 77, 141), (0, 0, int(WIDTH * progress), 4))
        if combo > 1:
            text(font_big, str(combo), (255, 255, 255), (WIDTH // 2, 210))
            text(font_small, "COMBO", (255, 184, 77), (WIDTH // 2, 255))
        if popup and time.perf_counter() - popup_time < 0.4:
            text(font, popup, JUDGE_COLOR[popup], (WIDTH // 2, 400))
        if t < 0:
            text(font_big, str(math.ceil(-t)), (255, 255, 255), (WIDTH // 2, 300))
            text(font_small, f"싱크 보정 ← → : {offset * 1000:+.0f}ms", (200, 190, 230), (WIDTH // 2, 360))
 
    # 결과 화면
    if state == "result":
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((11, 8, 32, 215))
        screen.blit(veil, (0, 0))
        text(font_big, grade(), (255, 225, 77), (WIDTH // 2, 130))
        text(font_big, f"{score():,}", (255, 255, 255), (WIDTH // 2, 220))
        if counts["MISS"] == 0:
            text(font, "FULL COMBO!", (255, 225, 77), (WIDTH // 2, 280))
        line = "   ".join(f"{k} {v}" for k, v in counts.items())
        text(font_small, line, (200, 190, 230), (WIDTH // 2, 340))
        text(font_small, f"{level}   MAX COMBO {max_combo}", (200, 190, 230), (WIDTH // 2, 375))
        text(font_small, "R : 다시 하기      M : 곡 선택      ESC : 종료", (255, 255, 255), (WIDTH // 2, 450))
 
    pygame.display.flip()
 
pygame.quit()
