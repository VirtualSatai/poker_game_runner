import unittest
from poker_game_runner.state import ActionInfo, InfoState, Observation, PlayerInfo
from poker_game_runner.utils import HandType

def assertPlayerInfo(player_info, spent, stack, active):
        assert player_info.stack == stack
        assert player_info.spent == spent
        assert player_info.active == active

def assertActionInfo(action_info, id, action):
    assert action_info.player == id
    assert action_info.action == action

class testObservation(unittest.TestCase):

    def setUp(self) -> None:
        self.infoStateHeadsup = InfoState([10, 50, 30, 40], [1000]*2, [5, 10])
        self.infoState3way = InfoState([10, 50, 30, 40, 20, 24], [1000]*3, [5, 10, 0])
        

    def test_init_headsup(self):
        obs = self.infoStateHeadsup.to_observation(0, [0,1] + [i for i in range(20, 1001-5)])
        self.assertTupleEqual(obs.my_hand, ('Ah', '4h'))
        self.assertEqual(obs.my_index, 0)
        self.assertTupleEqual(obs.board_cards, tuple())
        self.assertEqual(len(obs.player_infos), 2)
        assertPlayerInfo(obs.player_infos[0], 5, 1000-5, True)
        assertPlayerInfo(obs.player_infos[1], 10, 1000-10, True)
        self.assertTupleEqual(obs.history, (tuple(),tuple(),tuple(),tuple()))
        self.assertEqual(obs.small_blind, 5)
        self.assertEqual(obs.big_blind, 10)
        self.assertEqual(obs.current_round, 0)
        self.assertTupleEqual(obs.legal_actions, tuple([0,1] + [i for i in range(20, 1001-5)]))
    
    def test_init_3way(self):
        obs = self.infoState3way.to_observation(2, [0,1] + [i for i in range(20, 1001-5)])
        self.assertTupleEqual(obs.my_hand, ('8c', '7c'))
        self.assertEqual(obs.my_index, 2)
        self.assertTupleEqual(obs.board_cards, tuple())
        self.assertEqual(len(obs.player_infos), 3)
        assertPlayerInfo(obs.player_infos[0], 5, 1000-5, True)
        assertPlayerInfo(obs.player_infos[1], 10, 1000-10, True)
        assertPlayerInfo(obs.player_infos[2], 0, 1000, True)
        self.assertTupleEqual(obs.history, (tuple(),tuple(),tuple(),tuple()))
        self.assertEqual(obs.small_blind, 5)
        self.assertEqual(obs.big_blind, 10)
        self.assertEqual(obs.current_round, 0)
        self.assertTupleEqual(obs.legal_actions, tuple([0,1] + [i for i in range(20, 1001-5)]))

    def test_action_str(self):
        obs = self.infoStateHeadsup.to_observation(0, [0,1] + [i for i in range(20, 1001-5)])

        action_str = obs.action_to_str(300)
        self.assertEqual(action_str, "Player 0: Raise to 300")
        action_str = obs.action_to_str(1)
        self.assertEqual(action_str, "Player 0: Call")
        action_str = obs.action_to_str(0)
        self.assertEqual(action_str, "Player 0: Fold")

        action_str = obs.action_to_str(300, 1)
        self.assertEqual(action_str, "Player 1: Raise to 300")
        action_str = obs.action_to_str(1, 1)
        self.assertEqual(action_str, "Player 1: Call")
        action_str = obs.action_to_str(0, 1)
        self.assertEqual(action_str, "Player 1: Fold")

    def test_methods_headsup(self):
        obs = self.infoStateHeadsup.to_observation(0, [0,1] + [i for i in range(20, 1001-5)])

        self.assertTrue(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 20)
        self.assertEqual(obs.get_max_raise(), 1000-5)
        self.assertEqual(obs.get_max_spent(), 10)
        self.assertEqual(obs.get_call_size(), 5)
        self.assertEqual(obs.get_pot_size(), 15)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 20)
        self.assertEqual(obs.get_fraction_pot_raise(1), 30)
        self.assertEqual(obs.get_fraction_pot_raise(2), 50)

        self.assertEqual(obs.get_player_count(),2)
        self.assertEqual(len(obs.get_active_players()), 2)
        assertPlayerInfo(obs.get_active_players()[0], 5, 1000-5, True)
        assertPlayerInfo(obs.get_active_players()[1], 10, 1000-10, True)

        self.assertTupleEqual(obs.get_actions_this_round(), tuple())
        self.assertTupleEqual(obs.get_actions_in_round(1), tuple())

        self.infoStateHeadsup.update_info_state_action(0, 1)
        self.infoStateHeadsup.update_info_state_action(1, 50)
        obs = self.infoStateHeadsup.to_observation(0, [0,1] + [i for i in range(90, 1001-5)])

        self.assertTrue(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 90)
        self.assertEqual(obs.get_max_raise(), 1000-5)
        self.assertEqual(obs.get_max_spent(), 50)
        self.assertEqual(obs.get_call_size(), 40)
        self.assertEqual(obs.get_pot_size(), 60)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 100)
        self.assertEqual(obs.get_fraction_pot_raise(1), 150)
        self.assertEqual(obs.get_fraction_pot_raise(2), 250)
        assertActionInfo(obs.get_actions_this_round()[0], 0, 1)
        assertActionInfo(obs.get_actions_this_round()[1], 1,50)

        self.infoStateHeadsup.update_info_state_action(0, 100)
        self.infoStateHeadsup.update_info_state_action(1, 1000)
        obs = self.infoStateHeadsup.to_observation(0, [0,1])

        self.assertFalse(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 1)
        self.assertEqual(obs.get_max_raise(), 1)
        self.assertEqual(obs.get_max_spent(), 1000)
        self.assertEqual(obs.get_call_size(), 900)
        self.assertEqual(obs.get_pot_size(), 1100)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 1)
        self.assertEqual(obs.get_fraction_pot_raise(1), 1)
        self.assertEqual(obs.get_fraction_pot_raise(2), 1)
        assertActionInfo(obs.get_actions_this_round()[2], 0, 100)
        assertActionInfo(obs.get_actions_this_round()[3], 1, 1000)

    def test_methods_3way(self):
        obs = self.infoState3way.to_observation(2, [0,1] + [i for i in range(20, 1001-5)])

        self.assertTrue(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 20)
        self.assertEqual(obs.get_max_raise(), 1000-5)
        self.assertEqual(obs.get_max_spent(), 10)
        self.assertEqual(obs.get_call_size(), 10)
        self.assertEqual(obs.get_pot_size(), 15)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 22)
        self.assertEqual(obs.get_fraction_pot_raise(1), 35)
        self.assertEqual(obs.get_fraction_pot_raise(2), 60)

        self.assertEqual(obs.get_player_count(),3)
        self.assertEqual(len(obs.get_active_players()), 3)
        assertPlayerInfo(obs.get_active_players()[0], 5, 1000-5, True)
        assertPlayerInfo(obs.get_active_players()[1], 10, 1000-10, True)
        assertPlayerInfo(obs.get_active_players()[2], 0, 1000, True)

        self.assertTupleEqual(obs.get_actions_this_round(), tuple())
        self.assertTupleEqual(obs.get_actions_in_round(1), tuple())

        self.infoState3way.update_info_state_action(2, 50)
        obs = self.infoState3way.to_observation(0, [0,1] + [i for i in range(90, 1001-5)])

        self.assertTrue(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 90)
        self.assertEqual(obs.get_max_raise(), 1000-5)
        self.assertEqual(obs.get_max_spent(), 50)
        self.assertEqual(obs.get_call_size(), 45)
        self.assertEqual(obs.get_pot_size(), 65)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 105) # 50 + 110*0.5
        self.assertEqual(obs.get_fraction_pot_raise(1), 160) # 50 + 110*1
        self.assertEqual(obs.get_fraction_pot_raise(2), 270) # 50 + 110*2
        assertActionInfo(obs.get_actions_this_round()[0], 2, 50)

        self.infoState3way.update_info_state_action(0, 0)
        self.infoState3way.update_info_state_action(1, 1000)
        obs = self.infoState3way.to_observation(2, [0,1])

        self.assertFalse(obs.can_raise())
        self.assertEqual(obs.get_min_raise(), 1)
        self.assertEqual(obs.get_max_raise(), 1)
        self.assertEqual(obs.get_max_spent(), 1000)
        self.assertEqual(obs.get_call_size(), 950)
        self.assertEqual(obs.get_pot_size(), 1055)
        self.assertEqual(obs.get_fraction_pot_raise(0.5), 1) 
        self.assertEqual(obs.get_fraction_pot_raise(1), 1) 
        self.assertEqual(obs.get_fraction_pot_raise(2), 1) 
        assertActionInfo(obs.get_actions_this_round()[1], 0, 0)
        assertActionInfo(obs.get_actions_this_round()[2], 1, 1000)
        self.assertEqual(obs.get_player_count(),3)
        self.assertEqual(len(obs.get_active_players()), 2)
        assertPlayerInfo(obs.get_active_players()[0], 1000, 0, True)
        assertPlayerInfo(obs.get_active_players()[1], 50, 1000-50, True)

    def test_hand_type(self):
        obs = self.infoState3way.to_observation(2, [0,1] + [i for i in range(20, 1001-5)])

        self.assertEqual(obs.get_my_hand_type(), HandType.HIGHCARD)
        self.assertEqual(obs.get_board_hand_type(), HandType.HIGHCARD)

        self.infoState3way.update_info_state_draw(21)
        self.infoState3way.update_info_state_draw(22)
        self.infoState3way.update_info_state_draw(29)

        obs = self.infoState3way.to_observation(2, [0,1] + [i for i in range(20, 1001-5)])

        self.assertEqual(obs.get_my_hand_type(), HandType.THREEOFAKIND)
        self.assertEqual(obs.get_board_hand_type(), HandType.PAIR)

        self.infoState3way.update_info_state_draw(26)

        obs = self.infoState3way.to_observation(2, [0,1] + [i for i in range(20, 1001-5)])

        self.assertEqual(obs.get_my_hand_type(), HandType.FULLHOUSE)
        self.assertEqual(obs.get_board_hand_type(), HandType.PAIR)

