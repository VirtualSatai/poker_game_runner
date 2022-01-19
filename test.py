from poker_game_runner.runner import play_tournament_table, BlindScheduleElement
from poker_game_runner.bots import randombot, callBot

play_tournament_table([callBot, callBot, callBot, randombot], 1000, (BlindScheduleElement(-1, 5,10,0),))
