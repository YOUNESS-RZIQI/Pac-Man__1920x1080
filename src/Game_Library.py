"""Define maze, player, ghost, and cell game objects."""

from Files_Tools import FileTools
from typing import List, Tuple
from enum import Enum
import random
import time


class Cell:
    """
    Represent a single cell of the maze and its current game state.

    The cell stores its four walls and information about objects or
    entities currently present in it.
    """
    def __init__(
        self,
        up: bool = True,
        down: bool = True,
        left: bool = True,
        right: bool = True,

    ) -> None:
        """
        Initialize a maze cell with its walls and game objects state.

        Args:
            up: True if the upper wall is present.
            down: True if the lower wall is present.
            left: True if the left wall is present.
            right: True if the right wall is present.
        """
        self.up: bool = up
        self.down: bool = down
        self.left: bool = left
        self.right: bool = right
        self.bomb: bool = False
        self.ghost: bool = False
        self.is_42: bool = False
        self.player: bool = False
        self.magnet: bool = False
        self.pacgum: bool = False
        self.obj_ghost: List = []
        self.is_bomb: bool = False
        self.booster: bool = False
        self.add_live: bool = False
        self.extra_time: bool = False
        self.obj_eyes: List[Eyes] = []
        self.super_pacgum: bool = False


class Direction(Enum):
    """Represent the four possible movement directions."""

    UP = 1
    DOWN = 3
    LEFT = 4
    RIGHT = 2
    NONE = 0