class TestInfoState(unittest.TestCase):

    def setUp(self) -> None:
        self.infoState = InfoState([10, 50, 30, 40], [1000]*2, [5, 10])

    def test_init(self):
        self.assertEqual(self.infoState.small_blind, 5)
        self.assertEqual(self.infoState.big_blind, 10)
        self.assertListEqual(self.infoState.board_cards, [])
        self.assertEqual(self.infoState.current_round, 0)
        self.assertTupleEqual(self.infoState.history, ([],[],[],[]))
        self.assertTupleEqual(self.infoState.player_hands, (('Ah', '4h'),('Qc', '9h')))
        assertPlayerInfo(self.infoState.player_infos[0], 5, 1000-5, True)
        assertPlayerInfo(self.infoState.player_infos[1], 10, 1000-10, True)

    def test_draw(self):
        self.infoState.update_info_state_draw(25)
        self.infoState.update_info_state_draw(29)
        self.infoState.update_info_state_draw(33)
        self.assertListEqual(self.infoState.board_cards, ['8d', '9d', 'Td'])
        self.assertEqual(self.infoState.current_round, 1)
        self.infoState.update_info_state_draw(37)
        self.assertListEqual(self.infoState.board_cards, ['8d', '9d', 'Td', 'Jd'])
        self.assertEqual(self.infoState.current_round, 2)
        self.infoState.update_info_state_draw(41)
        self.assertListEqual(self.infoState.board_cards, ['8d', '9d', 'Td', 'Jd', 'Qd'])
        self.assertEqual(self.infoState.current_round, 3)

    def test_action(self):
        self.infoState.update_info_state_action(0, 1)
        assertActionInfo(self.infoState.history[0][0], 0, 1)
        assertPlayerInfo(self.infoState.player_infos[0], 10, 1000-10, True)
        assertPlayerInfo(self.infoState.player_infos[1], 10, 1000-10, True)
        self.infoState.update_info_state_action(1, 50)
        assertActionInfo(self.infoState.history[0][1], 1, 50)
        assertPlayerInfo(self.infoState.player_infos[0], 10, 1000-10, True)
        assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)
        self.infoState.update_info_state_action(0, 1)
        assertActionInfo(self.infoState.history[0][2], 0, 1)
        assertPlayerInfo(self.infoState.player_infos[0], 50, 1000-50, True)
        assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)

        self.infoState.update_info_state_draw(25)
        self.infoState.update_info_state_draw(29)
        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 100)
        assertActionInfo(self.infoState.history[1][0], 0, 100)
        assertPlayerInfo(self.infoState.player_infos[0], 100, 1000-100, True)
        assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)
        self.infoState.update_info_state_action(1, 1)
        assertActionInfo(self.infoState.history[1][1], 1, 1)
        assertPlayerInfo(self.infoState.player_infos[0], 100, 1000-100, True)
        assertPlayerInfo(self.infoState.player_infos[1], 100, 1000-100, True)

        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 150)
        assertActionInfo(self.infoState.history[2][0], 0, 150)
        assertPlayerInfo(self.infoState.player_infos[0], 150, 1000-150, True)
        assertPlayerInfo(self.infoState.player_infos[1], 100, 1000-100, True)
        self.infoState.update_info_state_action(1, 1)
        assertActionInfo(self.infoState.history[2][1], 1, 1)
        assertPlayerInfo(self.infoState.player_infos[0], 150, 1000-150, True)
        assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, True)

        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 200)
        assertActionInfo(self.infoState.history[3][0], 0, 200)
        assertPlayerInfo(self.infoState.player_infos[0], 200, 1000-200, True)
        assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, True)
        self.infoState.update_info_state_action(1, 0)
        assertActionInfo(self.infoState.history[3][1], 1, 0)
        assertPlayerInfo(self.infoState.player_infos[0], 200, 1000-200, True)
        assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, False)
