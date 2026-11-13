"""Provide the Enter Score Name screen of the game."""

from mlx import Mlx
from typing import Any, Dict
import os
from Files_Tools import PacManFilesTools, FileTools, Keys
from Sounds_Effects import Sounds


class EnterScoreNameScreen:
    """Provide the methods that build the Enter Score Name screen."""

    def __init__(self, score: int) -> None:
        """Initialize the screen with the needed data.

        Args:
            score: The score achieved by the player.

        Raises:
            ValueError: If mlx_init() or mlx_new_window() fails, or if an
                image cannot be loaded.
        """

        self.sounds: Sounds = Sounds()
        self.sounds.init_sounds()
        self.score: int = score

        self.mlx_obj: Mlx = Mlx()

        self.init_ptr: Any = self.mlx_obj.mlx_init()
        if not self.init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Enter_Score_name_Screen.py",
                    "EnterScoreNameScreen",
                    "__init__()",
                    "mlx_init() failed",
                )
            )

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (1920, 1080)
        FileTools.check_pc_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.images: Dict[str, Any] = self.load_all_imgs()

        self.win_ptr: Any = self.mlx_obj.mlx_new_window(
            self.init_ptr,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            "Enter Score Name",
        )
        if not self.win_ptr:
            for img_ptr in self.images.values():
                self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Enter_Score_name_Screen.py",
                    "EnterScoreNameScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.score_name: str = ""

        self.is_upper: bool = False

    def load_all_imgs(self) -> Dict[str, Any]:
        """Load all the images that this screen depends on.

        Returns:
            A dictionary mapping each image name to its pointer.

        Raises:
            ValueError: If one of the XPM files cannot be loaded.
        """

        base_path: str = PacManFilesTools.get_base_path_for_images()

        alphas_path: str = base_path + "Alpha" + os.sep
        digits_path: str = base_path + "Digits" + os.sep
        win_path: str = base_path + "Score_Name" + os.sep
        game_over_path: str = base_path + "Score_Name" + os.sep

        images_n_p: Dict[str, Any] = {}

        for (
            char
        ) in "QWERTYUIOPASDFGHJKLZXCVBNM0123456789qwer"\
                "tyuiopasdfghjklzxcvbnm":

            if char.isalpha():
                if char.isupper():
                    path: str = alphas_path + char + "_upper.png"
                else:
                    path = alphas_path + char + "_lower.png"
            else:
                path = digits_path + char + ".png"

            char_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
                self.init_ptr, path
            )

            if not char_ptr:
                for destroy_ptr in images_n_p.values():
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr)
                self.mlx_obj.mlx_release(self.init_ptr)
                raise ValueError(
                    FileTools.error_raise_message(
                        "Enter_Score_name_Screen.py",
                        "EnterScoreNameScreen",
                        "load_all_imgs()",
                        f"{char}.png not found",
                    )
                )

            images_n_p[char] = char_ptr

        win_game_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
            self.init_ptr, win_path + "win_game.png"
        )

        if not win_game_ptr:
            for img_ptr in images_n_p.values():
                self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Enter_Score_name_Screen.py",
                    "EnterScoreNameScreen",
                    "load_all_imgs()",
                    "win_game.png not found",
                )
            )

        images_n_p["win_game"] = win_game_ptr

        game_over_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
            self.init_ptr, game_over_path + "game_over.png"
        )

        if not game_over_ptr:
            for img_ptr in images_n_p.values():
                self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Enter_Score_name_Screen.py",
                    "EnterScoreNameScreen",
                    "load_all_imgs()",
                    "game_over.png not found",
                )
            )

        images_n_p["game_over"] = game_over_ptr

        return images_n_p

    def put_word_in_place(self, x: int, y: int, word: str) -> None:
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
            x += 40

    def get_char(self, keycode: int) -> str:
        """Convert a keycode into its character.

        Args:
            keycode: The number of the key.

        Returns:
            The character that represents the keycode, or an empty string
            if the keycode is not supported.
        """

        keycodes: Dict[int, str] = {
            113: "q", 119: "w", 101: "e", 114: "r", 116: "t", 121: "y",
            117: "u", 105: "i", 111: "o", 112: "p", 97: "a", 115: "s",
            100: "d", 102: "f", 103: "g", 104: "h", 106: "j", 107: "k",
            108: "l", 122: "z", 120: "x", 99: "c", 118: "v", 98: "b",
            110: "n", 109: "m", 65438: "0", 65436: "1", 65433: "2",
            65435: "3", 65430: "4", 65437: "5", 65432: "6", 65429: "7",
            65431: "8", 65434: "9", 49: "1", 50: "2", 51: "3", 52: "4",
            53: "5", 54: "6", 55: "7", 56: "8", 57: "9", 48: "0", 32: " ",
        }

        return keycodes.get(keycode, "")

    def _fix_score(self, score: str) -> str:
        """Truncate the score text so it fits on the screen.

        Args:
            score: The score to truncate.

        Returns:
            The score limited to 15 characters.
        """

        if len(score) > 15:
            new_score: str = score[:15]
            return new_score
        else:
            return score

    def is_valide_name(self) -> bool:
        """Check if Score Name is Valide

        Returns:
            True if Valide Name False if not Valide name.
        """

        counter: int = 0
        for c in self.score_name:
            if c.isalnum():
                counter += 1
        if not counter:
            return False
        return True

    def show_enter_score_name_screen(self, is_win: bool = False) -> None:
        """Create and show the Enter Score Name screen.

        Args:
            is_win: True to show the win screen, False to show the
                game over screen.
        """

        def key_hook(keycode: int, self: EnterScoreNameScreen) -> None:
            """Handle a key press and update the screen.

            Args:
                keycode: The number of the pressed key.
                self: The EnterScoreNameScreen instance.
            """

            if keycode == Keys.UPPER:
                self.is_upper = not self.is_upper
                return
            elif keycode == Keys.ESC:
                exit_loop(self)
                return
            elif self.get_char(keycode) != "" and len(self.score_name) < 10:
                if self.is_upper:
                    self.score_name += self.get_char(keycode).upper()
                else:
                    self.score_name += self.get_char(keycode).lower()

            elif keycode == Keys.DELET:
                self.score_name = self.score_name[:-1]
            elif keycode == Keys.ENTRE and\
                    self.score_name and self.is_valide_name():
                PacManFilesTools().add_score_to_highscores_file(
                    self.score_name, self.score
                )
                exit_loop(self)
                return

            if is_win:
                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr, self.win_ptr, self.images["win_game"], 0, -50
                )
            else:
                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr, self.win_ptr, self.images["game_over"], 0, -50
                )

            if is_win:
                self.put_word_in_place(920, 960, self.score_name)
                self.put_word_in_place(
                    670, 845, self._fix_score(str(self.score))
                )
            else:
                self.put_word_in_place(900, 955, self.score_name)
                self.put_word_in_place(
                    670, 828, self._fix_score(str(self.score))
                )

        def exit_loop(self: EnterScoreNameScreen) -> None:
            """Exit the mlx loop.

            Args:
                self: The EnterScoreNameScreen instance.
            """

            self.mlx_obj.mlx_loop_exit(self.init_ptr)

        if is_win:
            self.mlx_obj.mlx_put_image_to_window(
                self.init_ptr, self.win_ptr, self.images["win_game"], 0, -50
            )
            self.sounds.win_or_loss_sound("win")
        else:
            self.mlx_obj.mlx_put_image_to_window(
                self.init_ptr, self.win_ptr, self.images["game_over"], 0, -50
            )
            self.sounds.win_or_loss_sound("over")

        if is_win:
            self.put_word_in_place(670, 845, self._fix_score(str(self.score)))
        else:
            self.put_word_in_place(670, 828, self._fix_score(str(self.score)))

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, self)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, exit_loop, self)

        self.mlx_obj.mlx_loop(self.init_ptr)

        for img_ptr in self.images.values():
            self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)

        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)
        self.sounds.win_or_loss_sound("stop")
