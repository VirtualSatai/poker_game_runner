import json
from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import example_bot, randombot, foldBot, callBot


bots = [example_bot, example_bot, example_bot, example_bot, example_bot, example_bot, example_bot, example_bot, example_bot, example_bot]
bot_instances = [b.Bot() for b in bots]
#data = [{'name': b.get_name(), 'wins': 0} for b in bot_instances]
#for i in range(20):
#    res, _ = play_tournament_table(bot_instances, 1000)
#    data[res[0]['id']]['wins'] += 1

data, details = play_tournament_table(bot_instances, 1000, console_output=True)
print(len(details))
print(data)




