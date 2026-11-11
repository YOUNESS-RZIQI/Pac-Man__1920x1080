"""Provide the Highscore List screen of the game."""

from mlx import Mlx
from typing import Any, Dict, List
import os
from Files_Tools import PacManFilesTools, FileTools, Keys


class HighscoreListScreen:
    """Provide the methods that build the Highscore List screen."""

    def __init__(self) -> None:
        """Initialize the screen with the needed data.

        Raises:
            ValueError: If mlx_init() or mlx_new_window() fails, or if an
                image cannot be loaded.
        """

        self.mlx_obj: Mlx = Mlx()
        self.init_ptr: Any = self.mlx_obj.mlx_init()
        if not self.init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "High_scoore_list_screen.py",
                    "HighscoreListScreen",
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
            "High Scores List",
        )
        if not self.win_ptr:
            for img_ptr in self.images.values():
                self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "High_scoore_list_screen.py",
                    "HighscoreListScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.highscores: Dict[str, Any] = (
            PacManFilesTools().get_highscores_data()
        )

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
        background_path: str = base_path + "Highscore_List" + os.sep

        images_n_p: Dict[str, Any] = {}

        for (
            char
        ) in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm0123456789":

            if char.isalpha():
                if char.isupper():
                    path: str = alphas_path + char + "_upper.xpm"
                else:
                    path = alphas_path + char + "_lower.xpm"
            else:
                path = digits_path + char + ".xpm"

            char_ptr, _, _ = self.mlx_obj.mlx_xpm_file_to_image(
                self.init_ptr, path
            )

            if not char_ptr:
                for destroy_ptr in images_n_p.values():
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr)
                self.mlx_obj.mlx_release(self.init_ptr)
                raise ValueError(
                    FileTools.error_raise_message(
                        "High_scoore_list_screen.py",
                        "HighscoreListScreen",
                        "load_all_imgs()",
                        f"{char}.xpm not found",
                    )
                )

            images_n_p[char] = char_ptr

        bkgrd_ptr, _, _ = self.mlx_obj.mlx_xpm_file_to_image(
            self.init_ptr, background_path + "high_score_img.xpm"
        )

        if not bkgrd_ptr:
            for destroy_ptr in images_n_p.values():
                self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "High_scoore_list_screen.py",
                    "HighscoreListScreen",
                    "load_all_imgs()",
                    "high_score_img.xpm not found",
                )
            )

        images_n_p["high_score_img"] = bkgrd_ptr

        return images_n_p

    def fix_score(self, score: str) -> str:
        """Truncate the score text so it fits on the screen.

        Args:
            score: The score to truncate.

        Returns:
            The score limited to 7 characters.
        """

        if len(score) > 7:
            new_score: str = score[:7]
            return new_score
        else:
            return score

    def put_word_in_place(self, x: int, y: int, word: str) -> None:
        """Put the characters of a word at a specific position on screen.

        Args:
            x: The starting x position.
            y: The starting y position.
            word: The word to put on the screen.
        """

        for c in word:
            if c == " ":
                x += 30
                continue

            self.mlx_obj.mlx_put_image_to_window(
                self.init_ptr, self.win_ptr, self.images[c], x, y
            )
            x += 90

    def show_highscores_screen(self) -> None:
        """Create and show the Highscore List screen.

        Draws the names and scores of the best players (up to 10) and
        waits until the player presses Esc or closes the window.
        """

        def key_hook(keycode: int, self: HighscoreListScreen) -> None:
            """Exit the loop when the Esc key is pressed.

            Args:
                keycode: The number of the pressed key.
                self: The HighscoreListScreen instance.
            """

            if keycode == Keys.ESC:
                exit_loop(self)

        def exit_loop(self: HighscoreListScreen) -> None:
            """Exit the mlx loop.

            Args:
                self: The HighscoreListScreen instance.
            """

            self.mlx_obj.mlx_loop_exit(self.init_ptr)

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.images["high_score_img"], 0, 0
        )

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, self)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, exit_loop, self)

        names: List[str] = [name for name in self.highscores]
        scores: List[str] = [str(name) for name in self.highscores.values()]
        rng: int = min(len(names), 10)

        for i in range(rng):
            self.put_word_in_place(1230, 580 + (120 * i), names[i])
            self.put_word_in_place(
                2250, 580 + (120 * i), self.fix_score(scores[i])
            )

        self.mlx_obj.mlx_loop(self.init_ptr)

        for img_ptr in self.images.values():
            self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)

        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)
