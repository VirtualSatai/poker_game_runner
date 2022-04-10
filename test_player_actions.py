import sys
import unittest
from poker_game_runner.bots import testBot
from poker_game_runner.runner import BlindScheduleElement, Player, play_hand, play_tournament_table


class TestPlayerActions(unittest.TestCase):

    def test_raise_too_low(self):
        sb = testBot.Bot([15]) # raise too low -> fold
        bb = testBot.Bot([]) # never acts
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [-5,5])

    def test_raise_too_big(self):
        sb = testBot.Bot([1001]) # raise too high -> fold
        bb = testBot.Bot([]) # never acts
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [-5,5])

    def test_fold_when_check_possible(self):
        sb = testBot.Bot([1, 1, 0]) # call preflop, check-fold flop
        bb = testBot.Bot([0, 50]) # fold not allowed -> check preflop, raise flop. 
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [-10,10])

    def test_negative_action(self):
        sb = testBot.Bot([20, 1, 0]) 
        bb = testBot.Bot([-1, 50]) #illigal -> fold
        
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [10,-10])

    def test_no_action(self):
        sb = testBot.Bot([20, 1, 0]) 
        bb = testBot.Bot([None, 30]) #return nothing -> fold
        
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [10,-10])

    def test_string_action(self):
        sb = testBot.Bot([20, 1, 0])
        bb = testBot.Bot(["allin", 30]) #return string -> fold
         
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [10,-10])

    def test_exception_action(self):
        sb = testBot.Bot([20, 1, 0]) 
        bb = testBot.Bot(["throw", 30]) #throw expection -> fold
        
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [10,-10])

    def test_slow_action(self):
        sb = testBot.Bot([20, 0]) 
        bb = testBot.Bot(["slow"]) #too slow -> fold
        rewards = run_hand([sb, bb])
        self.assertListEqual(rewards, [10,-10])

    def test_slow_bot(self):
        bot1 = testBot.Bot([40, 0]) 
        bot2 = testBot.Bot(["slow", 0]) #too slow -> fold
        res, details = play_tournament_table([bot1, bot2], 70)
        self.assertEqual(len(details), 4)

def run_hand(bots, stacks = [1000, 1000], blinds = [5, 10]):
    players = [Player(bot,stacks[idx], idx) for idx, bot in enumerate(bots)]
    debugging = debugger_is_active()
    rewards, details = play_hand(players, blinds, False if debugging else True)
    return rewards

def debugger_is_active() -> bool:
    """Return if the debugger is currently active"""
    gettrace = getattr(sys, 'gettrace', lambda : None) 
    return gettrace() is not None

if __name__ == "__main__":
    unittest.main()