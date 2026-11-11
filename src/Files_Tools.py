"""Provide the tools that the screens may need."""

from typing import List, Dict, Any
from pathlib import Path
from mlx import Mlx
import json
import sys
import os


class E_MainMenuOptions:
    """Identifiers of the screens and options of the main menu."""

    MAIN_MENU_SCREEN: int = 0
    START_GAME_SCREEN: int = 1
    INSTRUCTIONS_SCREEN: int = 2
    HIGH_SCORES_SCREEN: int = 3
    EXIT: int = 4


class Keys:
    """Keycodes of the keyboard keys used by the game."""

    ESC: int = 65307
    DELET: int = 65288
    ENTRE: int = 65293
    LEFT: int = 65361
    RIGHT: int = 65363
    UP: int = 65362
    DOWN: int = 65364
    ESPACE: int = 32
    S: int = 115
    H: int = 104
    I: int = 105  # noqa: E741
    E: int = 101
    F11: int = 65480
    N: int = 110
    F: int = 102
    L: int = 108
    UPPER: int = 65509
    W: int = 119
    A: int = 97
    D: int = 100
    R: int = 114
    CHEAT: int = 96


class Character:
    """Identifiers of the game characters (Pac-Man and the ghosts)."""

    EYE_1: int = 1
    EYE_2: int = 2
    EYE_3: int = 3
    EYE_4: int = 4
    PAC_MAN: int = 5
    GHOST_1: int = 6
    GHOST_2: int = 7
    GHOST_3: int = 8
    GHOST_4: int = 9


