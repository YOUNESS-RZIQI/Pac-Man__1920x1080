"""Define core game logic, state management, and level creation."""

from Game_Library import Maze, Direction, Player, Ghost, Cell, Eyes
from Files_Tools import PacManFilesTools
from typing import List, Tuple, Dict
from Sounds_Effects import Sounds
from Files_Tools import FileTools
import time


class Game:
    """Represent a single game session with its maze, player, and ghosts."""

    def __init__(self, maze: Maze, player: Player, ghosts: List[Ghost],
                 eyess: List[Eyes], time_limit: int, pacgum_score: int,
                 super_pacgum_score: int, ghost_score: int) -> None:
        """Initialize the game session.

        Args:
            maze: The maze for this game session.
            player: The player object.
            ghosts: List of ghost objects.
            eyess: List of eyess objects.
            time_limit: Maximum time allowed for the level in seconds.
            pacgum_score: Points awarded for eating a pac-gum.
            super_pacgum_score: Points awarded for eating a super pac-gum.
            ghost_score: Points awarded for eating a ghost.
        """
        self.level: int = 0
        self.maze: Maze = maze
        self.player: Player = player
        self.eyess: List[Eyes] = eyess
        self.ghosts: List[Ghost] = ghosts

        self.booster: bool = False
        self.bomb_until: float = 0
        self.start_time: float = 0
        self.pause_time: float = 0
        self.pause_start: float = 0
        self.ghost_freeze: bool = False

        self.time_limit: int = time_limit
        self.ghost_score: int = ghost_score
        self.pacgum_score: int = pacgum_score
        self.super_pacgum_score: int = super_pacgum_score

        self.sounds_obj: Sounds = Sounds()
        self.sounds_obj.init_sounds()

        self.maze.grid[self.player.y][self.player.x].player = True
        self.maze.grid[self.player.y][self.player.x].pacgum = False

        for ghost in self.ghosts:
            cell: Cell = self.maze.grid[ghost.y][ghost.x]
            cell.obj_ghost.append(ghost)
            cell.ghost = True

        self.player.magnet = True

    def update(self, direction: Direction) -> None:
        """
        Update the game state for one frame in the given direction.

        Args:
            direction: Direction in which the player moves.
        """
        can_move: bool = self.maze.can_move(
            self.player.x, self.player.y, direction)

        in_tunnel = (self.player.y, self.player.x) in (
            self.maze.tunnel_a_pos, self.maze.tunnel_b_pos)

        if self.player.direction and not in_tunnel and not self.maze.can_move(
             self.player.x, self.player.y, self.player.direction):

            self.player.direction = Direction.NONE

        if can_move and not self.player.is_counting:
            self.player.direction = direction

        elif can_move and not self.maze.can_move(
                self.player.x, self.player.y, self.player.direction):
            self.player.direction = direction
            self.player.player_count = 0

        self.player.is_counting = True
        self.player.player_count += self.player.player_speed

        if (in_tunnel and not self.player.in_tunnel):
            self.teleport_player_tunnel()
            cell = self.maze.grid[self.player.y][self.player.x]
            self.check_pacgum_eating(cell)
            self.player.player_count = 0

        if self.player.player_count >= 90:
            self.player.is_counting = False

            if self.player.direction:
                self.player.move(self.maze, self.player.direction)
                self.player.in_tunnel = False

            self.player.player_count -= 90

            cell = self.maze.grid[self.player.y][self.player.x]
            self.check_booster()
            self.handle_extra_life()
            self.check_magnet_eating()
            self.check_pacgum_eating(cell)
            self.check_super_pacgum_eating(cell)

            for ghost in self.ghosts:
                self.check_ghost_position(ghost)

        self.extra_time()
        self.check_bomb()

        if self.is_game_over():
            return

        self.ghost_see_player_sound()

        for ghost in self.ghosts:
            if ghost.edible and ghost.ghost_speed > 1:
                ghost.ghost_speed = ghost.tmp_ghost_speed // 2
            else:
                ghost.ghost_speed = ghost.tmp_ghost_speed

            ghost.ghost_count += ghost.ghost_speed

            if ghost.ghost_count >= 90:

                ghost.check_edible_time()

                if ghost.handle_ghost_respawn(self.maze, self.player):
                    continue

                if not self.ghost_freeze:
                    ghost.move(self.maze, self.player)

                self.check_ghost_position(ghost)
                ghost.ghost_count -= 90

        for eyes in self.eyess:
            eyes.counter += eyes.speed
            if eyes.counter >= 90:
                eyes.move_eyes(self.maze)
                eyes.counter -= 90

    def check_ghost_position(self, ghost: Ghost) -> None:
        """
        Check if the player and a ghost are on the same cell and react.

        Args:
            ghost: Ghost whose position is checked.
        """
        if ghost.respawn_at:
            return

        if self.player.x == ghost.x and self.player.y == ghost.y:
            if ghost.edible:
                self.eat_ghost(ghost)
                self.sounds_obj.pacman_eat_ghost__sound()
            elif not self.player.invincible:
                self.eat_player()
                self.sounds_obj.play_pacman_death_sound()

    def eat_ghost(self, ghost: Ghost) -> None:
        """
        Handle the player eating an edible ghost.

        Args:
            ghost: Ghost eaten by the player.
        """
        self.player.score += self.ghost_score
        ghost.respawn_at = time.time() + 5
        if ghost.obj_eyes:
            ghost.obj_eyes.put_eyes(self.maze)
        ghost.respawn(self.maze, self.player)

    def eat_player(self) -> None:
        """Handle ghost collision, reduce lives, and reset positions."""
        self.player.respawn(self.maze)
        self.player.lives -= 1
        self.reset_ghosts()

    def check_pacgum_eating(self, cell: Cell) -> None:
        """
        Check if the player is on a pac-gum cell and collect it.

        Args:
            cell: Cell checked for a pac-gum.
        """
        if cell.pacgum:
            cell.pacgum = False
            self.player.score += self.pacgum_score

    def check_super_pacgum_eating(self, cell: Cell) -> None:
        """
        Check if the player is on a super pac-gum cell and collect it.

        Args:
            cell: Cell checked for a super pac-gum.
        """
        if cell.super_pacgum:
            self.sounds_obj.eat_super_pacgum_sound()
            cell.super_pacgum = False
            self.player.score += self.super_pacgum_score
            for ghost in self.ghosts:
                ghost.set_edible()

    def reset_ghosts(self) -> None:
        """Respawn all ghosts to their starting positions."""
        for ghost in self.ghosts:
            ghost.respawn(self.maze, self.player)

    def level_complete(self) -> bool:
        """Return True if all pac-gums in the maze have been eaten."""
        for row in self.maze.grid:
            for cell in row:
                if cell.pacgum:
                    return False
        return True

    def time_over(self) -> bool:
        """Return True if the time limit for the level has been reached."""
        elapsed: float = time.time() - self.start_time
        return elapsed >= (self.time_limit + self.pause_time)

    def get_time_left(self) -> int:
        """Return the number of seconds remaining in the level."""
        elapsed: float = time.time() - self.start_time
        return max(0, int((self.time_limit + self.pause_time) - elapsed))

    def pause_game_time(self, pause: bool) -> None:
        """
        Start or end the pause and update active timers.

        Args:
            pause: True to end the pause, False to start it.
        """
        if pause:
            p_time: float = time.time() - self.pause_start
            self.pause_time += p_time
            self.player.booster_until += p_time
            self.player.magnet_until += p_time
            self.bomb_until += p_time
            for ghost in self.ghosts:
                ghost.edible_until += p_time

        if not pause:
            self.pause_start = time.time()

    def start_game_timer(self) -> None:
        """Start the game countdown timer."""
        self.pause_time = 0
        self.start_time = time.time() + 1

    def is_game_over(self) -> bool:
        """Return True if the player is dead or time has expired."""
        return self.player.is_dead() or self.time_over()

    def cheat_mode(self, invincible: bool = False,
                   ghost_freeze: bool = False, extra_lives: int = 0,
                   player_speed: int = 0, ghost_speed: int = 0) -> None:
        """Apply cheat mode modifications to the game state.

        Args:
            invincible: Toggle player invincibility.
            ghost_freeze: Toggle ghost movement freezing.
            extra_lives: Number of extra lives to add to the player.
            player_speed: Amount to adjust the player's speed.
            ghost_speed: Amount to adjust all ghosts' speed.
        """
        if invincible:
            self.player.invincible = not self.player.invincible

        if ghost_freeze:
            self.ghost_freeze = not self.ghost_freeze

        if extra_lives:
            self.player.lives += extra_lives

        if player_speed:
            speed: int = max(1,
                             min(90, self.player.player_speed + player_speed))
            self.player.player_speed = speed

        if ghost_speed:
            for ghost in self.ghosts:
                minimum_speed: int = min(90, ghost.ghost_speed + ghost_speed)
                ghost.ghost_speed = max(1, minimum_speed)

                min_speed: int = min(90, ghost.tmp_ghost_speed + ghost_speed)
                ghost.tmp_ghost_speed = max(1, min_speed)

    def transfer_player_state(self, next_game: "Game") -> None:
        """
        Transfer the player's score and lives to the next game.

        Args:
            next_game: Game instance receiving the player's state.
        """
        next_game.player.score = self.player.score
        next_game.player.lives += self.player.lives

    def handle_extra_life(self) -> None:
        """Spawn and collect an extra life pickup."""
        x, y = self.maze.live_pos
        if self.player.lives == 1:
            if self.maze.live_pos == (None, None):
                self.maze.live_pos = self.maze.spawn_new_position()
                x, y = self.maze.live_pos
                self.maze.grid[y][x].add_live = True

            x, y = self.maze.live_pos

            if self.player.y == y and self.player.x == x:
                self.sounds_obj.eat_heart_sound()
                self.maze.grid[y][x].add_live = False
                self.player.lives += 1
                self.maze.live_pos = (None, None)

        elif (x is not None and y is not None
              and self.maze.grid[y][x].add_live and self.player.lives > 1):
            self.maze.live_pos = (None, None)
            self.maze.grid[y][x].add_live = False

    def check_magnet_eating(self) -> None:
        """Handle magnet collection, activation, and expiry."""
        x, y = self.maze.magnet_pos

        if self.player.x == x and self.player.y == y:
            self.sounds_obj.eat_magneet_or_power_sound()
            self.maze.grid[y][x].magnet = False

            self.player.magnet_until = time.time() + 15.0
            self.player.magnet = True
            self.maze.magnet_pos = (None, None)

        if self.player.magnet and time.time() >= self.player.magnet_until:
            self.player.magnet_until = 0.0
            self.player.magnet = False

            self.maze.magnet_pos = self.maze.spawn_new_position()
            x, y = self.maze.magnet_pos
            self.maze.grid[y][x].magnet = True

        self.magnet_pacgums()

    def magnet_pacgums(self) -> None:
        """Collect nearby pac-gums when the magnet is active."""
        if not self.player.magnet:
            return

        positions: List[Tuple[int, int]] = [
            (self.player.x, self.player.y),
            (self.player.x + 1, self.player.y),
            (self.player.x - 1, self.player.y),
            (self.player.x, self.player.y + 1),
            (self.player.x, self.player.y - 1),
        ]

        for x, y in positions:
            if 0 <= x < self.maze.width and 0 <= y < self.maze.height:
                cell = self.maze.grid[y][x]
                if cell.pacgum:
                    cell.pacgum = False
                    self.player.score += self.pacgum_score

    def teleport_player_tunnel(self) -> None:
        """Teleport the player through the tunnel to the other tunnel exit."""
        y, x = self.maze.tunnel_a_pos
        old_y: int = self.player.y

        if self.player.y == y:
            self.player.y = y + 2
        else:
            self.player.y = y

        self.maze.grid[old_y][x].player = False
        self.maze.grid[self.player.y][x].player = True
        self.player.in_tunnel = True
        self.sounds_obj.tunnel_sound()

    def ghost_see_player_sound(self) -> None:
        """Play a ghost sound when a ghost spots the player."""
        for ghost in self.ghosts:
            if self.sounds_obj.trol_sounds and not ghost.edible:
                if ghost.Did_you_see_the_player(self.maze, self.player):
                    self.sounds_obj.ghost_trol_sound()
                    return

    def check_booster(self) -> None:
        """Check if the player collected a booster and
            manage its activation and expiry."""
        speed: int = 3

        booster_expired: bool = self.player.booster_until <= time.time()
        if self.maze.booster == (None, None) and booster_expired:
            self.maze.booster = self.maze.spawn_new_position()
            x, y = self.maze.booster
            self.maze.grid[y][x].booster = True

        b_x, b_y = self.maze.booster

        if (b_x is not None and b_y is not None
                and self.player.y == b_y and self.player.x == b_x):

            self.sounds_obj.eat_magneet_or_power_sound()
            self.player.player_speed += speed
            self.maze.grid[b_y][b_x].booster = False
            self.player.booster_until = time.time() + 15
            self.booster = True
            self.maze.booster = (None, None)

        booster_expired = self.player.booster_until <= time.time()
        if self.booster and booster_expired:
            self.player.player_speed -= speed
            self.booster = False

    def check_bomb(self) -> None:
        """
        Check the bomb state, respawn it when necessary, and handle collisions.

        The bomb is respawned when there is no active bomb or when its timer
        expires.
        """
        x, y = self.maze.bomb_pos

        if (x is not None and y is not None and self.maze.grid[y][x].is_bomb):
            self.maze.grid[y][x].is_bomb = False

        if (self.maze.bomb_pos == (None, None) or
                self.bomb_until <= time.time()):
            x, y = self.maze.bomb_pos

            if x is not None and y is not None:
                self.maze.grid[y][x].bomb = False

            self.maze.bomb_pos = self.maze.spawn_new_position()
            x, y = self.maze.bomb_pos
            self.maze.grid[y][x].bomb = True
            self.bomb_until = time.time() + 1

        for ghost in self.ghosts:
            if ghost.y == y and ghost.x == x and not ghost.edible:
                self.bomb_until = 0
                self.maze.grid[y][x].is_bomb = True
                ghost.respawn(self.maze, self.player)

        if self.player.y == y and self.player.x == x:
            self.bomb_until = 0
            self.maze.grid[y][x].is_bomb = True
            self.player.respawn(self.maze)

    def extra_time(self) -> None:
        """Spawn the extra-time bonus and add 20 seconds when collected."""
        x, y = self.maze.time_pos
        if 20 >= self.get_time_left() and self.maze.time_pos == (None, None):
            self.maze.time_pos = self.maze.spawn_new_position()
            x, y = self.maze.time_pos
            self.maze.grid[y][x].extra_time = True

        if self.player.y == y and self.player.x == x:
            self.time_limit += 20
            self.maze.time_pos = (None, None)
            self.maze.grid[y][x].extra_time = False


