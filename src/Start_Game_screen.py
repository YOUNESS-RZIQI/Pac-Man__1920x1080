"""Provide the Start Game screen of the game."""

import os
from typing import Any, Tuple, Dict, List
from mlx import Mlx
from Enter_Score_Name_Screen import EnterScoreNameScreen
import random
from Files_Tools import FileTools, Keys, Character, PacManFilesTools
from Game_Library import Direction, Ghost
from Game_Logique import Create_Levels, Game
import time
from Sounds_Effects import Sounds


class X_Y_Tools:
    """Provide methods to work with mouse coordinates and buttons."""

    @staticmethod
    def is_x_in_range_xx_and_y_in_range_yy(
        x: int, y: int, xx: Tuple[int, int], yy: Tuple[int, int]
    ) -> bool:
        """Check whether a point is inside a rectangular area.

        Args:
            x: The x position of the point.
            y: The y position of the point.
            xx: The (min, max) x range, inclusive.
            yy: The (min, max) y range, inclusive.

        Returns:
            True if the point is inside both ranges, False otherwise.
        """

        return (xx[0] <= x <= xx[1]) and (yy[0] <= y <= yy[1])

    @staticmethod
    def is_click_in_button(
        x: int, y: int, xx: Tuple[int, int], yy: Tuple[int, int]
    ) -> bool:
        """Check whether a click is inside a button.

        Args:
            x: The x position of the click.
            y: The y position of the click.
            xx: The (min, max) x range of the button, inclusive.
            yy: The (min, max) y range of the button, inclusive.

        Returns:
            True if the click is inside the button, False otherwise.
        """

        return X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(x, y, xx, yy)


