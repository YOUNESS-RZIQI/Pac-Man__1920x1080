# Pac-Man - Packaged Game Instructions

## --- How to Launch ---

To play the game, open your terminal or command prompt, navigate to this folder, and run the executable with the configuration file as an argument.

**For Linux/macOS:**
```bash
./Pacman config.json
```

**Note:** If the executable does not run on Linux/macOS, ensure it has execution permissions by running:
```bash
chmod +x Pacman
```

You can always download the latest official release from:
https://amine-elh.itch.io/pacman-binary

## --- Display Resolution and Full-Screen Experience ---

For the best visual experience, set your PC's display resolution to **3840 × 2160** before launching the game, if your monitor supports this resolution.

Using the recommended resolution helps the game display its visuals at the intended quality and provides a better full-screen experience, provided that your display and hardware support it.

If your monitor does not support 3840 × 2160, use the highest suitable resolution supported by your display.

**Note:** Changing your PC's display resolution does not automatically enable full-screen mode. Full-screen behavior depends on the game's display implementation.

## --- Configuration Options ---

The game uses the included `config.json` file to set up the levels. You can edit this file in any text editor to change game behavior per level.

Important available options include:
- `"lives"`: Number of starting lives
- `"points_per_pacgum"`: Score awarded per standard Pac-Gum
- `"points_per_super_pacgum"`: Score awarded per Super Pac-Gum
- `"points_per_ghost"`: Score awarded for eating an edible ghost
- `"level_max_time"`: The time limit for the current level

## --- Basic Controls ---

- **Move Up:** Up Arrow or `W`
- **Move Down:** Down Arrow or `S`
- **Move Left:** Left Arrow or `A`
- **Move Right:** Right Arrow or `D`
- **Exit Game:** Escape

Enjoy playing Pac-Man!
