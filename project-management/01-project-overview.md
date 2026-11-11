# 01 Project Overview

## Original Goal
The team's objective was to build one of the strongest and most impressive Pac-Man projects in the school, significantly exceeding the minimum mandatory requirements.

## What Was Actually Built
The project evolved into a robust game containing features far beyond the basic implementation:
- Core gameplay mechanics (Pac-Man, Ghosts, Pacgums, Super Pacgums, Collisions, Score, Lives).
- Additional gameplay features (Tunnels, Magnet, Booster, bombs, extra time ...).
- Multiple game levels and level progression.
- Robust UI elements (Main menu, Instructions, Game Over, Win screen, Top 10 High scores, Start Game).
- A complete sound system tied to gameplay triggers.
- Cheat/debug functionalities.
- Packaging using PyInstaller.

## Technology Stack
- **Language**: Python (imposed by subject).
- **Graphics/UI**: MLX (chosen for direct, low-level graphical control without unnecessary compatibility layers).
- **Assets**: Custom pixel-art assets prepared with LibreSprite.
- **Packaging**: PyInstaller, Makefile.

## Key Choices
- **Backend/Frontend Separation**: Facilitated independent development and simplified debugging.
- **Direct MLX Usage**: Gave low-level control of the required graphical operations.
- **Structured Data**: Kept internal state representations clean instead of passing confusing raw numeric values.
- **Sounds and Polish**: Added immersion and entertainment value.
