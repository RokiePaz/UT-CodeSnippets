# Fall Guys–Style AI Simulator (Offline)

This project provides a safe, offline obstacle-course simulator inspired by Fall Guys and a simple AI agent that learns heuristics to complete the course. It does not interact with or automate the real game.

## Features
- Simple physics-based runner in 1D horizontal + vertical motion
- Obstacles: ground gaps and a rotating sweeper bar
- Heuristic AI that times jumps to clear gaps and avoid the sweeper
- Deterministic simulation for reproducibility

## Requirements
- Python 3.9+
- See `requirements.txt` for Python dependencies

## Install
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run (AI controlled)
```bash
python3 main.py --ai --episodes 3
```

## Run (manual baseline; prints control hints only)
This demo is headless by default. Manual mode simply runs a slow walk forward.
```bash
python3 main.py --episodes 1
```

## Files
- `main.py`: entry point; runs episodes and prints results
- `src/sim.py`: physics simulation core
- `src/course.py`: course and obstacles
- `src/agent.py`: simple heuristic AI controller

## Notes
- The agent is intentionally simple to keep the example compact.
- You can extend obstacles and improve the AI policy (e.g., predictive timing, PID control, or RL).
