import argparse
from typing import Optional

from src.sim import Simulation
from src.course import build_default_course
from src.agent import HeuristicAgent, ManualAgent


def run_episode(use_ai: bool, seed: Optional[int] = None) -> dict:
    course = build_default_course()
    sim = Simulation(course=course, seed=seed)
    agent = HeuristicAgent() if use_ai else ManualAgent()
    result = sim.run_episode(agent=agent)
    return result


def main():
    parser = argparse.ArgumentParser(description="Fall Guys–style AI Simulator (offline)")
    parser.add_argument("--ai", action="store_true", help="Use AI agent instead of manual baseline")
    parser.add_argument("--episodes", type=int, default=1, help="Number of episodes to run")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = parser.parse_args()

    num_success = 0
    best_time = None

    for i in range(args.episodes):
        seed = None if args.seed is None else args.seed + i
        result = run_episode(use_ai=args.ai, seed=seed)
        succeeded = result["succeeded"]
        t = result["time"]
        num_success += 1 if succeeded else 0
        if succeeded and (best_time is None or t < best_time):
            best_time = t
        status = "SUCCESS" if succeeded else "FAIL"
        print(f"Episode {i+1}/{args.episodes}: {status} in {t:.2f}s  (distance={result['distance']:.1f}/{result['course_length']:.1f})")

    print("\nSummary:")
    print(f"  Episodes: {args.episodes}")
    print(f"  Successes: {num_success}")
    if best_time is not None:
        print(f"  Best time: {best_time:.2f}s")


if __name__ == "__main__":
    main()