class FileTools:
    """Provide methods to read configuration files and report errors."""

    def _is_comment(self, line: str) -> bool:
        """Check whether a line is a comment.

        A line is a comment if it starts with ``#`` or ``//``.

        Args:
            line: The line to check.

        Returns:
            True if the line is a comment, False otherwise.
        """

        if line and line[0] == "#":
            return True
        elif line and len(line) >= 2 and line[:2] == "//":
            return True
        else:
            return False

    def separate_content_and_comments_from_file(
        self, path: str
    ) -> Dict[str, str | List[str]]:
        """Separate the content of a file from its comments.

        Args:
            path: The path of the file to read.

        Returns:
            A dictionary with the keys ``"config"`` (the content without
            comments, as a string) and ``"comments"`` (the list of
            comment lines).

        Raises:
            PermissionError: If the file cannot be read.
            FileNotFoundError: If the file does not exist.
            ValueError: If any other error happens while reading.
        """

        config: str = ""
        comments: List[str] = []
        try:
            with open(path, "r") as file:
                lines: List[str] = file.readlines()
                for line in lines:
                    line = line.strip()
                    if self._is_comment(line):
                        comments.append(line)
                    else:
                        config += line + "\n"
            return {"config": config, "comments": comments}

        except PermissionError:
            raise PermissionError(
                "\033[91mError in src/Files_Tools.py:"
                "\n\tYou Don't have Permission "
                "To Read Configuration file: \033[94m"
                f"{path}\033[0m"
            )

        except FileNotFoundError:
            raise FileNotFoundError(
                "\033[91mError in src/Files_Tools.py:"
                f"\n\tfile \033[94m'{path}'"
                "\033[91m Not Found\033[0m"
            )

        except Exception as e:
            raise ValueError(
                "\033[91mError in src/Files_Tools.py:"
                f"\n\t{e}"
                "\nAn Error appears in configuration.json"
                " File\033[0m"
            )

    def get_configuration_file_path(self) -> str:
        """Get the configuration file path from the command line.

        Returns:
            The full path of the configuration file.

        Raises:
            ValueError: If there is not exactly one argument, or if it
                does not end with ``.json``.
        """

        if len(sys.argv) != 2 or not sys.argv[1].endswith(".json"):
            raise ValueError(
                "\033[91mYou must give the correct two"
                " arguments:\n\n Input Example:\n\n\t"
                "\033[92muv run python3 \033[93mEntry_point.py"
                " \033[94mconfigurationfile.json "
                "(Must be json)\n\033[0m"
            )

        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            path: str = (
                str(Path(sys.executable).parent) + os.sep + sys.argv[1]
            )
        else:
            path = str(Path(__file__).parent.parent) + os.sep + sys.argv[1]

        return str(Path(path))

    def get_json_as_dict(self, path: str) -> Dict[str, Dict]:
        """Load a JSON file, ignoring comment lines, as a dictionary.

        Args:
            path: The path of the JSON file.

        Returns:
            The content of the file as a dictionary.

        Raises:
            ValueError: If the content is not valid JSON.
        """

        s_config: str = str(
            self.separate_content_and_comments_from_file(path)["config"]
        )

        try:
            config_d: Dict = json.loads(s_config)
        except Exception as e:
            raise ValueError(
                "\033[91mError in Files_Tools.py:"
                f"\n\tJSON Error in {path}:\n\t\033[93m{e}\033[0m\n"
            )

        return config_d

    def check_args(self) -> None:
        """Check that the configuration file argument is valid.

        Raises:
            PermissionError: If the configuration file cannot be read.
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the argument or the JSON content is invalid.
        """

        self.get_json_as_dict(self.get_configuration_file_path())

    @staticmethod
    def check_pc_resolution(width: int, height: int) -> None:
        """Print an error if the screen resolution is not 1920x1080.

        Args:
            width: The screen width in pixels.
            height: The screen height in pixels.
        """

        if (width, height) != (1920, 1080):
            print(
                "\033[91mError:\n\t\033[94mYour "
                "PC Resolution Must be 1920x1080\033[0m"
            )

    @staticmethod
    def error_raise_message(
        file_name: str, class_name: str, method_name: str, e: Any
    ) -> str:
        """Build a formatted error message.

        Args:
            file_name: The file where the error happened.
            class_name: The class where the error happened.
            method_name: The method where the error happened.
            e: The error to show.

        Returns:
            The formatted error message.
        """

        return (f"\n\033[91mError:\n\t\033[94min file: {file_name}\n\tin"
                f" class: {class_name}\n\tin Method: {method_name}\n\ter"
                f"ror is : {e}\033[0m")

    @staticmethod
    def resolution_error_window(width: int, height: int) -> None:
        """Show an error window if the resolution is not 3840x2160.

        Args:
            width: The screen width in pixels.
            height: The screen height in pixels.

        Raises:
            ValueError: If mlx_init(), mlx_xpm_file_to_image() or
                mlx_new_window() fails.
        """

        if (width, height) == (3840, 2160):
            return

        mlx_obj: Mlx = Mlx()
        init_ptr: Any = mlx_obj.mlx_init()
        if not init_ptr:
            raise ValueError(
                FileTools.error_raise_message(
                    "Files_Tools.py",
                    "FileTools",
                    "resolution_error_window()",
                    "mlx_init() failed",
                )
            )

        SCREEN_WIDTH, SCREEN_HEIGHT = (1254, 1254)

        img_path: str = PacManFilesTools.get_base_path_for_images()\
            + os.sep + "Error" + os.sep + "res_error_img.xpm"

        error_img_ptr, _, _ = mlx_obj.mlx_xpm_file_to_image(
            init_ptr, img_path
        )
        if not error_img_ptr:
            mlx_obj.mlx_release(init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Files_Tools.py",
                    "FileTools",
                    "resolution_error_window()",
                    "res_error_img.xpm failed",
                )
            )

        win_ptr: Any = mlx_obj.mlx_new_window(
            init_ptr,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            "Resolution Error",
        )
        if not win_ptr:
            mlx_obj.mlx_destroy_image(init_ptr, error_img_ptr)
            mlx_obj.mlx_release(init_ptr)
            raise ValueError(
                FileTools.error_raise_message(
                    "Files_Tools.py",
                    "FileTools",
                    "resolution_error_window()",
                    "mlx_new_window() failed",
                )
            )

        mlx_obj.mlx_put_image_to_window(
            init_ptr, win_ptr, error_img_ptr, 0, 0
        )

        def key_hook(keycode: int, none: None) -> None:
            """Handle a key press and update the screen.

            Args:
                keycode: The number of the pressed key.
                none: param sended by mlx key hook.
            """

            if keycode == Keys.ESC:
                exit_loop(None)

        def exit_loop(none: None) -> None:
            """Exit the mlx loop.

            Args:
                none: param sended by mlx key hook.
            """

            mlx_obj.mlx_loop_exit(init_ptr)

        mlx_obj.mlx_hook(win_ptr, 33, 0, exit_loop, None)
        mlx_obj.mlx_key_hook(win_ptr, key_hook, None)

        mlx_obj.mlx_loop(init_ptr)

        mlx_obj.mlx_destroy_window(init_ptr, win_ptr)
        mlx_obj.mlx_destroy_image(init_ptr, error_img_ptr)
        mlx_obj.mlx_release(init_ptr)


