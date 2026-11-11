# 12 Final Project Analysis

## Evolution of the Project
- **Original Concept**: Build a mandatory Pac-Man game.
- **Final Product**: A highly polished, feature-rich game with extra power-ups (tunnels, magnet, booster...), debug cheats, a robust UI (menus, instructions, high scores), and complete sound integration. The game is packaged into a standalone executable and officially distributed on itch.io: [https://amine-elh.itch.io/pacman-binary](https://amine-elh.itch.io/pacman-binary).

## What Worked Well
- The frontend/backend split was highly effective.
- Iterative manual testing caught many edge cases.
- The shared grid representation made backend states easily accessible to the frontend.

## Challenges & Adaptations
- Cross-machine compatibility and packaging caused delays, solved by intensive investigation and `.spec` file modifications.
- Asset creation became a bottleneck.

## Future Improvements (Retrospective)
If doing this again, we would:
1. Start testing the PyInstaller packaging on target environments much earlier.
2. Establish a clearer backlog of visual asset requirements at the start to estimate the workload better.
3. Define the backend/frontend data interfaces earlier to further reduce integration surprises.
