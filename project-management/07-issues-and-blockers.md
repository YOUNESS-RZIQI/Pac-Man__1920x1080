# 07 Issues and Blockers Log

| Issues | Description | Impact | Investigation & Solution | Owner | Evidence |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Packaging cross-platform compatibility**: Executable worked on the dev machine but failed elsewhere. | High (Blocks distribution) | The team realized environments weren't identical. Yrziqi fixed asset paths and adapted code for different environments. | Yrziqi | Git commit history, `pacman.spec`, `Makefile` |
| **2** | **Sound overlapping conflicts**: Multiple sounds playing simultaneously causing issues. | Low (Annoying UX) | Implemented checks between player and ghosts to correctly trigger and stop sounds. | Amelhach | Commits: "fixe play or stop sound", "fixe for conflet tow sound" |
| **3** | **MLX Image Layering**: Images rendering in the wrong order or overriding each other. | Medium (Visual bug) | Debugged the MLX rendering pipeline and adjusted draw orders. | Yrziqi | Git commits related to visual polish. |
| **4** | **Flake8 / Numpy / Mypy issues** | Low (Code Quality) | Cleaned up imports and added typing fixes across multiple files. | Amelhach/Yrziqi | Commits: "fixe numpy and flake8", "ceanap my repo" |
