from __future__ import annotations
from typing import Dict, Any
import math

from .course import Gap, Sweeper


class ManualAgent:
    def act(self, obs: Dict[str, Any]) -> Dict[str, bool]:
        # Simple baseline: walk right slowly, jump very occasionally
        x = obs["x"]
        on_ground = obs["on_ground"]
        action = {"left": False, "right": True, "jump": False}
        # Hop rarely to avoid getting stuck on minor terrain issues
        if on_ground and int(x) % 17 == 0:
            action["jump"] = True
        return action


class HeuristicAgent:
    def __init__(self):
        self.pending_jump_cooldown = 0.0
        self.jump_cooldown_time = 0.25

    def act(self, obs: Dict[str, Any]) -> Dict[str, bool]:
        x = obs["x"]
        y = obs["y"]
        vx = obs["vx"]
        on_ground = obs["on_ground"]
        t = obs["time"]
        gaps = obs["gaps"]
        sweepers = obs["sweepers"]

        action = {"left": False, "right": True, "jump": False}

        # Maintain a target run speed
        target_speed = 6.5
        if vx < target_speed * 0.8:
            action["right"] = True
        else:
            action["right"] = True  # keep pressing right for simplicity

        # Jump policy cooldown
        if self.pending_jump_cooldown > 0.0:
            self.pending_jump_cooldown -= 0.02
        can_jump = on_ground and self.pending_jump_cooldown <= 0.0

        # Lookahead for next gap
        next_gap = self._next_gap_ahead(x, gaps)
        if next_gap is not None and can_jump:
            trigger_dist = self._gap_jump_trigger_distance(next_gap)
            dist_to_start = next_gap.start_x - x
            if 0.2 < dist_to_start <= trigger_dist:
                action["jump"] = True

        # Sweeper avoidance: if near a sweeper and bar is about to pass, jump
        if can_jump and not action["jump"]:
            for sweeper in sweepers:
                if abs(x - sweeper.center_x) < (sweeper.arm_length + 1.0):
                    theta = sweeper.angle_at(t)
                    # When bar is near horizontal crossing our lane, jump
                    normalized = abs(math.sin(theta))
                    if normalized < 0.25:
                        action["jump"] = True
                        break

        if action["jump"]:
            self.pending_jump_cooldown = self.jump_cooldown_time

        return action

    @staticmethod
    def _next_gap_ahead(x: float, gaps: list[Gap]) -> Gap | None:
        ahead = [g for g in gaps if g.start_x + g.width > x]
        ahead.sort(key=lambda g: g.start_x)
        return ahead[0] if ahead else None

    @staticmethod
    def _gap_jump_trigger_distance(gap: Gap) -> float:
        # Empirical trigger based on gap width; larger gaps need earlier jump
        base = 0.9
        return base + 0.6 * gap.width