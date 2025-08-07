import math
from typing import List
from game.combat.bullet import Bullet


def radial_burst(cx: float, cy: float, speed: float, count: int) -> List[Bullet]:
    bullets: List[Bullet] = []
    for i in range(count):
        angle = (2 * math.pi) * (i / count)
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        bullets.append(Bullet(cx, cy, vx, vy))
    return bullets


def aimed_shot(cx: float, cy: float, tx: float, ty: float, speed: float, n: int = 3, spread_deg: float = 15.0) -> List[Bullet]:
    dx = tx - cx
    dy = ty - cy
    base_angle = math.atan2(dy, dx)
    bullets: List[Bullet] = []
    for i in range(n):
        offset = (i - (n - 1) / 2.0) * (spread_deg * math.pi / 180.0)
        angle = base_angle + offset
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed
        bullets.append(Bullet(cx, cy, vx, vy))
    return bullets