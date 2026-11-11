"""Manage game sounds and sound effects."""

from typing import Optional, Any, List
from Files_Tools import FileTools
from pathlib import Path
import random
import pygame
import sys
import os


class Sounds:
    """Handle loading and playing all in-game sounds."""

    def __init__(self) -> None:
        """Initialize the Sounds object with default sound lists and state."""
        self.trol_sounds = True
        self.sound_indexes = {
            "ghosts": 0,
            "player": 0,
            "death": 0,
            "super": 0
        }

        self.win_game_sounds: List[str] = ["yeeeeee.mp3",
                                           "His Name is JOHN CENA .mp3"]
        self.start_sounds: List[str] = [
            "salamo-3alikom.mp3", "kiled me kiled you nizar.mp3"]

        self.game_over_sounds: List[str] = [
            "game over 1.mp3", "game_over.mp3", "titanic.mp3"]

        self.super_pacgum_sounds: List[str] = [
            "kiled me kiled you nizar.mp3",
            "tji 3andi ncharbak l9a3wa.mp3",
        ]
        self.player_eat_ghost_sounds: List[str] = [
            "deez nuts.mp3", "Scream.mp3", "Hbet awa Hbet.mp3",
            "why me.mp3", "far.mp3", "duck.mp3",
        ]
        self.ghost_see_player_sounds: List[str] = [
            "stay away from me.mp3", "run don't look back.mp3",
            "they_will_kill_hem.mp3", "j j j .mp3", "run_taher_run.mp3",
        ]
        self.ghost_eat_player_sounds: List[str] = [
            "aaaa.mp3", "be_a_man_alitel.mp3",
            "what mh7ala we live.mp3", "A 7redha.mp3",
            "saad.mp3", "hir skot niba.mp3", "hada_crazy.mp3",
        ]

        self.start_sound_counter: int = 0
        self.movement_sound_counter: int = 0
        self.main__sound: Optional[pygame.mixer.Sound] = None
        self.bomb__sound: Optional[pygame.mixer.Sound] = None
        self.win_or_loss: Optional[pygame.mixer.Sound] = None
        self.intro_sound: Optional[pygame.mixer.Sound] = None
        self.start_sound: Optional[pygame.mixer.Sound] = None
        self.heart_sound: Optional[pygame.mixer.Sound] = None
        self.ghost_sound: Optional[pygame.mixer.Sound] = None
        self.tunnel__sound: Optional[pygame.mixer.Sound] = None
        self.movement_sound: Optional[pygame.mixer.Sound] = None
        self.pacman_death_sound: Optional[pygame.mixer.Sound] = None
        self.super_pacgum_sound: Optional[pygame.mixer.Sound] = None
        self.pacman_eat_ghost_sound: Optional[pygame.mixer.Sound] = None
        self.magneet_or_power_sound: Optional[pygame.mixer.Sound] = None
        self.all_levels_complete_sound: Optional[pygame.mixer.Sound] = None

    def get_songs_dir(self) -> str:
        """Return the path to the songs directory."""
        if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
            return (str(Path(sys._MEIPASS)) + os.sep + "songs")
        return str(Path(__file__).parent.parent) + os.sep + "songs"

    def _load_sound(self, filename: str) -> pygame.mixer.Sound:
        """
        Load and return a pygame Sound object for the given filename.

        Args:
            filename: Name of the sound file to load.

        Returns:
            A loaded pygame Sound object.
        """
        sound_path: str = self.get_songs_dir() + os.sep + filename
        return pygame.mixer.Sound(str(sound_path))

    def init_sounds(self) -> None:
        """Initialize pygame and load all game sounds from disk."""
        try:
            pygame.mixer.init()

            self.bomb__sound = self._load_sound("bomb.mp3")
            self.main__sound = self._load_sound("screens_musec.wav")
            self.intro_sound = self._load_sound("intro.mp3")
            self.start_sound = self._load_sound("pacman_start.wav")
            self.heart_sound = self._load_sound("i'v miss death.mp3")
            self.tunnel__sound = self._load_sound("tunnel_sound.wav")
            self.movement_sound = self._load_sound("pacman_move.wav")
            self.pacman_death_sound = self._load_sound("pacman_death.wav")
            self.magneet_or_power_sound = self._load_sound("i got power.mp3")
            self.pacman_eat_ghost_sound = self._load_sound("tunnel_sound.wav")
            self.all_levels_complete_sound = self._load_sound(
                                                    "all_levels_complete.mp3")

        except Exception as e:
            raise ValueError(FileTools.error_raise_message(
                "Sounds_Effects.py", "Sounds", "init_sounds", e))

    def _is_playing(self, sound: Optional[pygame.mixer.Sound]) -> bool:
        """
        Check if a sound is currently playing.

        Args:
            sound: Sound object to check.

        Returns:
            True if the sound is playing, otherwise False.
        """
        return bool(sound and sound.get_num_channels())

    def _stop_if_playing(self, sound: Optional[pygame.mixer.Sound]) -> None:
        """
        Stop a sound if it is currently playing.

        Args:
            sound: Sound object to stop.
        """
        if sound and self._is_playing(sound):
            sound.stop()

    def next_sound(self, sounds: list, name: str
                   ) -> Optional[pygame.mixer.Sound]:
        """
        Return the next sound in the list and advance the index.

        Args:
            sounds: List of sound filenames.
            name: Name of the sound group.

        Returns:
            The next Sound object, or None if unavailable.
        """
        if not sounds:
            return None
        index: int = self.sound_indexes.get(name, 0)
        sound: pygame.mixer.Sound = self._load_sound(sounds[index])

        self.sound_indexes[name] = (index + 1) % len(sounds)
        return sound

    def set_trol_sounds(self) -> None:
        """Toggle the trol sounds mode on or off."""
        self.trol_sounds = not self.trol_sounds

    def random_Sound(self, sounds: list) -> Optional[pygame.mixer.Sound]:
        """
        Return a randomly chosen sound from the given list.

        Args:
            sounds: List of sound filenames.

        Returns:
            A randomly selected Sound object, or None if unavailable.
        """
        if not sounds:
            return None
        return self._load_sound(random.choice(sounds))

    def is_priority_sound_playing(self) -> bool:
        """Return True if any priority sound is currently playing."""
        sounds_to_check = [
            self.ghost_sound,
            self.start_sound,
            self.pacman_death_sound,
            self.pacman_eat_ghost_sound,
            self.super_pacgum_sound,
            self.win_or_loss,
            self.magneet_or_power_sound,
            self.heart_sound,
            self.bomb__sound
        ]
        return any(self._is_playing(sound) for sound in sounds_to_check)

    def stop_all(self) -> None:
        """Stop all priority sounds that are currently playing."""
        sounds_to_check = [
            self.ghost_sound,
            self.start_sound,
            self.pacman_death_sound,
            self.pacman_eat_ghost_sound,
            self.super_pacgum_sound,
            self.win_or_loss,
            self.magneet_or_power_sound,
            self.heart_sound
        ]
        for sound in sounds_to_check:
            self._stop_if_playing(sound)

    def pacman_eat_ghost__sound(self) -> None:
        """Play the sound for Pac-Man eating a ghost."""
        if not self.trol_sounds:
            if self.pacman_eat_ghost_sound:
                self.pacman_eat_ghost_sound.play()
        elif not self._is_playing(self.pacman_eat_ghost_sound):
            self.stop_all()
            self.pacman_eat_ghost_sound = self.next_sound(
                self.player_eat_ghost_sounds, "player")
            if self.pacman_eat_ghost_sound:
                self.pacman_eat_ghost_sound.play()

    def play_pacman_death_sound(self) -> None:
        """Play the sound for Pac-Man's death and wait for it to finish."""
        if not self.trol_sounds:
            if self.pacman_death_sound:
                self.pacman_death_sound.play()
        else:
            self.stop_all()
            self.pacman_death_sound = self.next_sound(
                self.ghost_eat_player_sounds, "death")
            if self.pacman_death_sound:
                self.pacman_death_sound.play()

        if self.pacman_death_sound:
            pygame.time.wait(int(self.pacman_death_sound.get_length() * 1000))

    def play_start_sound(self, current_game: Any) -> None:
        """Play the game start sound once at the beginning of the game."""
        if self.start_sound_counter == 0:
            if self.trol_sounds:
                self.start_sound = self.random_Sound(self.start_sounds)

            if self.start_sound:
                self.stop_all()
                self.start_sound.play()
                current_game.start_time += self.start_sound.get_length()
            self.start_sound_counter = 1

    def play_movement_sound(self) -> None:
        """
        Play the movement sound every 35 frames if no priority soundisactive.
        """
        if self.movement_sound_counter >= 35:
            if (not self.is_priority_sound_playing() and self.movement_sound):
                self.movement_sound.play()
                self.movement_sound_counter = 0
        else:
            self.movement_sound_counter += 1

    def play_or_stop_intro_sound(self, sound: str) -> None:
        """Play or stop the intro sound.

        Args:
            sound: Action to perform, either "play" or "stop".
        """
        if sound == "play" and self.intro_sound:
            self.intro_sound.play()

        if sound == "stop" and self.intro_sound:
            self.intro_sound.stop()

    def ghost_trol_sound(self) -> None:
        """Play the next ghost trol sound if no priority sound is active."""
        if self.is_priority_sound_playing():
            return

        self.ghost_sound = self.next_sound(
            self.ghost_see_player_sounds, "ghosts")

        if self.ghost_sound:
            self.ghost_sound.play()

    def tunnel_sound(self) -> None:
        """Play the tunnel sound effect."""
        if self.tunnel__sound:
            self.tunnel__sound.play()

    def eat_super_pacgum_sound(self) -> None:
        """Play the super pac-gum eating sound if conditions allow."""
        if not self.is_priority_sound_playing() and self.trol_sounds:
            self.super_pacgum_sound = self.next_sound(
                self.super_pacgum_sounds, "super")

            if self.super_pacgum_sound:
                self.super_pacgum_sound.play()

    def eat_heart_sound(self) -> None:
        """Play the heart pickup sound if trol sounds are on
        and no priority sound is active."""
        if (self.trol_sounds and self.heart_sound
                and not self.is_priority_sound_playing()):
            self.heart_sound.play()

    def eat_magneet_or_power_sound(self) -> None:
        """Play the magnet or power pickup sound if conditions allow."""
        if (self.trol_sounds and self.magneet_or_power_sound
                and not self.is_priority_sound_playing()):
            self.magneet_or_power_sound.play()

    def win_or_loss_sound(self, sound: str) -> None:
        """Play a random win or game-over sound based on the given outcome.

        Args:
            sound: Either "win", "over", or any other value to stop the sound.
        """
        if sound == "win":
            self.win_or_loss = self.random_Sound(self.win_game_sounds)
        elif sound == "over":
            self.win_or_loss = self.random_Sound(self.game_over_sounds)
        else:
            if self.win_or_loss:
                self.win_or_loss.stop()
            return
        if self.win_or_loss:
            self.win_or_loss.play()

    def play_or_stop_main_sound(self, sound: str) -> None:
        """Stop or play the main background sound.

        Args:
            sound:Pass "stop" to stop the sound, or any other value to play it.
        """
        if sound == "stop":
            if self.main__sound:
                self.main__sound.stop()

        elif not self._is_playing(self.main__sound):
            if self.main__sound:
                self.main__sound.play()

    def bomb_sound(self) -> None:
        """Play the bomb sound and wait until it finishes"""
        if self.bomb__sound:
            self.bomb__sound.play()