class StartGameScreen:
    """Provide the methods that build the game play screen."""

    def __init__(self, LEVELS: int) -> None:
        """Initialize the screen with the needed data.

        Args:
            LEVELS: The number of levels to create.

        Raises:
            ValueError: If mlx_init() or mlx_new_window() fails, or if an
                image cannot be loaded.
        """

        self.mlx_obj: Mlx = Mlx()

        self.init_ptr: Any = self.mlx_obj.mlx_init()
        if not self.init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Start_Game_screen.py",
                    "StartGameScreen",
                    "__init__()",
                    "mlx_init() failed",
                )
            )

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (1920, 1080)
        FileTools.check_pc_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.win_ptr: Any = self.mlx_obj.mlx_new_window(
            self.init_ptr, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Pac-Man"
        )
        if not self.win_ptr:
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Start_Game_screen.py",
                    "StartGameScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.CELL_SIZE: int = 45
        self.MAZE_ROWS, self.MAZE_COLMS = 13, 19
        self.X_MAZE_ON_SCREEN, self.Y_MAZE_ON_SCREEN = (550, 215)

        self.is_shaking: bool = False

        self.shake_counter: int = 0
        self.x_shaking_offset: int = 0
        self.y_shaking_offset: int = 0

        self.base_path: str = PacManFilesTools.get_base_path_for_images()
        start_game_path: str = self.base_path + "Start_Game" + os.sep

        self.back_ground1, _, _ = self.mlx_obj.mlx_png_file_to_image(
            self.init_ptr, start_game_path + "back_ground1.png")
        if not self.back_ground1:
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Start_Game_screen.py",
                    "StartGameScreen",
                    "__init__()",
                    "back_ground1.png failed to create",
                )
            )
        self.mlx_obj.mlx_put_image_to_window(self.init_ptr, self.win_ptr,
                                             self.back_ground1, 0, 0)

        self.black_wall_cover, _, _ = self.mlx_obj.mlx_png_file_to_image(
            self.init_ptr, start_game_path + "black_wall_cover.png")
        if not self.black_wall_cover:
            self.mlx_obj.mlx_destroy_image(self.init_ptr, self.back_ground1)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Start_Game_screen.py",
                    "StartGameScreen",
                    "__init__()",
                    "black_wall_cover.png failed to create",
                )
            )
        self.mlx_obj.mlx_put_image_to_window(self.init_ptr, self.win_ptr,
                                             self.black_wall_cover,
                                             self.X_MAZE_ON_SCREEN +
                                             self.x_shaking_offset - 22,
                                             self.Y_MAZE_ON_SCREEN +
                                             self.y_shaking_offset - 25,)
        self.mlx_obj.mlx_do_sync(self.init_ptr)

        self.images: Dict[str, Any] = {}
        self.images = self._load_all_imgs()
        self.images["back_ground1"] = self.back_ground1
        self.images["black_wall_cover"] = self.black_wall_cover

        self.levels_obj: Create_Levels = Create_Levels(
                self.MAZE_COLMS, self.MAZE_ROWS, levels_create=LEVELS
            )
        self.current_game: Game = self.levels_obj.get_next_level()

        self.plr_counter_mc_mo: int = 0
        self.old_pacman_imag: str = "pac_man_du_mo"
        self.plr_next_direction: Direction = Direction.NONE

        self.player_motion_offset: int = 0
        self.old_pac_man_pos: Tuple[int, int] = (-10, -10)

        self.ghost_1_motion_offset: int = 0
        self.old_ghost_1_pos: Tuple[int, int] = (-10, -10)
        self.ghost_2_motion_offset: int = 0
        self.old_ghost_2_pos: Tuple[int, int] = (-10, -10)
        self.ghost_3_motion_offset: int = 0
        self.old_ghost_3_pos: Tuple[int, int] = (-10, -10)
        self.ghost_4_motion_offset: int = 0
        self.old_ghost_4_pos: Tuple[int, int] = (-10, -10)

        self.eye_1_motion_offset: int = 0
        self.old_eye_1_pos: Tuple[int, int] = (-10, -10)
        self.eye_2_motion_offset: int = 0
        self.old_eye_2_pos: Tuple[int, int] = (-10, -10)
        self.eye_3_motion_offset: int = 0
        self.old_eye_3_pos: Tuple[int, int] = (-10, -10)
        self.eye_4_motion_offset: int = 0
        self.old_eye_4_pos: Tuple[int, int] = (-10, -10)

        self.increase_player_spd_x_x: Tuple[int, int] = (355, 400)
        self.increase_player_spd_y_y: Tuple[int, int] = (863, 904)
        self.decrease_player_spd_x_x: Tuple[int, int] = (539, 579)
        self.decrease_player_spd_y_y: Tuple[int, int] = (863, 904)

        self.increase_ghost_spd_x_x: Tuple[int, int] = (338, 380)
        self.increase_ghost_spd_y_y: Tuple[int, int] = (942, 986)
        self.decrease_ghost_spd_x_x: Tuple[int, int] = (515, 566)
        self.decrease_ghost_spd_y_y: Tuple[int, int] = (942, 986)

        self.go_to_next_level_x_x: Tuple[int, int] = (833, 1161)
        self.go_to_next_level_y_y: Tuple[int, int] = (884, 931)

        self.ghost_freeze_x_x: Tuple[int, int] = (874, 1143)
        self.ghost_freeze_y_y: Tuple[int, int] = (952, 995)

        self.extra_live_x_x: Tuple[int, int] = (1510, 1750)
        self.extra_live_y_y: Tuple[int, int] = (870, 913)

        self.unedible_player_x_x: Tuple[int, int] = (1499, 1804)
        self.unedible_player_y_y: Tuple[int, int] = (947, 1000)

        self.pause_game_x_x: Tuple[int, int] = (910, 950)
        self.pause_game_y_y: Tuple[int, int] = (841, 878)

        self.pause_menu_x_x: Tuple[int, int] = (958, 995)
        self.pause_menu_y_y: Tuple[int, int] = (841, 878)

        self.cheat_mode_x_x: Tuple[int, int] = (1005, 1042)
        self.cheat_mode_y_y: Tuple[int, int] = (841, 878)

        self.exit_x_x: Tuple[int, int] = (575, 961)
        self.exit_y_y: Tuple[int, int] = (429, 605)

        self.resume_x_x: Tuple[int, int] = (991, 1374)
        self.resume_y_y: Tuple[int, int] = (429, 605)

        self.is_exit: bool = False
        self.pause_game: bool = False
        self.is_cheat_mode: bool = False
        self.is_pause_menu: bool = False
        self.is_new_level_start: bool = False
        self.show_win_game_screen: bool = False
        self.show_game_over_screen: bool = False
        self.error_in_func_on_each_level: bool = False

        self.time_befor_pause: int = 0
        self.old_level_num: int = -1
        self.current_level_num: int = 0

    def _load_all_imgs(self) -> Dict[str, Any]:
        """Load all the images that this screen depends on.

        self.current_level_num: int = 0
        Returns:
            A dictionary mapping each image name to its pointer.

        Raises:
            ValueError: If one of the XPM files cannot be loaded.
        """

        play_path: str = self.base_path + "Start_Game" + os.sep
        digits_path: str = self.base_path + "Digits" + os.sep
        alphas_path: str = self.base_path + "Alpha" + os.sep
        special_chars_path: str = self.base_path + "Special_chars" + os.sep

        img_files: Dict[str, str] = {
            "up": "Up.png",
            "left": "Left.png",
            "down": "Down.png",
            "pause": "pause.png",
            "right": "Right.png",
            "tunnel": "tunnel.png",
            "resume": "resume.png",
            "pacgum": "pac_gum.png",
            "bomb_1": "bomb_on.png",
            "bomb_2": "bomb_off.png",
            "eyes1_1": "eyes1_1.png",
            "eyes1_2": "eyes1_2.png",
            "eyes2_1": "eyes2_1.png",
            "eyes2_2": "eyes2_2.png",
            "eyes3_1": "eyes3_1.png",
            "eyes3_2": "eyes3_2.png",
            "eyes4_1": "eyes4_1.png",
            "eyes4_2": "eyes4_2.png",
            "heart_1": "heart_1.png",
            "heart_2": "heart_2.png",
            "ghost1_1": "ghost1_1.png",
            "ghost1_2": "ghost1_2.png",
            "ghost2_1": "ghost2_1.png",
            "ghost2_2": "ghost2_2.png",
            "ghost3_1": "ghost3_1.png",
            "ghost3_2": "ghost3_2.png",
            "ghost4_1": "ghost4_1.png",
            "ghost4_2": "ghost4_2.png",
            "ghost_42": "ghost_42.png",
            "rocket_2": "rocket_2.png",
            "rocket_1": "rocket_1.png",
            "magnet_1": "magnet_1.png",
            "magnet_2": "magnet_2.png",
            "red_circle": "red_circle.png",
            "hand_cursor": "hand_cursor.png",
            "extra_time_1": "extra_time_1.png",
            "extra_time_2": "extra_time_2.png",
            "back_ground2": "back_ground2.png",
            "super_pacgum": "super_pacgum.png",
            "green_circle": "green_circle.png",
            "pac_man_dr_mo": "pac_man_dr_mo.png",
            "pac_man_dr_mc": "pac_man_dr_mc.png",
            "pac_man_dl_mo": "pac_man_dl_mo.png",
            "pac_man_dl_mc": "pac_man_dl_mc.png",
            "pac_man_du_mo": "pac_man_du_mo.png",
            "pac_man_du_mc": "pac_man_du_mc.png",
            "pac_man_dd_mo": "pac_man_dd_mo.png",
            "pac_man_dd_mc": "pac_man_dd_mc.png",
            "cheat_mode_on": "cheat_mode_on.png",
            "pause_menu_bg": "pause_menu_bg.png",
            "pause_menu_b_on": "pause_menu_on.png",
            "edibl_ghost_1": "edibl_ghost_1.png",
            "edibl_ghost_2": "edibl_ghost_2.png",
            "pause_menu_b_off": "pause_menu_off.png",
            "cheat_mode_b_off": "cheat_mode_off.png",
            "edibl_ghost_v2_1": "edibl_ghost_v2_1.png",
            "edibl_ghost_v2_2": "edibl_ghost_v2_2.png",
        }

        images_n_p: Dict[str, Any] = {}

        for name, filename in img_files.items():
            if name in ["red_circle", "green_circle", "pause", "resume",
                        "hand_cursor", "pause_menu_b_on", "pause_menu_b_off",
                        "cheat_mode_b_off", "cheat_mode_on"]:
                path: str = special_chars_path + filename
            else:
                path = play_path + filename

            img_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
                                                        self.init_ptr, path)

            if not img_ptr:
                for destroy_ptr1 in images_n_p.values():
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr1)
                for destroy_ptr2 in [self.back_ground1, self.black_wall_cover]:
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr2)
                self.mlx_obj.mlx_release(self.init_ptr)
                raise ValueError(
                    FileTools.error_raise_message(
                        "Start_Game_screen.py",
                        "StartGameScreen",
                        "_load_all_imgs()",
                        f"{filename} not found",
                    )
                )

            images_n_p[name] = img_ptr

        for (
            char
        ) in (
            "QWERTYUIOPASDFGHJKLZXCVBNM0123456789qwertyuiopasdfghjklzxcvbnm+-:"
        ):

            if char.isalpha():
                if char.isupper():
                    path = alphas_path + char + "_upper.png"
                else:
                    path = alphas_path + char + "_lower.png"
            elif char.isdigit():
                path = digits_path + char + ".png"
            else:
                path = special_chars_path + char + ".png"

            char_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
                self.init_ptr, path
            )

            if not char_ptr:
                for destroy_ptr1 in images_n_p.values():
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr1)
                for destroy_ptr2 in [self.back_ground1, self.black_wall_cover]:
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr2)
                self.mlx_obj.mlx_release(self.init_ptr)
                raise ValueError(
                    FileTools.error_raise_message(
                        "Start_Game_screen.py",
                        "StartGameScreen",
                        "_load_all_imgs()",
                        f"{char}.png not found",
                    )
                )

            images_n_p[char] = char_ptr

        return images_n_p

    def _put_image_in_maze_place(self, x: int, y: int, name: str
                                 ) -> None:
        """Put an image at a position relative to the maze.

        Args:
            x: The x position inside the maze.
            y: The y position inside the maze.
            name: The name of the image to put.
        """

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr,
            self.win_ptr,
            self.images[name],
            x + self.X_MAZE_ON_SCREEN + self.x_shaking_offset,
            y + self.Y_MAZE_ON_SCREEN + self.y_shaking_offset,
        )

    def _put_word_in_place(self, x: int, y: int, word: str) -> None:
        """Put the characters of a word at a specific position on screen.

        Args:
            x: The starting x position.
            y: The starting y position.
            word: The word to put on the screen.
        """

        for c in word:
            if c == " ":
                x += 20
                continue

            self.mlx_obj.mlx_put_image_to_window(
                self.init_ptr, self.win_ptr, self.images[c], x, y
            )
            x += 20

    def _put_time_lives_levels_score_on_screen(self) -> None:
        """Put the time, lives, level and score on the screen."""

        self._put_word_in_place(65, 137, "Time")
        if not self.pause_game:
            self._put_word_in_place(
                88, 183, self._fix_len(str(self.current_game.get_time_left()),
                                       20))
        else:
            self._put_word_in_place(
                88, 183, str(self.time_befor_pause))

        self._put_word_in_place(1722, 137, "Lives")
        self._put_word_in_place(
            1753, 183, self._fix_len(str(self.current_game.player.lives), 5)
        )

        self._put_word_in_place(40, 675, "Score")
        self._put_word_in_place(
            50, 725, self._fix_len(str(self.current_game.player.score), 19)
        )

        self._put_word_in_place(1740, 665, "Level")
        self._put_word_in_place(1775, 730, str(self.current_game.level))

    def _put_game_buttons_in_place(self) -> None:
        """Put the game information and the cheat buttons on the screen."""

        self._put_time_lives_levels_score_on_screen()

        if self.is_cheat_mode:
            self._put_word_in_place(58, 874, "Player Speed:  +   OR   -")
            self._put_word_in_place(58, 955, "Ghost Speed:  +   OR   -")
