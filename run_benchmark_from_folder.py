from collections import defaultdict
from operator import mod
import os
import sys
import inspect
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
import run_tournament_from_folder

PATH_TO_BOTS = run_tournament_from_folder.PATH_TO_BOTS
OUTPUT_LOCATION = "out"
TIMESTAMP = f'{datetime.now().strftime("%Y%m%d-%H%M%S")}'


def find_bots(subfolder=""):
    bots = defaultdict(lambda: list())
    files = glob.glob(join(PATH_TO_BOTS + subfolder, "**/**", "*.py"))
    is_bot_regex = re.compile(r"(\W*)def(\W*)get_name\(self\)")
    class_name_regex = re.compile(r"class[\W+](\w+):")
    for f in files:
        # with open(f, "r") as file:
        #     match = [is_bot_regex.match(
        #         l) for l in file.readlines() if is_bot_regex.match(l)]
        #     if len(match) == 0:
        #         # This file is not a bot
        #         continue
        if not f.endswith("my_bot_master.py"):
            continue
        # TODO: Check if there is already another bot from this folder.
        try:
            spec = importlib.util.spec_from_file_location(__name__, f)
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
            clazz = next(c for c in inspect.getmembers(
                foo) if "class '__main__." in str(c))
            instance = clazz[-1]()
            table = f.split("/")[-3]
            print(f"Found bot: {instance.get_name()} for table {table}")
            bots[table].append(instance)
        except Exception as ex:
            print(f"Failed to import from file: {f}")
            print(ex)

    return bots

def run_benchmark(bots, run_count):
    # bot_instances = [b.Bot() for b in bots]
    data = [{'name': b.get_name(), 'wins': 0} for b in bots]
    for i in range(run_count):
        res, _ = play_tournament_table(bots, 1000)
        data[res[0]['id']]['wins'] += 1
        print(chr(27) + "[2J")
        print("--- " + str(i+1) + "/" + str(run_count) + " ---")
        [print(d) for d in data]
    return data


def schedule_tournament_and_run(bots, table_index):
    jsondata = run_benchmark(
        bots,
        1000
    )
    print(jsondata)
    # print(jsondata)
    if not os.path.exists(OUTPUT_LOCATION):
        os.mkdir(OUTPUT_LOCATION)
    with open(filename(table_index), "w+") as outfile:
        outfile.write(json.dumps(jsondata))
        print(f"Wrote output to file: {filename(table_index)}")


def filename(table_index):
    return f"{OUTPUT_LOCATION}/run-{TIMESTAMP}-{table_index}.json"


if __name__ == '__main__':
    bots = find_bots()
    for table_number, table_bots in bots.items():
        schedule_tournament_and_run(table_bots, table_number)
