from dataclasses import dataclass
from typing import List
import math


@dataclass(frozen=True)
class Gap:
    start_x: float
    width: float

    def contains(self, x: float) -> bool:
        return self.start_x <= x <= self.start_x + self.width


@dataclass(frozen=True)
class Sweeper:
    center_x: float
    arm_length: float
    height: float
    angular_speed: float  # radians per second
    start_angle: float = 0.0

    def angle_at(self, t: float) -> float:
        return self.start_angle + self.angular_speed * t

    def bar_end(self, t: float) -> tuple[float, float]:
        theta = self.angle_at(t)
        x = self.center_x + self.arm_length * math.cos(theta)
        y = self.height + self.arm_length * math.sin(theta)
        return x, y


@dataclass
class Course:
    length: float
    gaps: List[Gap]
    sweepers: List[Sweeper]


def build_default_course() -> Course:
    length = 120.0

    gaps = [
        Gap(start_x=10.0, width=2.0),
        Gap(start_x=18.0, width=2.5),
        Gap(start_x=26.0, width=3.0),
        Gap(start_x=40.0, width=2.0),
        Gap(start_x=48.0, width=3.5),
    ]

    sweepers = [
        Sweeper(center_x=70.0, arm_length=4.0, height=1.2, angular_speed=1.3, start_angle=0.0),
        Sweeper(center_x=95.0, arm_length=5.0, height=1.4, angular_speed=-1.0, start_angle=math.pi / 4.0),
    ]

    return Course(length=length, gaps=gaps, sweepers=sweepers)