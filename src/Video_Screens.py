"""Provide the intro video screen of the game."""

from mlx import Mlx
from typing import Any, List
import os
import time
from Sounds_Effects import Sounds
from Files_Tools import FileTools, Keys, PacManFilesTools


class VideoScreen:
    """Provide the methods that build the intro video screen."""

    def __init__(self) -> None:
        """Initialize the screen with the needed data.

        Checks the command line arguments, initializes the sounds and
        creates the mlx window.

        Raises:
            ValueError: If the arguments are invalid, or if mlx_init() or
                mlx_new_window() fails.
        """

        FileTools().check_args()

        self.sounds_obj: Sounds = Sounds()
        self.sounds_obj.init_sounds()

        self.mlx_obj: Mlx = Mlx()

        self.init_ptr: Any = self.mlx_obj.mlx_init()
        if not self.init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Video_Screens.py",
                    "VideoScreen",
                    "__init__()",
                    "mlx_init() failed",
                )
            )

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = (1920, 1080)
        FileTools.check_pc_resolution(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        FileTools.resolution_error_window(self.SCREEN_WIDTH,
                                          self.SCREEN_HEIGHT)

        self.win_ptr: Any = self.mlx_obj.mlx_new_window(
            self.init_ptr, self.SCREEN_WIDTH, self.SCREEN_HEIGHT, "Intro"
        )
        if not self.win_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Video_Screens.py",
                    "VideoScreen",
                    "__init__()",
                    "mlx_new_window() failed",
                )
            )

        self.images_paths: List[str] = self.load_all_imgs_paths()

        self.index: int = 0

        self.error_appeared: bool = False
        self.e: str | Exception = ""

    def load_all_imgs_paths(self) -> List[str]:
        """Build the list of the paths of all the intro frames.

        Returns:
            The paths of the intro1 frames, the background image, the
            black wall image and the intro2 frames, in display order.
        """

        imgs: List[str] = []

        base_path: str = PacManFilesTools.get_base_path_for_images()\
            + "Videos" + os.sep

        for i in range(1, 121):
            imgs.append(base_path + f"intro1{os.sep}frame_" + str(i) + ".png")

        imgs.append(base_path + "intro_background.png")
        imgs.append(base_path + "black_wall.png")

        for i in range(1, 281):
            imgs.append(base_path + f"intro2{os.sep}frame_" + str(i) + ".png")

        return imgs

    def show_video_screen(self) -> None:
        """Play the intro video until it ends or the player skips it.

        Raises:
            ValueError: If an error happens while the video is playing.
        """

        def video(self: VideoScreen) -> None:
            """Show the next frame of the video (the mlx loop hook).

            If an error happens, it is saved and the loop is stopped.

            Args:
                self: The VideoScreen instance.
            """

            img_ptr: Any = None
            try:

                if self.index >= len(self.images_paths):
                    self.mlx_obj.mlx_loop_exit(self.init_ptr)
                    self.sounds_obj.play_or_stop_intro_sound("stop")
                    return

                img_ptr, _, _ = self.mlx_obj.mlx_png_file_to_image(
                    self.init_ptr, self.images_paths[self.index]
                )

                if not img_ptr:
                    raise ValueError("failed to create "
                                     f"image: {self.images_paths[self.index]}")

                if "/intro1/" in self.images_paths[self.index]:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr, img_ptr, 656, 300
                    )

                elif "/intro_background.png" in self.images_paths[self.index]:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr, img_ptr, 0, 0
                    )

                elif "/black_wall.png" in self.images_paths[self.index]:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr, img_ptr, 543, 180
                    )

                elif "/intro2/" in self.images_paths[self.index]:
                    self.mlx_obj.mlx_put_image_to_window(
                        self.init_ptr, self.win_ptr, img_ptr, 568, 205
                    )

                self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
                img_ptr = None

                if "/intro2/" in self.images_paths[self.index]:
                    time.sleep(1 / 12)

                self.index += 1
            except Exception as e:
                if img_ptr:
                    self.mlx_obj.mlx_destroy_image(self.init_ptr, img_ptr)
                self.mlx_obj.mlx_loop_exit(self.init_ptr)
                self.error_appeared = True
                self.e = e
                return

        def key_hook(keycode: int, self: VideoScreen) -> None:
            """Skip the video when the Esc key is pressed.

            Args:
                keycode: The number of the pressed key.
                self: The VideoScreen instance.
            """

            if keycode == Keys.ESC:
                self.sounds_obj.play_or_stop_intro_sound("stop")
                self.mlx_obj.mlx_loop_exit(self.init_ptr)

        def exit_loop(self: VideoScreen) -> None:
            """Stop the intro sound and exit the mlx loop.

            Args:
                self: The VideoScreen instance.
            """

            self.sounds_obj.play_or_stop_intro_sound("stop")
            self.mlx_obj.mlx_loop_exit(self.init_ptr)

        self.mlx_obj.mlx_key_hook(self.win_ptr, key_hook, self)
        self.mlx_obj.mlx_loop_hook(self.init_ptr, video, self)
        self.mlx_obj.mlx_hook(self.win_ptr, 33, 0, exit_loop, self)

        self.sounds_obj.play_or_stop_intro_sound("play")
        self.mlx_obj.mlx_loop(self.init_ptr)

        self.mlx_obj.mlx_destroy_window(self.init_ptr, self.win_ptr)
        self.mlx_obj.mlx_release(self.init_ptr)

        if self.error_appeared:
            self.sounds_obj.play_or_stop_intro_sound("stop")
            raise ValueError(
                FileTools.error_raise_message(
                    "Videos_screens.py", "VideoScreen", "video()", self.e
                )
            )