class PacManFilesTools(FileTools):
    """Provide the Pac-Man level configuration and highscores tools."""

    def __init__(self) -> None:
        """Initialize the file paths, the configuration and the defaults.

        Raises:
            PermissionError: If the configuration file cannot be read.
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the argument or the configuration file is
                invalid.
        """

        config_file_path: str = self.get_configuration_file_path()

        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            highscores_path: str = (
                str(Path(sys.executable).parent)
                + os.sep + "highscores.json"
            )
        else:
            highscores_path = (
                str(Path(__file__).parent) + os.sep + "highscores.json"
            )

        self.highscores_path: str = highscores_path

        self.config: Dict[str, Any] = self.get_json_as_dict(config_file_path)

        self.level: int = 1
        self.level_up_difference: int = 0
        self.default_data: Dict[str, int] = {
            "lives": 3,
            "points_per_pacgum": 1,
            "points_per_super_pacgum": 5,
            "points_per_ghost": 20,
            "seed": 42,
            "level_max_time": 200,
        }

    def __is_respected_data(self, val: Any) -> bool:
        """Check that a configuration value is valid.

        A valid value is an integer (not a boolean) from 1 to 999.

        Args:
            val: The value to check.

        Returns:
            True if the value is valid, False otherwise.
        """

        if (
            isinstance(val, bool)
            or not isinstance(val, int)
            or 999 < val
            or val <= 0
        ):
            return False

        return True

    def get_current_level_data(self) -> Dict[str, Dict]:
        """Build the data of the current level, then move to the next.

        Increases the default values by the level difference, overrides them
        with the valid values from the configuration file, and prints a
        warning for each missing or invalid key.

        Returns:
            A dictionary mapping ``"level N"`` to the data of that level.
        """

        is_found: Dict[str, bool] = {
            "lives": False,
            "points_per_pacgum": False,
            "points_per_super_pacgum": False,
            "points_per_ghost": False,
            "level_max_time": False
        }

        for name, val in self.default_data.copy().items():
            if name not in ["lives", "seed"]:
                self.default_data[name] = val + self.level_up_difference

        s_level: str = "level " + str(self.level)

        if isinstance(self.config, dict) and s_level in self.config.keys():
            if isinstance(self.config[s_level], dict):
                for key, val in self.config[s_level].items():
                    if (
                        key not in self.default_data.keys()
                        or key == "seed"
                        or not self.__is_respected_data(val)
                    ):
                        continue
                    self.default_data[key] = val
                    is_found[key] = True

        for key_name, founded in is_found.items():
            if not founded:
                print(f"\033[93mWarning in level {self.level}: Invalid"
                      f" '{key_name}'. Default Used \033[0m")
        print()
        self.level += 1
        self.level_up_difference += 10
        level_config: Dict[str, Dict] = {s_level: self.default_data.copy()}
        self.default_data["seed"] = 0
        self.default_data["lives"] = 0

        return level_config

    def add_score_to_highscores_file(self, name: str, score: int
                                     ) -> None:
        """Add a score to the highscores file, sorted from high to low.

        Args:
            name: The name of the player.
            score: The score of the player.
        """

        new_highscores: Dict[str, int] = self.get_highscores_data()
        new_highscores[name] = score
        sorted_highscores: Dict[str, int] = dict(
            sorted(new_highscores.items(), key=lambda items: items[1],
                   reverse=True)
        )

        with open(self.highscores_path, "w") as f:
            json.dump(sorted_highscores, f, indent=4)

    def creat_new_highscores_file_if_not_found(self) -> None:
        """
        Create highscores file in not found else just read it's data.
        """

        try:
            with open(self.highscores_path, "w") as file:
                file.write("{\n}")

        except PermissionError:
            raise PermissionError(
                "\033[91mError in src/Files_Tools.py:"
                "\n\tYou Don't have Permission "
                "To Write in highscores file: \033[94m"
                f"{self.highscores_path}\033[0m"
            )

        except FileNotFoundError:
            raise FileNotFoundError(
                "\033[91mError in src/Files_Tools.py:"
                f"\n\tfile \033[94m'{self.highscores_path}'"
                "\033[91m Not Found\033[0m"
            )

        except Exception as e:
            raise ValueError(
                "\033[91mError in src/Files_Tools.py:"
                f"\n\t{e}"
                "\nAn Error appears in highscores.json"
                " File\033[0m"
            )

    def get_highscores_data(self) -> Dict[str, Any]:
        """Load the highscores file.

        Returns:
            A dictionary mapping each player name to their score,
            sorted from the highsed to the lowest.

        Raises:
            PermissionError: If the highscores file cannot be read.
            FileNotFoundError: If the highscores file does not exist.
            ValueError: If the highscores file is not valid JSON, or score,
            or sore name.
        """

        try:
            highscores_data: Dict[str, Any] = self.get_json_as_dict(
                self.highscores_path)
            if isinstance(highscores_data, list):
                try:
                    highscores_data = highscores_data[0]
                except Exception:
                    raise ValueError(self.error_raise_message(
                        "Files_Tools.py", "PacManFilesTools",
                        "get_highscores_data()", "invalide highscores file"))

            if not isinstance(highscores_data, dict):
                raise ValueError(self.error_raise_message(
                        "Files_Tools.py", "PacManFilesTools",
                        "get_highscores_data()", "invalide highscores file"))

            for score_name, val in highscores_data.items():
                if isinstance(val, bool) or not isinstance(val, int)\
                   or val < 0:
                    raise ValueError(self.error_raise_message(
                        "Files_Tools.py", "PacManFilesTools",
                        "get_highscores_data()", "invalide high score"))
                if len(score_name) > 10 or not score_name:
                    raise ValueError(self.error_raise_message(
                            "Files_Tools.py", "PacManFilesTools",
                            "get_highscores_data()",
                            "invalide name for high score."))
                for c in score_name:
                    if not c.isalnum() and c != " ":
                        raise ValueError(self.error_raise_message(
                            "Files_Tools.py", "PacManFilesTools",
                            "get_highscores_data()",
                            "invalide high score name"))
            highscores_data = dict(
                        sorted(highscores_data.items(),
                               key=lambda items: items[1],
                               reverse=True)
                    )
            with open(self.highscores_path, "w") as f:
                json.dump(highscores_data, f, indent=4)

            return highscores_data
        except FileNotFoundError:
            self.creat_new_highscores_file_if_not_found()
            return self.get_json_as_dict(self.highscores_path)
        except Exception as e:
            raise ValueError(e)

    @staticmethod
    def get_base_path_for_images() -> str:
        """Get the base path for the images.
        Returns:
            base path of the images.
        """
        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            base_path: str = (
                str(Path(sys._MEIPASS))
                + os.sep + "Images" + os.sep
            )
        else:
            base_path = (
                str(Path(__file__).parent.parent) + os.sep + "Images" + os.sep
            )
        return base_path