class Create_Levels:
    """Create and manage all game levels."""

    def __init__(self, maze_width: int,
                 maze_height: int, levels_create: int) -> None:
        """Initialize the level creator and pre-build all game levels.

        Args:
            maze_width: Width of the maze in cells.
            maze_height: Height of the maze in cells.
            levels_create: Total number of levels to create.
        """
        self.lvl_id: int = 0
        self.maze_width: int = maze_width
        self.maze_height: int = maze_height
        self.levels_create: int = levels_create
        self.games: List[Game] = self._create_level_games(levels_create)

    def get_next_level(self) -> Game:
        """Return the next game level and advance the level counter."""
        next_game: Game = self.games[self.lvl_id]
        self.lvl_id += 1
        return next_game

    def is_complete_all_levels(self) -> bool:
        """Return True if all levels have been completed."""
        if self.lvl_id >= self.levels_create:
            return True
        return False

    def _create_level_games(self, levels: int) -> List[Game]:
        """
        Build and return a list of Game objects for all levels.

        Args:
            levels: Number of levels to create.

        Returns:
            A list of Game objects.
        """
        try:
            pacman: PacManFilesTools = PacManFilesTools()
            games: List = []
            counter: int = 0
            s_ghost: int = 3
            s_player: int = 3

            for lvl in range(1, levels + 1):
                data: Dict[str, Dict] = pacman.get_current_level_data()
                level = list(data.values())[0]

                maze: Maze = Maze(
                    self.maze_width, self.maze_height, seed=level["seed"])

                player: Player = Player(maze.get_center_maze(), level["lives"])

                eyess: List[Eyes] = []
                ghosts: List[Ghost] = [
                    Ghost(position)for position in
                    maze.get_super_pacgum_position_and_ghost()]

                num: int = 1
                for ghost in ghosts:
                    ghost.ghost_id = num
                    eyes = Eyes(ghost)
                    ghost.obj_eyes = eyes
                    eyess.append(eyes)
                    num += 1

                game: Game = Game(
                        maze,
                        player,
                        ghosts,
                        eyess,
                        time_limit=level["level_max_time"],
                        pacgum_score=level["points_per_pacgum"],
                        super_pacgum_score=level["points_per_super_pacgum"],
                        ghost_score=level["points_per_ghost"])

                game.player.player_speed = s_player
                counter = 0
                for gst, eyes in zip(game.ghosts, game.eyess):
                    gst.set_direction(game.maze, game.player)
                    gst.ghost_count = counter
                    gst.ghost_speed = s_ghost
                    gst.tmp_ghost_speed = s_ghost
                    eyes.counter = counter
                    eyes.speed = s_ghost
                    counter += 22

                s_ghost += 1
                s_player += 1

                game.level = lvl
                games.append(game)

        except Exception as e:
            raise ValueError(FileTools.error_raise_message(
                "Game_Logique.py", "Create_Levels", "_create_level_games", e))

        return games
