import json
from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot, fbl_bot, foldBot, callBot


bots = [fbl_bot, foldBot, fbl_bot, fbl_bot, fbl_bot, callBot, randombot, foldBot, randombot, randombot]
bot_instances = [b.Bot() for b in bots]
#data = [{'name': b.get_name(), 'wins': 0} for b in bot_instances]
#for i in range(20):
#    res, _ = play_tournament_table(bot_instances, 1000)
#    data[res[0]['id']]['wins'] += 1

res, details = play_tournament_table(bot_instances, 1000)
print(res)

with open('output.json', 'w') as file:
    json.dump(details, file)



