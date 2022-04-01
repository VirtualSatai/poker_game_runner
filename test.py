from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot, bovlebot


bots = [bovlebot, bovlebot, randombot, randombot, bovlebot, bovlebot, randombot, randombot, bovlebot, bovlebot]
bot_instances = [b.Bot() for b in bots]

res, details = play_tournament_table(bot_instances, 1000, tuple(BlindScheduleElement(i*20, i*5,i*10,0) for i in range(1,100)) +
                                                           (BlindScheduleElement(-1, 500,1000,0), ), use_timeout=False)
print(res)
print(len(details))