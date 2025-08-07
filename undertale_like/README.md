# Undertale-like Original Game Framework (No IP Content)

This is an original, from-scratch game framework inspired by the mechanics of Undertale (top-down overworld, branching choices, and heart-in-a-box bullet-hell battle), without copying Undertale's dialog, assets, music, or story.

## Features
- Overworld scene: move a character around a room
- Interact key to trigger an original dialogue box
- Battle scene: heart-in-a-box movement with simple bullet patterns
- Modular scenes and state manager for easy extension

## Requirements
- Python 3.9+
- Pygame (installed via requirements.txt)

## Setup and Run
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m game.main
```

## Controls
- Arrow Keys: Move
- Z: Interact / Advance dialogue
- X or ESC: Back / Cancel
- Enter: Confirm

## Notes
- All content is original and placeholder. Feel free to replace `game/data/` dialogues with your own.
- Add your own sprites, sounds, and fonts to `game/assets/` if desired.

## Folder Structure
```
undertale_like/
  README.md
  requirements.txt
  game/
    __init__.py
    main.py
    settings.py
    core/
      scene.py
      state_manager.py
      ui.py
    overworld/
      world.py
      player.py
      npc.py
      dialogue.py
    combat/
      battle.py
      heart.py
      bullet.py
      patterns.py
    data/
      dialogues/
        intro.json
    assets/
      fonts/
      images/
      sounds/
```

## Legal
This project is an homage to gameplay style only. It contains no Undertale IP (no dialog, story, art, names, or music). Replace all placeholder content with your own.