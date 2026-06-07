# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

2D pixel-art top-down RPG built with Python 3.13 and pygame-ce, structured as a learning exercise for game development fundamentals and data structures/algorithms. Currently in Phase 4 development (NPC + Dialogue system).

## Commands

```bash
# Activate virtual environment and run the game
cd rpg_game
.venv\Scripts\activate
python main.py

# Install dependencies
pip install pygame-ce>=2.5.0
```

No test framework or build system exists yet.

## Architecture

### Scene / State Management

Currently no scene management — everything runs inline in `main.py`'s `main()` function. Phase 4 plans to introduce `src/scenes/scene_base.py` (abstract `Scene`) and `src/scenes/dialogue_scene.py`.

### Entity System (Inheritance Hierarchy)

```
Entity (src/entity.py) — base: tile position, pixel coords, render()
  ├── Player (src/player.py) — move(dx, dy, map), facing direction
  ├── NPC (planned Phase 4) — dialogue tree
  └── Monster (planned Phase 6) — pathfinding + combat AI
```

### Map System

- Map files live in `assets/maps/` as plaintext grids of integers (space-separated).
- `MapLoader` (`src/map_data.py`) parses them into a 2D list and provides `get_tile(col, row)` and `is_walkable(col, row)`.
- `Tile.is_walkable(tile_id)` (`src/tile.py`) is a static utility — only grass (0), path (2), and door (4) are walkable.
- Grid dimensions: 30 tiles wide × 20 tiles tall. Each tile is 32×32 pixels (960×640 screen).

### Data Structures (Planned)

- `src/dsa/` — intended for `DialogueTree` (N-ary tree with BFS/DFS), A*/Dijkstra pathfinding, and linked-list inventory.
- `assets/dialogues/` — JSON files for NPC dialogue trees.

### Game Loop (main.py)

Standard 60 FPS loop: handle events → update → render. Player movement is grid-based via arrow keys. No camera/scrolling yet (offset params exist but are unused).

### Constants

All configuration centralized in `src/constants.py`: screen dimensions, tile types + colors, entity colors, `PATHFINDING_ALGO` toggle, direction mappings.

## Phase Roadmap

| Phase | Feature | Status |
|-------|---------|--------|
| 1 | Project setup + window | Done |
| 2 | Map system | Done |
| 3 | Player + collision | Done |
| 4 | NPC + Dialogue system | In progress |
| 5 | Inventory (Linked List) | Planned |
| 6 | Pathfinding + Monsters | Planned |
| 7 | Combat | Planned |
| 8 | Pathfinding comparison | Planned |

Detailed plans (in Chinese) are in `rpg_game/PROGRESS.md`.