#
            self._put_word_in_place(830, 889, "Go To Next Level")
            self._put_word_in_place(880, 955, "Ghost Freeze")
            self._put_word_in_place(1510, 874, "Extra lives")

            if not self.current_game.player.invincible:
                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["green_circle"],
                    1495,
                    955,
                )
            else:
                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["red_circle"],
                    1495,
                    955,
                )
            self._put_word_in_place(1525, 955, "Edible Player")

        pause_img: str = (
            "resume" if self.pause_game else "pause")

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.images[pause_img],
            910, 835
        )

        pause_menu_img: str = (
            "pause_menu_b_off" if self.is_pause_menu else "pause_menu_b_on"
        )
        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.images[pause_menu_img],
            955, 835
        )

        cheat_mode_img: str = (
            "cheat_mode_on" if self.is_cheat_mode else "cheat_mode_b_off")
        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.images[cheat_mode_img],
            1000, 835
        )

    def _go_to_next_level(self) -> None:
        """Move to the next level, or exit the loop if all are completed."""

        self.current_game.sounds_obj.stop_all()
        if self.levels_obj.is_complete_all_levels():
            self.mlx_obj.mlx_loop_exit(self.init_ptr)
            self.show_win_game_screen = True
            return

        self.current_level_num += 1
        self.ghost_1_motion_offset = 0
        self.ghost_2_motion_offset = 0
        self.ghost_3_motion_offset = 0
        self.ghost_4_motion_offset = 0

        next_game: Game = self.levels_obj.get_next_level()
        self.current_game.transfer_player_state(next_game)
        self.current_game = next_game
        self.plr_next_direction = Direction.NONE

    def _fix_len(self, score: str, max_len: int) -> str:
        """Truncate a text so it fits on the screen.

        Args:
            score: The text to truncate.
            max_len: The maximum length allowed.

        Returns:
            The text limited to max_len characters.
        """

        if len(score) > max_len:
            new_score: str = score[:max_len]
            return new_score
        else:
            return score

    def _put_back_grounds(self) -> None:
        """Put the background images on the screen."""

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr,
            self.images[f"back_ground{random.choice([1, 2])}"], 0, 0
        )
        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr,
            self.win_ptr,
            self.images["black_wall_cover"],
            self.X_MAZE_ON_SCREEN + self.x_shaking_offset - 22,
            self.Y_MAZE_ON_SCREEN + self.y_shaking_offset - 25,
        )

    def _on_each_level(self) -> None:
        """Prepare for a new level.

        Resets the timer and synchronization.
        """

        if self.old_level_num != self.current_level_num:
            self.old_level_num = self.current_level_num
            self.is_new_level_start = True

            self.current_game.start_game_timer()

    def _put_pac_man_img_in_maze(self, x: int, y: int) -> None:
        """Put the Pac-Man image, facing its direction, in the maze.

        The mouth is open during the first part of the movement between two
        cells and closed during the rest, depending on the motion offset.

        Args:
            x: The x position inside the maze.
            y: The y position inside the maze.
        """

        direction: Direction = self.current_game.player.direction

        if direction == Direction.UP:
            self.old_pacman_imag = "pac_man_du_mo"
        elif direction == Direction.DOWN:
            self.old_pacman_imag = "pac_man_dd_mo"
        elif direction == Direction.LEFT:
            self.old_pacman_imag = "pac_man_dl_mo"
        elif direction == Direction.RIGHT:
            self.old_pacman_imag = "pac_man_dr_mo"

        mouth: str = "mo" if self.player_motion_offset < 22 else "mc"
        self._put_image_in_maze_place(
            x, y, self.old_pacman_imag[:-2] + mouth)

    def _movement_animation(self, mx: int, my: int, character: int,
                            speed: Any, eye: Any = None) -> Tuple[int, int]:
        """Compute the animated position of a character between two cells.

        Args:
            mx: The x position of the cell.
            my: The y position of the cell.
            character: The character id (Pac-Man, a ghost or an eye).
            speed: The movement speed of the character.
            eye: eye object when moving an eye, otherwise None.

        Returns:
            The (x, y) position where the character must be drawn.
        """

        motion_my: int = my
        motion_mx: int = mx
        sound_obj: Sounds = self.current_game.sounds_obj

        if character == Character.PAC_MAN:
            direction: Direction = \
                self.current_game.player.direction
        elif character == Character.GHOST_1:
            direction = self.current_game.ghosts[0].direction
        elif character == Character.GHOST_2:
            direction = self.current_game.ghosts[1].direction
        elif character == Character.GHOST_3:
            direction = self.current_game.ghosts[2].direction
        elif character == Character.GHOST_4:
            direction = self.current_game.ghosts[3].direction
        else:
            direction = eye.direction

        if character == Character.PAC_MAN and self.current_game.maze.can_move(
            mx // self.CELL_SIZE, my // self.CELL_SIZE, direction
        ):

            if self.old_pac_man_pos != (mx, my):
                self.player_motion_offset = 0
                self.old_pac_man_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.player_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.player_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.player_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.player_motion_offset

            if self.player_motion_offset < self.CELL_SIZE - 1:
                if self.player_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.player_motion_offset = self.CELL_SIZE - 1
                else:
                    self.player_motion_offset += speed

        elif (character == Character.GHOST_1
              and not self.current_game.ghost_freeze and not
                sound_obj._is_playing(sound_obj.start_sound)):

            if (
                self.old_ghost_1_pos != (mx, my)
            ):
                self.ghost_1_motion_offset = 0
                self.old_ghost_1_pos = (mx, my)
            if direction == Direction.UP:
                motion_my = my - self.ghost_1_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.ghost_1_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.ghost_1_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.ghost_1_motion_offset

            if self.ghost_1_motion_offset < self.CELL_SIZE - 1:
                if self.ghost_1_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.ghost_1_motion_offset = self.CELL_SIZE - 1
                else:
                    self.ghost_1_motion_offset += speed

        elif (
            character == Character.GHOST_2
            and not self.current_game.ghost_freeze and not
                sound_obj._is_playing(sound_obj.start_sound)
        ):

            if (
                self.old_ghost_2_pos != (mx, my)
            ):
                self.ghost_2_motion_offset = 0
                self.old_ghost_2_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.ghost_2_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.ghost_2_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.ghost_2_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.ghost_2_motion_offset

            if self.ghost_2_motion_offset < self.CELL_SIZE - 1:
                if self.ghost_2_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.ghost_2_motion_offset = self.CELL_SIZE - 1
                else:
                    self.ghost_2_motion_offset += speed

        elif (
            character == Character.GHOST_3
            and not self.current_game.ghost_freeze and not
                sound_obj._is_playing(sound_obj.start_sound)
        ):

            if self.old_ghost_3_pos != (mx, my):
                self.ghost_3_motion_offset = 0
                self.old_ghost_3_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.ghost_3_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.ghost_3_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.ghost_3_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.ghost_3_motion_offset

            if self.ghost_3_motion_offset < self.CELL_SIZE - 1:
                if self.ghost_3_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.ghost_3_motion_offset = self.CELL_SIZE - 1
                else:
                    self.ghost_3_motion_offset += speed

        elif (
            character == Character.GHOST_4
            and not self.current_game.ghost_freeze and not
                sound_obj._is_playing(sound_obj.start_sound)
        ):

            if self.old_ghost_4_pos != (mx, my):
                self.ghost_4_motion_offset = 0
                self.old_ghost_4_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.ghost_4_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.ghost_4_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.ghost_4_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.ghost_4_motion_offset

            if self.ghost_4_motion_offset < self.CELL_SIZE - 1:
                if self.ghost_4_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.ghost_4_motion_offset = self.CELL_SIZE - 1
                else:
                    self.ghost_4_motion_offset += speed

        elif character == Character.EYE_1:

            if self.old_eye_1_pos != (mx, my):
                self.eye_1_motion_offset = 0
                self.old_eye_1_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.eye_1_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.eye_1_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.eye_1_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.eye_1_motion_offset

            if self.eye_1_motion_offset < self.CELL_SIZE - 1:
                if self.eye_1_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.eye_1_motion_offset = self.CELL_SIZE - 1
                else:
                    self.eye_1_motion_offset += speed

        elif character == Character.EYE_2:

            if self.old_eye_2_pos != (mx, my):
                self.eye_2_motion_offset = 0
                self.old_eye_2_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.eye_2_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.eye_2_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.eye_2_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.eye_2_motion_offset

            if self.eye_2_motion_offset < self.CELL_SIZE - 1:
                if self.eye_2_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.eye_2_motion_offset = self.CELL_SIZE - 1
                else:
                    self.eye_2_motion_offset += speed

        elif character == Character.EYE_3:
            if self.old_eye_3_pos != (mx, my):
                self.eye_3_motion_offset = 0
                self.old_eye_3_pos = (mx, my)

            if direction == Direction.UP:
                motion_my = my - self.eye_3_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.eye_3_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.eye_3_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.eye_3_motion_offset

            if self.eye_3_motion_offset < self.CELL_SIZE - 1:
                if self.eye_3_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.eye_3_motion_offset = self.CELL_SIZE - 1
                else:
                    self.eye_3_motion_offset += speed

        elif character == Character.EYE_4:

            if self.old_eye_4_pos != (mx, my):
                self.eye_4_motion_offset = 0
                self.old_eye_4_pos = (mx, my)
            if direction == Direction.UP:
                motion_my = my - self.eye_4_motion_offset
            elif direction == Direction.DOWN:
                motion_my = my + self.eye_4_motion_offset
            elif direction == Direction.LEFT:
                motion_mx = mx - self.eye_4_motion_offset
            elif direction == Direction.RIGHT:
                motion_mx = mx + self.eye_4_motion_offset

            if self.eye_4_motion_offset < self.CELL_SIZE - 1:
                if self.eye_4_motion_offset + speed >= self.CELL_SIZE - 1:
                    self.eye_4_motion_offset = self.CELL_SIZE - 1
                else:
                    self.eye_4_motion_offset += speed

        elif character == Character.GHOST_1 and self.ghost_1_motion_offset > 0:

            var: int = (50 if self.ghost_1_motion_offset > 50
                        else self.ghost_1_motion_offset)
            if direction == Direction.UP:
                motion_my = my - var
            elif direction == Direction.DOWN:
                motion_my = my + var
            elif direction == Direction.LEFT:
                motion_mx = mx - var
            elif direction == Direction.RIGHT:
                motion_mx = mx + var

        elif character == Character.GHOST_2 and self.ghost_2_motion_offset > 0:
            var = (50 if self.ghost_2_motion_offset > 50
                   else self.ghost_2_motion_offset)
            if direction == Direction.UP:
                motion_my = my - var
            elif direction == Direction.DOWN:
                motion_my = my + var
            elif direction == Direction.LEFT:
                motion_mx = mx - var
            elif direction == Direction.RIGHT:
                motion_mx = mx + var

        elif character == Character.GHOST_3 and self.ghost_3_motion_offset > 0:
            var = (50 if self.ghost_3_motion_offset > 50
                   else self.ghost_3_motion_offset)
            if direction == Direction.UP:
                motion_my = my - var
            elif direction == Direction.DOWN:
                motion_my = my + var
            elif direction == Direction.LEFT:
                motion_mx = mx - var
            elif direction == Direction.RIGHT:
                motion_mx = mx + var

        elif character == Character.GHOST_4 and self.ghost_4_motion_offset > 0:
            var = (50 if self.ghost_4_motion_offset > 50
                   else self.ghost_4_motion_offset)
            if direction == Direction.UP:
                motion_my = my - var
            elif direction == Direction.DOWN:
                motion_my = my + var
            elif direction == Direction.LEFT:
                motion_mx = mx - var
            elif direction == Direction.RIGHT:
                motion_mx = mx + var

        return motion_mx, motion_my

    def _get_ghost_character(self, ghost_id: int) -> int:
        """Get the character id of a ghost from its number.

           Args:
               ghost_id: The number of the ghost (1 to 4).

           Returns:
               The matching ``Character`` id.
        """

        if ghost_id == 1:
            return Character.GHOST_1
        elif ghost_id == 2:
            return Character.GHOST_2
        elif ghost_id == 3:
            return Character.GHOST_3
        return Character.GHOST_4

    def _get_eye_character(self, eye_id: int) -> int:
        """Get the character id of an eye from its number.

           Args:
               eye_id: The number of the eye (1 to 4).

           Returns:
               The matching ``Character`` id.
        """

        if eye_id == 1:
            return Character.EYE_1
        elif eye_id == 2:
            return Character.EYE_2
        elif eye_id == 3:
            return Character.EYE_3
        return Character.EYE_4

    def _get_eye_offset_var(self, _id: int) -> int:
        """Get the animation variable offset of the eyes.

        Args:
                _id: the id of the eyes.
        Returns:
                The animation offset variable.
        """

        if _id == 1:
            return self.eye_1_motion_offset
        elif _id == 2:
            return self.eye_2_motion_offset
        elif _id == 3:
            return self.eye_3_motion_offset

        return self.eye_4_motion_offset

    def _get_ghost_offset_var(self, _id: int) -> int:
        """Get the animation variable offset of the thost.

        Args:
                _id: the id of the thost.
        Returns:
                The animation offset variable.
        """

        if _id == 1:
            return self.ghost_1_motion_offset
        elif _id == 2:
            return self.ghost_2_motion_offset
        elif _id == 3:
            return self.ghost_3_motion_offset

        return self.ghost_4_motion_offset

    def _get_edibl_ghost_img_name(self, ghost: Ghost) -> str:
        """ Get the correct ghost name depending on hes status.

        Args:
                ghost: the ghost object.
        Returns:
                The name of the ghost image.
        """

        if self._get_ghost_offset_var(ghost.ghost_id) < 45:
            ghost_img_number: int = 1
        else:
            ghost_img_number = 2

        if ghost.edible_until - time.time() > 5:
            return "edibl_ghost_"
        elif ghost_img_number == 1:
            return "edibl_ghost_v2_"
        return "edibl_ghost_"

    def _do_maze_shaking(self) -> None:
        """Make the maze shake for a short time after a bomb explosion."""

        if self.is_shaking:
            if self.shake_counter < 60:
                self.x_shaking_offset += random.choice([-10, 10])
                self.y_shaking_offset += random.choice([-10, 10])
                self.shake_counter += 1
            else:
                self.is_shaking = False

                self.shake_counter = 0
                self.x_shaking_offset = 0
                self.y_shaking_offset = 0

    def _render(self) -> None:
        """Draw all the game objects of the current maze on the screen."""

        game: Game = self.current_game
        for r, row in enumerate(game.maze.grid):
            for c, cell in enumerate(row):

                m_c: int = c * self.CELL_SIZE
                m_r: int = r * self.CELL_SIZE

                if cell.up:
                    self._put_image_in_maze_place(m_c, m_r, "up")
                if cell.down:
                    self._put_image_in_maze_place(m_c, m_r, "down")
                if cell.left:
                    self._put_image_in_maze_place(m_c, m_r, "left")
                if cell.right:
                    self._put_image_in_maze_place(m_c, m_r, "right")

                if cell.super_pacgum:
                    self._put_image_in_maze_place(m_c, m_r, "super_pacgum")

                if cell.obj_ghost:
                    for ghost in cell.obj_ghost:
                        if self._get_ghost_offset_var(ghost.ghost_id) < 45:
                            ghost_img_number: int = 1
                        else:
                            ghost_img_number = 2
                        if ghost.edible:
                            self._put_image_in_maze_place(
                                *self._movement_animation(
                                    m_c,
                                    m_r,
                                    self._get_ghost_character(ghost.ghost_id),
                                    ghost.ghost_speed,
                                ),
                                self._get_edibl_ghost_img_name(ghost) +
                                str(ghost_img_number)
                            )

                        else:
                            self._put_image_in_maze_place(
                                *self._movement_animation(
                                    m_c,
                                    m_r,
                                    self._get_ghost_character(ghost.ghost_id),
                                    ghost.ghost_speed,
                                ),
                                "ghost" + str(ghost.ghost_id) + "_" +
                                str(ghost_img_number),
                            )

                if cell.player:
                    player_speed: int = self.current_game.player.player_speed
                    self._put_pac_man_img_in_maze(
                        *self._movement_animation(
                            m_c,
                            m_r,
                            Character.PAC_MAN,
                            player_speed
                        )
                    )

                if (r, c) in (game.maze.tunnel_a_pos, game.maze.tunnel_b_pos):
                    self._put_image_in_maze_place(m_c, m_r, "tunnel")

                if cell.obj_eyes:

                    for eyes in cell.obj_eyes:

                        if self._get_eye_offset_var(eyes.id) < 45:
                            eyes_img_number: int = 1
                        else:
                            eyes_img_number = 2
                        self._put_image_in_maze_place(
                            *self._movement_animation(
                                m_c,
                                m_r,
                                self._get_eye_character(eyes.id),
                                eyes.speed,
                                eyes
                            ), "eyes" + str(eyes.id) + "_" +
                            str(eyes_img_number)
                        )

                if cell.pacgum:
                    self._put_image_in_maze_place(m_c, m_r, "pacgum")

                if cell.booster:
                    self._put_image_in_maze_place(m_c, m_r, "rocket_" +
                                                  str(random.choice([1, 2])))

                if cell.bomb:
                    self._put_image_in_maze_place(m_c, m_r, "bomb_" +
                                                  str(random.choice([1, 2])))

                if cell.add_live:
                    self._put_image_in_maze_place(m_c, m_r, "heart_" +
                                                  str(random.choice([1, 2])))

                if cell.magnet:
                    self._put_image_in_maze_place(m_c, m_r, "magnet_" +
                                                  str(random.choice([1, 2])))

                if cell.is_42:
                    dlmtr: int = random.choice(
                        [
                            random.choice(range(-5, 6)),
                            random.choice(range(-15, 16)),
                        ]
                    )
                    self._put_image_in_maze_place(m_c + dlmtr, m_r, "ghost_42")

                if cell.extra_time:
                    self._put_image_in_maze_place(m_c, m_r, "extra_time_" +
                                                  str(random.choice([1, 2])))

                if cell.is_bomb:
                    self.current_game.sounds_obj.bomb_sound()
                    self.is_shaking = True

        self._do_maze_shaking()

    def _check_game_status(self) -> None:
        """Check whether the game is over or the level is completed."""

        if self.current_game.is_game_over():
            self.mlx_obj.mlx_loop_exit(self.init_ptr)
            self.show_game_over_screen = True
            return

        if self.current_game.level_complete():
            self._go_to_next_level()

    def _mouse_hover(self) -> None:
        """Draw a hand cursor over a button when the mouse is on it."""

        _, x, y = self.mlx_obj.mlx_mouse_get_pos(self.win_ptr)
        cheat_mode_buttons_ranges: List[Tuple] = [
            (self.increase_player_spd_x_x, self.increase_player_spd_y_y),
            (self.decrease_player_spd_x_x, self.decrease_player_spd_y_y),
            (self.increase_ghost_spd_x_x, self.increase_ghost_spd_y_y),
            (self.decrease_ghost_spd_x_x, self.decrease_ghost_spd_y_y),
            (self.go_to_next_level_x_x, self.go_to_next_level_y_y),
            (self.ghost_freeze_x_x, self.ghost_freeze_y_y),
            (self.extra_live_x_x, self.extra_live_y_y),
            (self.unedible_player_x_x, self.unedible_player_y_y),
        ]

        _3_mid_buttons_ranges: List[Tuple] = [
            (self.pause_game_x_x, self.pause_game_y_y),
            (self.pause_menu_x_x, self.pause_menu_y_y),
            (self.cheat_mode_x_x, self.cheat_mode_y_y)
        ]

        exit_resume_button_ranges: List[Tuple] = [
            (self.exit_x_x, self.exit_y_y),
            (self.resume_x_x, self.resume_y_y)]

        if self.is_pause_menu is False:
            for xx, yy in _3_mid_buttons_ranges:
                if X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(x, y, xx, yy):
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr,
                        self.images["hand_cursor"], x - 7, y)
                    break

        if self.is_cheat_mode and self.is_pause_menu is False\
                and self.pause_game is False:
            for xx, yy in cheat_mode_buttons_ranges:
                if X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(x, y, xx, yy):
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr,
                        self.images["hand_cursor"], x - 7, y)
                    return

        if self.is_pause_menu:
            for xx, yy in exit_resume_button_ranges:
                if X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(x, y, xx, yy):
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr,
                        self.images["hand_cursor"], x - 7, y)
                    return

    def _pause_game_or_unpause(self) -> None:
        """Pause the game if it is running, otherwise resume it."""

        if self.pause_game:
            self.current_game.pause_game_time(True)
            self.pause_game = False
        else:
            self.current_game.pause_game_time(False)
            self.pause_game = True
            self.time_befor_pause = self.current_game.get_time_left()

    def _pause_menu(self, just_for_mlx: None = None) -> None:
        """Activate pause menu State.
        Args:
            just_for_mlx: it is None sended by mlx_hook.
        """
        if self.pause_game is False:
            self._pause_game_or_unpause()

        self.is_pause_menu = True
        self.current_game.sounds_obj.stop_all()

    def _put_pause_menu_image(self) -> None:
        """Put the pause menu image on the screen if the menu is active."""

        if self.is_pause_menu:
            self.mlx_obj.mlx_put_image_to_window(
                self.init_ptr, self.win_ptr, self.images["pause_menu_bg"],
                self.X_MAZE_ON_SCREEN + self.x_shaking_offset - 22,
                self.Y_MAZE_ON_SCREEN + self.y_shaking_offset - 25)

    def _game_loop(self, just_for_mlx: Any) -> None:
        """Run one frame of the game (the mlx loop hook).

        Args:
            just_for_mlx: The parameter passed by the mlx loop hook (not used).
        """

        self._put_back_grounds()

        self._on_each_level()
        if self.error_in_func_on_each_level:
            return

        self._put_game_buttons_in_place()

        self._render()

        self._put_pause_menu_image()

        self.current_game.sounds_obj.play_start_sound(self.current_game)
        sound_obj: Sounds = self.current_game.sounds_obj
        if (sound_obj._is_playing(
                sound_obj.start_sound) and self.is_new_level_start):
            return
        self.is_new_level_start = False

        self._mouse_hover()

        if not self.pause_game:
            self.current_game.sounds_obj.play_movement_sound()
            self.current_game.update(direction=self.plr_next_direction)
            self._check_game_status()



        # print(self.player_motion_offset)

    def show_game_play_screen(self) -> None:
        """Create and show the game play screen.

        Runs the game until it is over, won or closed, then shows the
        Enter Score Name screen.

        Raises:
            ValueError: If the walls image cannot be loaded.
        """

        def key_hook(keycode: int, just_for_mlx: None) -> None:
            """Handle a key press (pause, move and cheat keys).

            Args:
                keycode: The number of the pressed key.
                just_for_mlx: None that mlx function send.
            """

            if keycode == Keys.CHEAT:
                self.is_cheat_mode = not self.is_cheat_mode
            elif keycode == Keys.ESPACE:
                if self.is_pause_menu is False:
                    self._pause_game_or_unpause()

            elif keycode == Keys.ESC:
                self._pause_menu()

            elif keycode == Keys.E and self.is_pause_menu is True:
                exit_loop(self.init_ptr)
            elif keycode == Keys.R and self.is_pause_menu is True:
                self._pause_game_or_unpause()
                self.is_pause_menu = False

            elif self.pause_game:
                return

            elif keycode == Keys.RIGHT or keycode == Keys.D:
                self.plr_next_direction = Direction.RIGHT
            elif keycode == Keys.LEFT or keycode == Keys.A:
                self.plr_next_direction = Direction.LEFT
            elif keycode == Keys.UP or keycode == Keys.W:
                self.plr_next_direction = Direction.UP
            elif keycode == Keys.DOWN or keycode == Keys.S:
                self.plr_next_direction = Direction.DOWN
            elif keycode == Keys.F11:
                self.current_game.sounds_obj.set_trol_sounds()
            elif keycode == Keys.N and self.is_cheat_mode:
                self.is_new_level_start = False
                self._go_to_next_level()
            elif keycode == Keys.L and self.is_cheat_mode:
                self.current_game.cheat_mode(extra_lives=1)
            elif keycode == Keys.F and self.is_cheat_mode:
                self.current_game.cheat_mode(ghost_freeze=True)
            elif keycode == Keys.E and self.is_pause_menu is False\
                    and self.is_cheat_mode:
                self.current_game.cheat_mode(invincible=True)

        def mouse_click(button: int, x: int, y: int, self: Any) -> None:
            """Handle a mouse click on the pause and cheat buttons.

            Only the left mouse button is handled.

            Args:
                button: The number of the mouse button.
                x: The x position of the click.
                y: The y position of the click.
                self: The StartGameScreen instance.
            """

            if self.is_pause_menu is False:

                if self.is_cheat_mode and self.pause_game is False:
                    if button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.increase_player_spd_x_x,
                        self.increase_player_spd_y_y
                    ):
                        self.current_game.cheat_mode(player_speed=1)
                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.decrease_player_spd_x_x,
                        self.decrease_player_spd_y_y
                    ):
                        self.current_game.cheat_mode(player_speed=-1)

                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.increase_ghost_spd_x_x,
                        self.increase_ghost_spd_y_y
                    ):
                        self.current_game.cheat_mode(ghost_speed=1)
                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.decrease_ghost_spd_x_x,
                        self.decrease_ghost_spd_y_y
                    ):
                        self.current_game.cheat_mode(ghost_speed=-1)

                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.go_to_next_level_x_x,
                        self.go_to_next_level_y_y
                    ):
                        self._go_to_next_level()

                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.extra_live_x_x, self.extra_live_y_y
                    ):
                        self.current_game.cheat_mode(extra_lives=1)

                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.ghost_freeze_x_x, self.ghost_freeze_y_y
                    ):
                        self.current_game.cheat_mode(ghost_freeze=True)

                    elif button == 1 and X_Y_Tools.is_click_in_button(
                        x, y, self.unedible_player_x_x,
                        self.unedible_player_y_y
                    ):
                        self.current_game.cheat_mode(invincible=True)

                if button == 1 and X_Y_Tools.is_click_in_button(
                    x, y, self.pause_menu_x_x, self.pause_menu_y_y
                ):
                    self._pause_menu()
                elif button == 1 and X_Y_Tools.is_click_in_button(
                    x, y, self.pause_game_x_x, self.pause_game_y_y
                ):
                    self._pause_game_or_unpause()
                elif button == 1 and X_Y_Tools.is_click_in_button(
                    x, y, self.cheat_mode_x_x, self.cheat_mode_y_y
                ):
                    self.is_cheat_mode = not self.is_cheat_mode

            else:
                if button == 1 and X_Y_Tools.is_click_in_button(
                    x, y, self.exit_x_x,
                    self.exit_y_y
                ):
                    exit_loop(self.init_ptr)
                elif button == 1 and X_Y_Tools.is_click_in_button(
                    x, y, self.resume_x_x,
                    self.resume_y_y
                ):
                    self._pause_game_or_unpause()
                    self.is_pause_menu = False

        def exit_loop(init_ptr: Any) -> None:
            """Stop the mlx loop.

            Args:
                init_ptr: The mlx init pointer.
            """

            self.show_game_over_screen = True
            self.mlx_obj.mlx_loop_exit(init_ptr)

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, None)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, self._pause_menu, None)

        self.mlx_obj.mlx_mouse_hook(self.win_ptr, mouse_click, self)
        self.mlx_obj.mlx_loop_hook(self.init_ptr, self._game_loop, None)

        self.mlx_obj.mlx_loop(self.init_ptr)

        self.current_game.sounds_obj.stop_all()

        for img_ptr in self.images.values():
            self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)

        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)

        if self.error_in_func_on_each_level:
            raise ValueError(
                FileTools.error_raise_message(
                    "Start_Game_screen.py",
                    "StartGameScreen",
                    "_on_each_level()",
                    "error in function: _on_each_level",
                )
            )

        # if self.show_game_over_screen:
        #     EnterScoreNameScreen(
        #         self.current_game.player.score
        #     ).show_enter_score_name_screen(is_win=False)

        # else:
        #     EnterScoreNameScreen(
        #         self.current_game.player.score
        #     ).show_enter_score_name_screen(is_win=True)


StartGameScreen(1).show_game_play_screen()
