from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot, callBot, testBot
import json

res, json_data = play_tournament_table([callBot, callBot, randombot, randombot], 1000, (BlindScheduleElement(-1, 5,10,0),))
json_str = json.dumps(json_data)
print(res)
