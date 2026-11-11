"""Provide the Instructions screen of the game."""

from mlx import Mlx
from typing import Any
import os
from Files_Tools import FileTools, Keys, PacManFilesTools


class InstructionsScreen:
    """Provide the methods that build the Instructions screen."""

    def __init__(self) -> None:
        """Initialize the screen with the needed data.

        Raises:
            ValueError: If mlx_init(), mlx_new_window() or
                mlx_xpm_file_to_image() fails.
        """

        self.mlx_obj: Mlx = Mlx()
        self.init_ptr: Any = self.mlx_obj.mlx_init()
        if not self.init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Instructions_screen.py",
                    "InstructionsScreen",
                    "__init__()",
                    "mlx_init() failed",
                )
            )

        size_ptr, self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (
            self.mlx_obj.mlx_get_screen_size(self.init_ptr)
        )
        if size_ptr != 0:
            self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (3840, 2160)
        FileTools.check_pc_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

        base_path: str = PacManFilesTools.get_base_path_for_images() + os.sep\
            + "Instructions" + os.sep + "instructions_img.xpm"

        self.instr_img_ptr, _, _ = self.mlx_obj.mlx_xpm_file_to_image(
            self.init_ptr, base_path
        )
        if not self.instr_img_ptr:
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Instructions_screen.py",
                    "InstructionsScreen",
                    "__init__()",
                    "instructions_img.xpm failed",
                )
            )

        self.win_ptr: Any = self.mlx_obj.mlx_new_window(
            self.init_ptr,
            self.SCREEN_WIDTH,
            self.SCREEN_HEIGHT,
            "Instructions",
        )
        if not self.win_ptr:
            self.mlx_obj.mlx_destroy_image(self.init_ptr, self.instr_img_ptr)
            self.mlx_obj.mlx_release(self.init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Instructions_screen.py",
                    "InstructionsScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.mlx_obj.mlx_put_image_to_window(
            self.init_ptr, self.win_ptr, self.instr_img_ptr, 0, 0
        )

    def show_instructions_screen(self) -> None:
        """Show the Instructions screen.

        Waits until the player presses Esc or closes the window.
        """

        def key_hook(keycode: int, self: InstructionsScreen) -> None:
            """Exit the loop when the Esc key is pressed.

            Args:
                keycode: The number of the pressed key.
                self: The InstructionsScreen instance.
            """

            if keycode == Keys.ESC:
                exit_loop(self)

        def exit_loop(self: InstructionsScreen) -> None:
            """Exit the mlx loop.

            Args:
                self: The InstructionsScreen instance.
            """

            self.mlx_obj.mlx_loop_exit(self.init_ptr)

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, self)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, exit_loop, self)

        self.mlx_obj.mlx_loop(self.init_ptr)

        self.mlx_obj.mlx_destroy_image(self.init_ptr, self.instr_img_ptr)
        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)
