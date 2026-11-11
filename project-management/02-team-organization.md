# 02 Team Organization

The team divided responsibilities to allow clear ownership, making development faster and debugging easier.

## Responsibility Matrix

| Area | Amelhach | Yrziqi |
| :--- | :--- | :--- |
| **Backend/game logic** | Lead | Support |
| **Maze** | Lead | Integration |
| **Player** | Lead | UI integration |
| **Ghosts** | Lead | UI integration |
| **Pacgums & Power-ups** | Lead | UI integration |
| **MLX & UI** | Support | Lead |
| **Main menu & Instructions** | Support | Lead |
| **Game over & Win screens** | Backend support | Lead |
| **Configuration** | Support | Lead |
| **Sounds** | Lead | Integration |
| **Assets** | Shared | Lead |
| **Testing** | Shared | Shared |
| **Packaging** | Lead | Support |

## Collaboration Model
While Amelhach owned the backend logic and Yrziqi owned the UI/visualisation, the separation was not a strict wall. 
Integration required frequent communication (mostly via Discord, GitHub, and Teldraw). A key technical choice enabling this was the **shared grid/state representation**, which allowed the frontend to easily query the game state without repeatedly passing manual values.
