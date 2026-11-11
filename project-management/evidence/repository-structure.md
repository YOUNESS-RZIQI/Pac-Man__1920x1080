# Repository Structure Evidence

The actual repository structure reflects the project's complexity and requirements:

- `src/`: Contains all python source code (`pac-man.py`, `Game_Logique.py`, `Sounds_Effects.py`, UI screens).
- `Images/`: Contains the visual pixel-art assets.
- `songs/`: Contains audio assets for gameplay triggers.
- `config.json`: Configuration file for levels, lives, etc.
- `Makefile`: Automates setup, running, linting (`flake8`, `mypy`), and PyInstaller packaging.
- `pyproject.toml` / `uv.lock`: Dependency management (mlx, pygame-ce, mazegenerator).
- `ubuntu/` & `mazegenerator/`: Local wheel dependencies indicating specific packaging solutions.

*(Evidence: Directory listings of the project root and src/ directory).*
