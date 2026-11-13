"""Provide the entry point of the Pac-Man game."""

from Start_Game_screen import StartGameScreen
from Instructions_screen import InstructionsScreen
from High_scoore_list_screen import HighscoreListScreen
from Video_Screens import VideoScreen
from Files_Tools import FileTools, E_MainMenuOptions
from Main_menu_screen import MainMenuScreen
from Sounds_Effects import Sounds
import sys


def main() -> None:
    """Run the game and manage the navigation between the screens.

    Clears the highscores file, shows the intro video, then loops
    between the main menu, the game, the highscores and the
    instructions screens until the player chooses to exit. Any
    exception is caught and printed.
    """

    try:

        VideoScreen().show_video_screen()
        sound: Sounds = Sounds()
        sound.init_sounds()

        screen: int = E_MainMenuOptions.MAIN_MENU_SCREEN
        LEVELS: int = 1

        while screen != E_MainMenuOptions.EXIT:

            if screen == E_MainMenuOptions.MAIN_MENU_SCREEN:

                sound.play_or_stop_main_sound("play")
                screen = MainMenuScreen().show_main_menu_screen()

            elif screen == E_MainMenuOptions.START_GAME_SCREEN:

                sound.play_or_stop_main_sound("stop")
                StartGameScreen(LEVELS).show_game_play_screen()
                screen = E_MainMenuOptions.MAIN_MENU_SCREEN

            elif screen == E_MainMenuOptions.HIGH_SCORES_SCREEN:

                sound.play_or_stop_main_sound("play")
                HighscoreListScreen().show_highscores_screen()
                screen = E_MainMenuOptions.MAIN_MENU_SCREEN

            elif screen == E_MainMenuOptions.INSTRUCTIONS_SCREEN:

                sound.play_or_stop_main_sound("play")
                InstructionsScreen().show_instructions_screen()
                screen = E_MainMenuOptions.MAIN_MENU_SCREEN

    except Exception as e:
        print(
            FileTools.error_raise_message(
                "pac-man.py",
                "None",
                "main()",
                "Unexpected error in main()",
            )
        )
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
