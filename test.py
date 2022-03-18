from poker_game_runner.runner import play_tournament_table, BlindScheduleElement, Player, play_hand
from poker_game_runner.bots import randombot, callBot, testBot
import json

test_bot_1 = testBot.Bot([15])
test_bot_2 = testBot.Bot([0])
stacks = [1000, 1000]
blinds = [5, 10]

bots = [test_bot_1, test_bot_2]
players = [Player(bot,stacks[idx], idx) for idx, bot in enumerate(bots)]

rewards, json_hand_events = play_hand(players, blinds)

print(list(rewards))