class Maze:
    """Represent the game maze and its cell grid."""

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Initialize the maze and build its cell grid.

        Args:
            width: Number of cells horizontally.
            height: Number of cells vertically.
            seed: Random seed used for maze generation.
        """
        self.width: int = width
        self.height: int = height
        self.tunnel_b_pos: Tuple[int, int] = (7, 11)
        self.tunnel_a_pos: Tuple[int, int] = (5, 11)
        self.booster: Tuple[int | None, int | None] = (None, None)
        self.time_pos: Tuple[int | None, int | None] = (None, None)
        self.live_pos: Tuple[int | None, int | None] = (None, None)
        self.bomb_pos: Tuple[int | None, int | None] = (None, None)
        self.magnet_pos: Tuple[int | None, int | None] = (None, None)

        try:
            from mazegenerator import MazeGenerator  # type: ignore
            self._generator: MazeGenerator = MazeGenerator(
                size=(width, height),
                perfect=False,
                seed=seed
            )
        except Exception as e:
            raise ValueError(FileTools.error_raise_message(
                "Game_Library.py", "Maze", "__init__", e))

        self.grid: List[List[Cell]] = []
        self._build_cells()

    def _build_cells(self) -> None:
        """Build the grid of Cell objects from the maze generator output."""
        try:
            for y in range(self.height):
                row: List[Cell] = []

                for x in range(self.width):
                    value: int = self._generator.maze[y][x]

                    cell: Cell = Cell(
                        up=bool(value & 1),
                        right=bool(value & 2),
                        down=bool(value & 4),
                        left=bool(value & 8),
                    )

                    row.append(cell)

                    if (cell.up and cell.right and cell.down and cell.left):
                        cell.is_42 = True

                    if not cell.is_42:
                        cell.pacgum = True

                self.grid.append(row)

            super_pacgum_positions: List[Tuple[int, int]] = \
                self.get_super_pacgum_position_and_ghost()
            for x, y in super_pacgum_positions:
                self.grid[y][x].super_pacgum = True
                self.grid[y][x].pacgum = False

        except Exception as e:
            raise ValueError(FileTools.error_raise_message(
                "Game_Library.py", "Maze", "_build_cells", e))

    def can_move(self, x: int, y: int, direction: Direction) -> bool:
        """
        Check if the player can move from the given position.

        Args:
            x: X coordinate of the current position.
            y: Y coordinate of the current position.
            direction: Direction of the movement.

        Returns:
            True if the movement is possible, otherwise False.
        """
        if not (0 <= y < self.height and 0 <= x < self.width):
            return False

        cell: Cell = self.grid[y][x]

        if direction == Direction.UP:
            return not cell.up

        if direction == Direction.RIGHT:
            return not cell.right

        if direction == Direction.DOWN:
            return not cell.down

        if direction == Direction.LEFT:
            return not cell.left

        return False

    def get_center_maze(self) -> Tuple[int, int]:
        """Return the coordinates of the center cell of the maze."""
        x, y = self.width // 2, self.height // 2
        centre: Cell = self.grid[y][x]

        if centre.right and centre.up and centre.down and centre.left:
            return (self.width - 1) // 2, self.height // 2
        return x, y

    def get_super_pacgum_position_and_ghost(self) -> List[Tuple[int, int]]:
        """Return the four corner positions for super pac-gums."""
        return [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]

    def spawn_new_position(self) -> Tuple[int, int]:
        """Return a random valid position to spawn a new item."""
        positions: List[Tuple[int, int]] = []

        for y in range(self.height):
            for x in range(self.width):
                cell: Cell = self.grid[y][x]

                if (not cell.is_42 and not cell.super_pacgum
                    and not cell.extra_time and not cell.magnet
                    and not cell.add_live and not cell.booster
                    and (y, x) not in (
                        self.tunnel_a_pos, self.tunnel_b_pos)):

                    positions.append((x, y))

        return random.choice(positions)


class Player:
    """Represent the player and its current game state."""

    def __init__(self, position: Tuple[int, int], lives: int) -> None:
        """
        Initialize the player at the given position with a set number of lives.

        Args:
            position: Starting (x, y) coordinates of the player.
            lives: Number of lives the player starts with.
        """
        self.x: int = position[0]
        self.y: int = position[1]

        self.score: int = 0
        self.lives: int = lives
        self.magnet: bool = False
        self.player_speed: int = 0
        self.player_count: int = 0
        self.in_tunnel: bool = False
        self.invincible: bool = False
        self.is_counting: bool = False
        self.magnet_until: float = 0.0
        self.booster_until: float = 0.0
        self.direction: Direction = Direction.NONE

    def move(self, maze: Maze, direction: Direction) -> None:
        """
        Move the player one cell in the given direction if possible.

        Args:
            maze: Maze in which the player moves.
            direction: Direction in which the player should move.
        """
        if maze.can_move(self.x, self.y, direction):
            old_cell: Cell = maze.grid[self.y][self.x]
            if direction == Direction.UP:
                self.y -= 1
            elif direction == Direction.RIGHT:
                self.x += 1
            elif direction == Direction.DOWN:
                self.y += 1
            elif direction == Direction.LEFT:
                self.x -= 1
            new_cell: Cell = maze.grid[self.y][self.x]
            old_cell.player = False
            new_cell.player = True

    def respawn(self, maze: Maze) -> None:
        """
        Respawn the player at the center of the maze.

        Args:
            maze: Maze in which the player is respawned.
        """
        maze.grid[self.y][self.x].player = False
        self.x, self.y = maze.get_center_maze()
        maze.grid[self.y][self.x].player = True

    def is_dead(self) -> bool:
        """Return True if the player has no lives remaining."""
        return self.lives <= 0


class Ghost:
    """Represent a ghost enemy and its movement behavior."""

    def __init__(self, position: Tuple[int, int]) -> None:
        """Initialize the ghost at the given position.

        Args:
            position: Starting (x, y) coordinates of the ghost.
        """
        self.x = position[0]
        self.y = position[1]

        self.ghost_id: int = 0
        self.edible: bool = False
        self.ghost_speed: int = 0
        self.ghost_count: int = 0
        self.respawn_at: float = 0.0
        self.tmp_ghost_speed: int = 0
        self.edible_until: float = 0.0
        self.obj_eyes: Eyes | None = None
        self.spawn: Tuple[int, int] = position
        self.direction: Direction = Direction.NONE

    def reverse_direction(self, direction: Direction) -> Direction:
        """
        Return the opposite of the given direction.

        Args:
            direction: Direction to reverse.

        Returns:
            The opposite direction.
        """
        if direction == Direction.UP:
            return Direction.DOWN
        elif direction == Direction.DOWN:
            return Direction.UP
        elif direction == Direction.RIGHT:
            return Direction.LEFT
        else:
            return Direction.RIGHT

    def clear_path(self, maze: Maze, player: Player) -> bool:
        """
        Return True if there is an unobstructed straight line to the player.

        Args:
            maze: Maze used to check for obstacles.
            player: Player whose position is checked.

        Returns:
            True if the path to the player is clear, otherwise False.
        """
        if self.x == player.x:
            step: int = 1 if self.y < player.y else -1

            for y in range(self.y, player.y, step):
                if maze.grid[y][self.x].down if step == 1 \
                        else maze.grid[y][self.x].up:
                    return False

        elif self.y == player.y:
            step = 1 if self.x < player.x else -1
            for x in range(self.x, player.x, step):
                if maze.grid[self.y][x].right if step == 1 \
                        else maze.grid[self.y][x].left:
                    return False

        else:
            return False
        return True

    def set_direction(self, maze: Maze, player: Player) -> None:
        """
        Choose and set the ghost's next movement direction.

        Args:
            maze: Maze used to determine the available paths.
            player: Player whose position is targeted.
        """

        def where_is_player() -> Direction:
            """Return the direction toward the player."""
            if dx > 0:
                return Direction.RIGHT
            if dx < 0:
                return Direction.LEFT
            if dy > 0:
                return Direction.DOWN
            if dy < 0:
                return Direction.UP
            return self.direction

        directions: list[Direction] = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT
        ]

        dx: int = player.x - self.x
        dy: int = player.y - self.y

        possible: List[Direction] = [
            direction for direction in directions
            if maze.can_move(self.x, self.y, direction)
        ]

        player_in_direction: Direction = where_is_player()

        if not self.edible and self.clear_path(maze, player):
            if player_in_direction in possible:
                self.direction = player_in_direction
                return

        elif self.edible and self.clear_path(maze, player):
            away_direction: Direction = \
                self.reverse_direction(player_in_direction)

            if away_direction in possible:
                self.direction = away_direction
                return

        reverse: Direction = self.reverse_direction(self.direction)
        if self.clear_path(maze, player):
            reverse = player_in_direction

        if reverse in possible and len(possible) > 1:
            possible.remove(reverse)

        self.direction = random.choice(possible)

    def move(self, maze: Maze, player: Player) -> None:
        """
        Move the ghost one cell in it current direction and update it position.

        If the current direction is blocked, choose a new valid direction.
        Update the previous and new maze cells with the ghost's current state.

        Args:
            maze: Maze in which the ghost moves.
            player: Player used to determine the ghost's next direction.
        """
        if not maze.can_move(self.x, self.y, self.direction):
            self.set_direction(maze, player)

        old_cell: Cell = maze.grid[self.y][self.x]

        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1

        new_cell: Cell = maze.grid[self.y][self.x]

        if self in old_cell.obj_ghost:
            old_cell.obj_ghost.remove(self)
        old_cell.ghost = len(old_cell.obj_ghost) > 0

        new_cell.obj_ghost.append(self)
        new_cell.ghost = True

        self.set_direction(maze, player)

    def set_edible(self, duration: float = 15.0) -> None:
        """Make the ghost edible for the given duration in seconds."""
        self.edible = True
        self.edible_until = time.time() + duration

    def respawn(self, maze: Maze, player: Player) -> None:
        """
        Respawn the ghost at its starting position and reset its state.

        Remove the ghost from its current cell, restore its spawn position,
        reset its edible and ghost count states, and update its direction.

        Args:
            maze: Maze in which the ghost is respawned.
            player: Player used to determine the ghost's direction.
        """
        old_cell: Cell = maze.grid[self.y][self.x]

        if self in old_cell.obj_ghost:
            old_cell.obj_ghost.remove(self)
        old_cell.ghost = len(old_cell.obj_ghost) > 0

        self.x, self.y = self.spawn
        self.edible = False
        self.ghost_count = 0

        if not self.respawn_at:
            new_cell: Cell = maze.grid[self.y][self.x]
            new_cell.obj_ghost.append(self)
            new_cell.ghost = True

        self.set_direction(maze, player)

    def check_edible_time(self) -> None:
        """Deactivate edible state if its duration has expired."""
        if self.edible and time.time() >= self.edible_until:
            self.edible = False

    def handle_ghost_respawn(self, maze: Maze, player: Player) -> bool:
        """
        Respawn the ghost if its respawn timer has elapsed.

        Args:
            maze: Maze used to determine the respawn position.

        Returns:
            True if the ghost is waiting to respawn, otherwise False.
        """
        assert self.obj_eyes is not None

        if self.respawn_at:
            if time.time() >= self.respawn_at and not self.obj_eyes.path:
                self.respawn_at = 0.0
                self.respawn(maze, player)
            return True

        return False

    def Did_you_see_the_player(self, maze: Maze, player: Player) -> bool:
        """
        Return True if the ghost can see the player three cells ahead.

        Args:
            maze: Maze used to check the path to the player.
            player: Player whose position is checked.

        Returns:
           True if the player is three cells ahead with two cells between them.
        """
        direction: Direction = self.direction

        def check(x: int, y: int) -> bool:
            """
            Check if the player is three cells ahead in the given direction.

            Args:
                x: Horizontal movement offset.
                y: Vertical movement offset.

            Returns:
                True if the player is three cells ahead without walls.
            """
            if not maze.can_move(self.x, self.y, direction):
                return False

            if not maze.can_move(self.x + x, self.y + y, direction):
                return False

            if not maze.can_move(self.x + x + x, self.y + y + y, direction):
                return False

            return (self.y + y + y + y,
                    self.x + x + x + x) == (player.y, player.x)

        if direction == Direction.UP:
            return check(0, -1)

        if direction == Direction.RIGHT:
            return check(1, 0)

        if direction == Direction.DOWN:
            return check(0, 1)

        if direction == Direction.LEFT:
            return check(-1, 0)

        return False


class Eyes():
    """
    Eyes of a ghost that has been eaten.

    Holds the state needed to move and draw the eyes on the maze, such as
    their position, speed, direction and the ghost they belong to.

    Attributes:
        ghost (Ghost): The ghost these eyes belong to.
    """

    def __init__(self, ghost: Ghost) -> None:
        """Initialize the eyes for a given ghost.

        Args:
            ghost (Ghost): The ghost these eyes belong to. Its ``ghost_id``
                is used as the id of the eyes.
        """
        self.y: int = 0
        self.x: int = 0
        self.speed: int = 4
        self.counter: int = 0
        self.ghost: Ghost = ghost
        self.path: str | None = None
        self.id: int = ghost.ghost_id
        self.direction:  Direction | None = None

    def put_eyes(self, maze: Maze) -> None:
        """
        Calculate and store the shortest path for the ghost's eyes animation.

        Args:
            maze: Maze used to calculate the shortest path.
        """
        try:
            from mazegenerator import MazeGenerator  # type: ignore
            gen: MazeGenerator = maze._generator

            gen._entryx = self.ghost.x
            gen._entryy = self.ghost.y
            gen._exitx = self.ghost.spawn[0]
            gen._exity = self.ghost.spawn[1]

            gen._find_short_path()
            self.path = gen._shortest_path

            self.x = self.ghost.x
            self.y = self.ghost.y
        except Exception as e:
            raise ValueError(FileTools.error_raise_message(
                "Game_Library.py", "Eyes", "put_eyes", e))

    def move_eyes(self, maze: Maze) -> None:
        """
        Move the ghost's eyes one step toward the spawn position.

        Args:
            maze: Maze used to determine the next step.
        """
        if not self.path:
            if self in maze.grid[self.y][self.x].obj_eyes:
                maze.grid[self.y][self.x].obj_eyes.remove(self)
            self.path = None
            return

        direction: str = self.path[0]
        if self in maze.grid[self.y][self.x].obj_eyes:
            maze.grid[self.y][self.x].obj_eyes.remove(self)

        if direction == "N":
            self.y -= 1
        elif direction == "E":
            self.x += 1
        elif direction == "S":
            self.y += 1
        elif direction == "W":
            self.x -= 1

        if len(self.path) > 1:
            maze.grid[self.y][self.x].obj_eyes.append(self)
        self.path = self.path[1:]

        if self.path:
            direction = self.path[0]

            if direction == "N":
                self.direction = Direction.UP
            elif direction == "E":
                self.direction = Direction.RIGHT
            elif direction == "S":
                self.direction = Direction.DOWN
            elif direction == "W":
                self.direction = Direction.LEFT
        else:
            self.direction = None
