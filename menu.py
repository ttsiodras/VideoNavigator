#!/usr/bin/env python
"""
A simple Pygame-based menu system: it scans folders and collects the single
image/movie pair within each folder. It then shows the collected pictures,
allowing you to navigate with up/down cursors; and when you hit ENTER,
it plays the related movie.

The configuration of folders, resolutions, players, etc is done with a
simple 'settings.ini' file.
"""
import sys
import os
import subprocess
from dataclasses import dataclass
from typing import List, Tuple
# pylint: disable=wrong-import-position
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame  # NOQA


def panic(msg):
    """
    Report error and abort.
    """
    sys.stderr.write('[x] ' + msg + "\n")
    sys.exit(1)


@dataclass
class Settings:
    """
    Store all settings provided by user.
    """
    video_folder: str
    full_screen: bool
    width_in_pixels: int
    height_in_pixels: int
    image_extensions: List[str]
    movie_extensions: List[str]
    command: str


def parse_settings() -> Settings:
    """
    Parse 'settings.ini', return dictionary object with all settings.
    """
    settings = {}
    if not os.path.exists("settings.ini"):
        panic("Missing settings.ini!")
    for idx, line in enumerate(open("settings.ini", "r")):
        if line.startswith('#'):
            continue
        try:
            line = line.strip()
            key, value = line.split('=')
            key = key.strip()
            value = value.strip()
        except ValueError:
            print("[x] Warning! Weird line", idx+1, " ignored:\n\t", line)
        settings[key] = value

    # Validate
    if 'VideoFolder' not in settings:
        panic("Did not find 'VideoFolder=' line in your settings.ini...")

    for param in ['WidthInPixels', 'HeightInPixels']:
        if param in settings:
            try:
                settings[param] = int(settings[param])
            except ValueError:
                panic("Invalid '%s=' line in your settings.ini..." % param)

    # Default values
    settings.setdefault('FullScreen', 'no')
    settings['FullScreen'] = settings['FullScreen'].lower() == 'yes'

    info_object = pygame.display.Info()
    settings.setdefault('WidthInPixels', info_object.current_w)
    settings.setdefault('HeightInPixels', info_object.current_h)

    settings.setdefault(
        'ImageExtensions', "jpg,jpeg,gif,png,webp")
    settings['ImageExtensions'] = settings['ImageExtensions'].split(",")

    settings.setdefault(
        'MovieExtensions', "mkv,mp4,flv,avi,mov")
    settings['MovieExtensions'] = settings['MovieExtensions'].split(",")

    settings.setdefault(
        'Command', r"C:\Program Files\VideoLAN\VLC\vlc.exe")

    return Settings(
        settings['VideoFolder'],
        settings['FullScreen'],
        settings['WidthInPixels'],
        settings['HeightInPixels'],
        settings['ImageExtensions'],
        settings['MovieExtensions'],
        settings['Command'])


def collect_all_videos(settings) -> List[Tuple[str, str]]:
    """
    Scan the folder specified in the settings, and collect
    images and movies.

    Returns list of tuples containing (image,movie) paths.
    """
    results = []
    for root, unused_dirs, files in os.walk(
            settings.video_folder, topdown=True):
        found_images = [
            x for x in files
            if any(
                x.lower().endswith(y)
                for y in settings.image_extensions)
        ]
        found_movies = [
            x for x in files
            if any(
                x.lower().endswith(y)
                for y in settings.movie_extensions)
        ]
        if found_images and found_movies:
            results.append((
                root + os.sep + found_images[0],
                root + os.sep + found_movies[0]))
    return results


def main():
    """
    The heart of the show.
    """
    pygame.init()
    settings = parse_settings()
    args = []
    args.append(
        (settings.width_in_pixels, settings.height_in_pixels))
    if settings.full_screen:
        args.append(pygame.FULLSCREEN)
    win = pygame.display.set_mode(*args)

    images_and_movies = collect_all_videos(settings)
    if not images_and_movies:
        panic("No folders found...")

    current_slot = 0
    image = []
    while True:
        del image
        image = pygame.image.load(images_and_movies[current_slot][0])
        image = pygame.transform.scale(
            image,
            (settings.width_in_pixels, settings.height_in_pixels))

        win.blit(image, (0, 0))
        pygame.display.update()
        while True:
            evt = pygame.event.wait()
            if evt.type == pygame.NOEVENT:
                break
            if evt.type == pygame.KEYUP:
                break

        if evt.key == pygame.K_SPACE or evt.key == pygame.K_RETURN:
            pygame.quit()
            cmd = [settings.command]
            cmd.append(images_and_movies[current_slot][1])
            subprocess.call(cmd)
            pygame.init()
            win = pygame.display.set_mode(
                (settings.width_in_pixels, settings.height_in_pixels),
                pygame.FULLSCREEN)
        elif evt.key == pygame.K_DOWN:
            current_slot = current_slot + 1
            current_slot = current_slot % len(images_and_movies)
        elif evt.key == pygame.K_UP:
            current_slot = current_slot + len(images_and_movies) - 1
            current_slot = current_slot % len(images_and_movies)
        elif evt.key == pygame.K_ESCAPE:
            pygame.quit()
            break


if __name__ == "__main__":
    main()
