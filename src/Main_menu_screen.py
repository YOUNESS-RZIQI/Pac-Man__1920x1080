"""Provide the Main Menu screen of the game."""

from Files_Tools import FileTools, Keys, E_MainMenuOptions, PacManFilesTools
from typing import Any, Dict, List, Tuple
import os
from mlx import Mlx


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


class MainMenuScreen:
    """Provide the methods that build the Main Menu screen."""

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
                    "Main_menu_screen.py",
                    "MainMenuScreen",
                    "__init__()",
                    "mlx_init() failed",
                )
            )

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (1920, 1080)
        FileTools.check_pc_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        self.win_ptr: Any = self.mlx_obj.mlx_new_window(
            self.init_ptr, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Main Menu"
        )
        if not self.win_ptr:
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Main_menu_screen.py",
                    "MainMenuScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.images: Dict[str, Any] = self.load_all_imgs()

        self.start_game_show_count: int = 0
        self.hiscors_show_count: int = 0
        self.intsr_show_count: int = 0
        self.exit_show_count: int = 0

        # here
        self.mmc_width_x_x: Tuple[int, int] = (671, 2521)
        self.str_g_button_y_y: Tuple[int, int] = (307, 862)
        self.vw_scor_button_y_y: Tuple[int, int] = (472, 1183)
        self.istrc_button_y_y: Tuple[int, int] = (651, 1513)
        self.exit_button_y_y: Tuple[int, int] = (808, 1745)

        self.chosen_screen: int = E_MainMenuOptions.EXIT

        self.is_error_inside_mlx: bool = False
        self.e: str | Exception = ""

    def load_all_imgs(self) -> Dict[str, Any]:
        """Load all the images that this screen depends on.

        Returns:
            A dictionary mapping each image name to its pointer.

        Raises:
            ValueError: If one of the XPM files cannot be loaded.
        """

        base_path: str = PacManFilesTools.get_base_path_for_images() +\
            "Main_menu" + os.sep

        img_files: Dict[str, str] = {
            "main_menu": "main_menu.png",
            "start_game_button": "start_game_button.png",
            "view_highscores_button": "view_highscores_button.png",
            "instructions_button": "instructions_button.png",
            "exit_button": "exit_button.png",
            "hand_cursor": "hand_cursor.png"
        }

        images: Dict[str, Any] = {}

        for name, filename in img_files.items():
            path: str = base_path + filename

            img, _, _ = self.mlx_obj.mlx_png_file_to_image(self.init_ptr, path)

            if not img:
                for destroy_ptr in images.values():
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, destroy_ptr)
                self.mlx_obj.mlx_release(self.init_ptr)
                raise ValueError(
                    FileTools.error_raise_message(
                        "Main_menu_screen.py",
                        "MainMenuScreen",
                        "load_all_imgs()",
                        f"{filename} not found",
                    )
                )

            images[name] = img

        return images

    def show_main_menu_screen(self) -> int:
        """Create and show the Main Menu screen.

        Handles the mouse hover, the mouse clicks and the keyboard
        shortcuts until the player chooses an option.

        Returns:
            The chosen option (one of the E_MainMenuOptions values).

        Raises:
            ValueError: If an error happens inside the mlx loop.
        """

        def exit_loop(self: MainMenuScreen) -> None:
            """Exit the mlx loop and select the exit option.

            Args:
                self: The MainMenuScreen instance.
            """

            self.mlx_obj.mlx_loop_exit(self.init_ptr)
            self.chosen_screen = E_MainMenuOptions.EXIT

        def motion(mouse_x: int, mouse_y: int, self: MainMenuScreen) -> None:
            """Show the highlighted image of the button under the mouse.

            Shows the normal menu image if the mouse is not over a button.

            Args:
                mouse_x: The x position of the mouse.
                mouse_y: The y position of the mouse.
                self: The MainMenuScreen instance.
            """

            if X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(
                mouse_x, mouse_y, self.mmc_width_x_x, self.str_g_button_y_y
            ):
                self.start_game_show_count += 1
                if self.start_game_show_count > 8:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["main_menu"],
                        0,
                        0,
                    )
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["start_game_button"],
                        self.mmc_width_x_x[0] - 22,
                        self.str_g_button_y_y[0],
                    )
                    self.start_game_show_count = 0

            elif X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(
                mouse_x, mouse_y, self.mmc_width_x_x, self.vw_scor_button_y_y
            ):
                self.hiscors_show_count += 1
                if self.hiscors_show_count > 8:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["main_menu"],
                        0,
                        0,
                    )
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["view_highscores_button"],
                        self.mmc_width_x_x[0] - 25,
                        self.vw_scor_button_y_y[0],
                    )
                    self.hiscors_show_count = 0

            elif X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(
                mouse_x, mouse_y, self.mmc_width_x_x, self.istrc_button_y_y
            ):
                self.intsr_show_count += 1
                if self.intsr_show_count > 8:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["main_menu"],
                        0,
                        0,
                    )
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["instructions_button"],
                        self.mmc_width_x_x[0] - 20,
                        self.istrc_button_y_y[0],
                    )
                    self.intsr_show_count = 0

            elif X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(
                mouse_x, mouse_y, self.mmc_width_x_x, self.exit_button_y_y
            ):
                self.exit_show_count += 1
                if self.exit_show_count > 8:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["main_menu"],
                        0,
                        0,
                    )
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr,
                        self.win_ptr,
                        self.images["exit_button"],
                        self.mmc_width_x_x[0] - 8,
                        self.exit_button_y_y[0],
                    )
                    self.exit_show_count = 0

            else:
                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["main_menu"],
                    0,
                    0,
                )

                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["start_game_button"],
                    self.mmc_width_x_x[0] - 22,
                    self.str_g_button_y_y[0],
                )

                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["view_highscores_button"],
                    self.mmc_width_x_x[0] - 25,
                    self.vw_scor_button_y_y[0],
                )

                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["instructions_button"],
                    self.mmc_width_x_x[0] - 20,
                    self.istrc_button_y_y[0],
                )

                self.mlx_obj.mlx_put_image_to_window(
                    self.init_ptr,
                    self.win_ptr,
                    self.images["exit_button"],
                    self.mmc_width_x_x[0] - 8,
                    self.exit_button_y_y[0],
                )
                self.start_game_show_count = 0
                self.exit_show_count = 0
                self.intsr_show_count = 0
                self.hiscors_show_count = 0

        def curser_animation_loop(self: MainMenuScreen) -> None:
            """Update the displayed image and the hand cursor.

            If an error happens, it is saved and the loop is stopped.

            Args:
                self: The MainMenuScreen instance.
            """

            try:
                _, x, y = self.mlx_obj.mlx_mouse_get_pos(self.win_ptr)

                motion(x, y, self)

                ranges: List[Tuple] = [
                        (self.mmc_width_x_x, self.str_g_button_y_y),
                        (self.mmc_width_x_x, self.vw_scor_button_y_y),
                        (self.mmc_width_x_x, self.istrc_button_y_y),
                        (self.mmc_width_x_x, self.exit_button_y_y)
                    ]
                for xx, yy in ranges:
                    if X_Y_Tools.is_x_in_range_xx_and_y_in_range_yy(x, y,
                                                                    xx, yy):
                        self.mlx_obj.mlx_put_image_to_window(
                            self.init_ptr, self.win_ptr,
                            self.images["hand_cursor"], x - 28, y)
                        break

                motion(x, y, self)

            except Exception as e:
                self.is_error_inside_mlx = True
                self.e = e
                exit_loop(self)

        def click(button: int, x: int, y: int, self: MainMenuScreen) -> None:
            """Select the option whose button was clicked.

            Only the left mouse button is handled.

            Args:
                button: The number of the mouse button.
                x: The x position of the click.
                y: The y position of the click.
                self: The MainMenuScreen instance.
            """

            print(x, y)
            return

            if button == 1 and X_Y_Tools.is_click_in_button(
                x, y, self.mmc_width_x_x, self.str_g_button_y_y
            ):

                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.START_GAME_SCREEN

            elif button == 1 and X_Y_Tools.is_click_in_button(
                x, y, self.mmc_width_x_x, self.vw_scor_button_y_y
            ):

                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.HIGH_SCORES_SCREEN

            elif button == 1 and X_Y_Tools.is_click_in_button(
                x, y, self.mmc_width_x_x, self.istrc_button_y_y
            ):

                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.INSTRUCTIONS_SCREEN

            elif button == 1 and X_Y_Tools.is_click_in_button(
                x, y, self.mmc_width_x_x, self.exit_button_y_y
            ):
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.EXIT

        def key_hook(keycode: int, self: MainMenuScreen) -> None:
            """Select an option with the keyboard.

            S starts the game, H shows the highscores, I shows the
            instructions, and E or Esc exits.

            Args:
                keycode: The number of the pressed key.
                self: The MainMenuScreen instance.
            """

            if keycode == Keys.ESC:
                exit_loop(self)

            elif keycode == Keys.S:
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.START_GAME_SCREEN

            elif keycode == Keys.H:
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.HIGH_SCORES_SCREEN

            elif keycode == Keys.I:
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.INSTRUCTIONS_SCREEN

            elif keycode == Keys.E:
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.chosen_screen = E_MainMenuOptions.EXIT

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.images["main_menu"], 0, 0
        )

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, self)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, exit_loop, self)

        self.mlx_obj.mlx_mouse_hook(self.win_ptr, click, self)
        self.mlx_obj.mlx_loop_hook(self.init_ptr, curser_animation_loop, self)

        self.mlx_obj.mlx_loop(self.init_ptr)

        for img_ptr in self.images.values():
            self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)

        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)

        if self.is_error_inside_mlx:
            raise ValueError(
                FileTools.error_raise_message(
                    "Main_menu_screen.py",
                    "MainMenuScreen",
                    "animation_loop()",
                    self.e,
                )
            )

        return self.chosen_screen


MainMenuScreen().show_main_menu_screen()