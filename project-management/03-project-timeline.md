# 03 Project Timeline

## Development Progression
Based on the Git history, the project did not follow a rigid predefined schedule. Instead, it was developed progressively, feature by feature.

### Reconstructed Timeline Phases
1. **Initial Setup (Late July - Late August)**: Base project files, initial git setup (`pac-man` init).
2. **Core Mechanics (Early September)**: 
   - Moving ghosts in the maze.
   - Player movement and collisions.
   - Core visual components (coloured virtual printed maze, MLX added).
3. **Advanced Features (Mid to Late September)**: 
   - Power-ups (Boosters, Magnets, Extra lives, Bombs).
   - Cheat modes.
   - Audio integration (Sounds added for various triggers).
4. **Finalisation and Packaging (End of September - Early October)**: 
   - Executable generation and testing.
   - Code optimisation, bug fixing, flake8 and mypy linting.
5. **Documentation & Final Delivery (Early October)**: 
   - Updating README and project management documents.
   - Final review of implemented mechanics and codebase state.

## Gantt Chart Representation

```mermaid
%%{init: {'theme':'dark', 'themeVariables': {
  'critBkgColor':'#ef4444',
  'critBorderColor':'#b91c1c',
  'taskTextColor':'#1b0505',
  'taskTextLightColor':'#1b0505',
  'taskTextDarkColor':'#1b0505',
  'taskTextOutsideColor':'#ffffff'
}}}%%
gantt
    title Reconstructed Project Timeline
    dateFormat  YYYY-MM-DD
    section Setup & Core
    Project Setup           :crit, 2026-07-31, 2026-08-30
    Core Backend Mechanics  :done, 2026-09-01, 2026-09-10
    Core UI & MLX           :done, 2026-09-01, 2026-09-10
    section Advanced Features
    Power-ups & Power-ups UI:done, 2026-09-11, 2026-09-28
    Sound Integration       :done, 2026-09-28, 2026-09-30
    section Finalisation
    Packaging & PyInstaller :done, 2026-09-28, 2026-10-02
    Bug Fixing & Polish     :done, 2026-09-28, 2026-10-02
    section Delivery
    Documentation & Review  :done, 2026-10-03, 2026-10-08
    Last Review             :done, 2026-10-09, 2026-10-11
```

*(Evidence: Git commit history dates spanning from 2026-07-31 to 2026-10-08)*
