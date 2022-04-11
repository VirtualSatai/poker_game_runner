import json
from poker_game_runner.runner import play_tournament_table, BlindScheduleElement, Player, play_hand
from poker_game_runner.state import Observation
import glob
from datetime import datetime
from os import makedirs, sep
from os.path import dirname, exists, join
from time import sleep
import importlib
import re
import importlib.util

PATH_TO_BOTS = "/mnt/c/Git/poker_game_visualizer/poker-tournament-server/bots/20220409-102136"


def find_bots():
    bots = []
    files = glob.glob(join(PATH_TO_BOTS, "**/", "*.py"))
    is_bot_regex = re.compile(r"(\W*)def(\W*)get_name\(self\)")
    for f in files:
        with open(f, "r") as file:
            match = [is_bot_regex.match(
                l) for l in file.readlines() if is_bot_regex.match(l)]
            if len(match) == 0:
                # This file is not a bot
                continue
        # f.split("/")[-2]
        try:
            spec = importlib.util.spec_from_file_location(__name__, f)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            name = foo.get_name()
            print(f"Found bot: {name}")
            bots.append(foo)
        except Exception as ex:
            print(f"Failed to import from file: {f}")
            print(ex)

    return bots


def schedule_tournament_and_run(bots):
    results, jsondata = play_tournament_table(
        bots,
        1000,
        (BlindScheduleElement(10, 5, 10, 0), BlindScheduleElement(-1, 10, 20, 0))
    )
    print(results)
    print(jsondata)


if __name__ == '__main__':
    bots = find_bots()
    schedule_tournament_and_run(bots)
