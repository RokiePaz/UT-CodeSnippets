from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict
import math
import random

from .course import Course, Gap, Sweeper


@dataclass
class PlayerState:
    x: float
    y: float
    vx: float
    vy: float
    on_ground: bool


class Simulation:
    def __init__(self, course: Course, seed: Optional[int] = None):
        self.course = course
        self.random = random.Random(seed)
        # Physics params (tuned for stability)
        self.dt = 0.02
        self.gravity = -25.0
        self.ground_y = 0.0
        self.player_radius = 0.4
        self.max_time = 120.0
        self.max_steps = int(self.max_time / self.dt)

        # Movement params
        self.max_speed = 8.0
        self.accel = 20.0
        self.friction_ground = 10.0
        self.friction_air = 0.5
        self.jump_speed = 10.5

        # Sweeper interaction
        self.sweeper_knockback_speed = -6.0
        self.sweeper_vertical_boost = 6.0
        self.sweeper_hit_distance = 0.6  # collision tolerance

    def is_over_gap(self, x: float) -> bool:
        for gap in self.course.gaps:
            if gap.contains(x):
                return True
        return False

    def ground_height(self, x: float) -> float:
        return float("-inf") if self.is_over_gap(x) else self.ground_y

    def simulate_step(self, state: PlayerState, action: Dict[str, bool], t: float) -> PlayerState:
        ax = 0.0
        # Horizontal control
        if action.get("left", False):
            ax -= self.accel
        if action.get("right", False):
            ax += self.accel

        # Apply friction
        friction = self.friction_ground if state.on_ground else self.friction_air
        ax += -friction * math.copysign(1.0, state.vx) if abs(state.vx) > 0.01 else 0.0

        # Integrate horizontal
        vx = state.vx + ax * self.dt
        # Clamp
        if vx > self.max_speed:
            vx = self.max_speed
        if vx < -self.max_speed:
            vx = -self.max_speed
        x = state.x + vx * self.dt

        # Vertical/jump
        vy = state.vy
        if action.get("jump", False) and state.on_ground:
            vy = self.jump_speed
        # Gravity
        vy += self.gravity * self.dt
        y = state.y + vy * self.dt

        # Ground collision
        ground_y = self.ground_height(x)
        on_ground = state.on_ground
        if y - self.player_radius <= ground_y:
            y = ground_y + self.player_radius
            vy = 0.0
            on_ground = ground_y != float("-inf")
        else:
            on_ground = False

        # Sweeper collisions
        hit = False
        for sweeper in self.course.sweepers:
            # Consider collisions only near the sweeper along x
            if abs(x - sweeper.center_x) > sweeper.arm_length + 2.0:
                continue
            sx, sy = sweeper.bar_end(t)
            dist = math.hypot(x - sx, y - sy)
            if dist <= self.sweeper_hit_distance:
                hit = True
                break
        if hit:
            vx = min(vx, self.sweeper_knockback_speed)
            vy = max(vy, self.sweeper_vertical_boost)

        return PlayerState(x=x, y=y, vx=vx, vy=vy, on_ground=on_ground)

    def run_episode(self, agent) -> dict:
        state = PlayerState(x=0.0, y=self.ground_y + self.player_radius, vx=0.0, vy=0.0, on_ground=True)
        time_elapsed = 0.0
        distance = 0.0
        for step in range(self.max_steps):
            t = step * self.dt
            obs = {
                "x": state.x,
                "y": state.y,
                "vx": state.vx,
                "vy": state.vy,
                "on_ground": state.on_ground,
                "time": t,
                "course_length": self.course.length,
                "gaps": self.course.gaps,
                "sweepers": self.course.sweepers,
            }
            action = agent.act(obs)
            state = self.simulate_step(state, action, t)
            time_elapsed += self.dt
            distance = state.x

            if state.x >= self.course.length:
                return {
                    "succeeded": True,
                    "time": time_elapsed,
                    "distance": distance,
                    "course_length": self.course.length,
                }

            # Simple failure: fell into a gap beyond some depth
            if state.y < -5.0:
                return {
                    "succeeded": False,
                    "time": time_elapsed,
                    "distance": distance,
                    "course_length": self.course.length,
                }

        return {
            "succeeded": False,
            "time": time_elapsed,
            "distance": distance,
            "course_length": self.course.length,
        }