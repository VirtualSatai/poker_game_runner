import unittest

from poker_game_runner.state import InfoState

class TestInfoState(unittest.TestCase):

    def setUp(self) -> None:
        self.infoState = InfoState([10, 50, 30, 40], [1000]*2, [5, 10])

    def assertPlayerInfo(self, player_info, spent, stack, active):
        self.assertEqual(player_info.stack, stack)
        self.assertEqual(player_info.spent, spent)
        self.assertEqual(player_info.active, active)

    def assertActionInfo(self, action_info, id, action):
        self.assertEqual(action_info.player, id)
        self.assertEqual(action_info.action, action)

    def test_init(self):
        self.assertEqual(self.infoState.small_blind, 5)
        self.assertEqual(self.infoState.big_blind, 10)
        self.assertListEqual(self.infoState.board_cards, [])
        self.assertEqual(self.infoState.current_round, 0)
        self.assertTupleEqual(self.infoState.history, ([],[],[],[]))
        self.assertTupleEqual(self.infoState.player_hands, (('Ah', '4h'),('Qc', '9h')))
        self.assertPlayerInfo(self.infoState.player_infos[0], 5, 1000-5, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 10, 1000-10, True)

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
        self.assertActionInfo(self.infoState.history[0][0], 0, 1)
        self.assertPlayerInfo(self.infoState.player_infos[0], 10, 1000-10, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 10, 1000-10, True)
        self.infoState.update_info_state_action(1, 50)
        self.assertActionInfo(self.infoState.history[0][1], 1, 50)
        self.assertPlayerInfo(self.infoState.player_infos[0], 10, 1000-10, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)
        self.infoState.update_info_state_action(0, 1)
        self.assertActionInfo(self.infoState.history[0][2], 0, 1)
        self.assertPlayerInfo(self.infoState.player_infos[0], 50, 1000-50, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)

        self.infoState.update_info_state_draw(25)
        self.infoState.update_info_state_draw(29)
        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 100)
        self.assertActionInfo(self.infoState.history[1][0], 0, 100)
        self.assertPlayerInfo(self.infoState.player_infos[0], 100, 1000-100, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 50, 1000-50, True)
        self.infoState.update_info_state_action(1, 1)
        self.assertActionInfo(self.infoState.history[1][1], 1, 1)
        self.assertPlayerInfo(self.infoState.player_infos[0], 100, 1000-100, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 100, 1000-100, True)

        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 150)
        self.assertActionInfo(self.infoState.history[2][0], 0, 150)
        self.assertPlayerInfo(self.infoState.player_infos[0], 150, 1000-150, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 100, 1000-100, True)
        self.infoState.update_info_state_action(1, 1)
        self.assertActionInfo(self.infoState.history[2][1], 1, 1)
        self.assertPlayerInfo(self.infoState.player_infos[0], 150, 1000-150, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, True)

        self.infoState.update_info_state_draw(33)
        self.infoState.update_info_state_action(0, 200)
        self.assertActionInfo(self.infoState.history[3][0], 0, 200)
        self.assertPlayerInfo(self.infoState.player_infos[0], 200, 1000-200, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, True)
        self.infoState.update_info_state_action(1, 0)
        self.assertActionInfo(self.infoState.history[3][1], 1, 0)
        self.assertPlayerInfo(self.infoState.player_infos[0], 200, 1000-200, True)
        self.assertPlayerInfo(self.infoState.player_infos[1], 150, 1000-150, False)
