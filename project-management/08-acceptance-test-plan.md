# 08 Acceptance Test Plan

| Test ID | Feature | Preconditions | Test Steps | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AT-001** | Player Movement | Game started | Use directional keys to move Pac-Man. | Pac-Man moves smoothly and respects walls. | Passed |
| **AT-002** | Pacgum Collection | Game started | Move Pac-Man over a pacgum. | Pacgum disappears, score increases. | Passed |
| **AT-003** | Super Pacgum | Game started | Eat a super pacgum. | Ghosts turn edible, speed changes, score increases, sound Play. | Passed |
| **AT-004** | Ghost Collision (Normal) | Game started, ghost normal | Move into a ghost. | Player loses a life, resets position. | Passed |
| **AT-005** | Ghost Collision (Edible) | Ghost is edible | Move into a ghost. | Ghost is eaten, respawns, score increases. | Passed |
| **AT-006** | Cheat Mode | Game started | Activate cheat inputs. | Speed changes / ghost freeze / invincibility applies... | Passed |
| **AT-007** | Game Over | 1 life remaining | Die to a ghost. | Game Over screen displays, high score checked. | Passed |
| **AT-008** | Packaging Executable | Built via PyInstaller | Run the generated executable on a fresh target machine. | Game launches with assets and sounds without error. | Passed |
| **AT-009** | Configuration Load | `config.json` exists | Modify `config.json` (e.g., lives) and launch. | Game respects the JSON configuration values. | Passed |
