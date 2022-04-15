from poker_game_runner.utils import get_hand_type, HandType, Range
import unittest

class TestRange(unittest.TestCase):

    def test_error(self):
        try:
            r = Range("K1s+")
            self.fail()
        except:
            self.assertTrue(True)

    def test_range_suited_above(self):
        r = Range("K3s+")
        self.assertTrue(r.is_hand_in_range(("3d", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Qs")))
        self.assertFalse(r.is_hand_in_range(("Ks", "As")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2s")))
        self.assertFalse(r.is_hand_in_range(("Ks", "4c")))
        self.assertFalse(r.is_hand_in_range(("Ts", "Td")))
    
    def test_range_suited_between(self):
        r = Range("K3s-KJs")
        self.assertTrue(r.is_hand_in_range(("3d", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Js")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Qs")))
        self.assertFalse(r.is_hand_in_range(("Ks", "As")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2s")))
        self.assertFalse(r.is_hand_in_range(("Ks", "4c")))
        self.assertFalse(r.is_hand_in_range(("Ts", "Td")))

    def test_range_offsuited_above(self):
        r = Range("K3o+")
        self.assertTrue(r.is_hand_in_range(("3s", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Qd")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Ad")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2c")))
        self.assertFalse(r.is_hand_in_range(("Ks", "4s")))
        self.assertFalse(r.is_hand_in_range(("Ts", "Td")))

    def test_range_offsuited_between(self):
        r = Range("K3o-KJo")
        self.assertTrue(r.is_hand_in_range(("3s", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Jd")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Qd")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Ad")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2c")))
        self.assertFalse(r.is_hand_in_range(("Ks", "4s")))
        self.assertFalse(r.is_hand_in_range(("Ts", "Td")))

    def test_range_pair_above(self):
        r = Range("JJ+")
        self.assertTrue(r.is_hand_in_range(("Ks", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Js", "Jd")))
        self.assertFalse(r.is_hand_in_range(("Ts", "Td")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2s")))

    def test_range_pair_between(self):
        r = Range("99-KK")
        self.assertTrue(r.is_hand_in_range(("Ks", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Js", "Jd")))
        self.assertFalse(r.is_hand_in_range(("As", "Ad")))
        self.assertFalse(r.is_hand_in_range(("8s", "8d")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2s")))

    def test_composite(self):
        r = Range("99-KK, K3o-KJo, K3s-KJs")

        self.assertTrue(r.is_hand_in_range(("3d", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Js")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Qs")))
        self.assertFalse(r.is_hand_in_range(("Ks", "As")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2s")))

        self.assertTrue(r.is_hand_in_range(("3s", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Ks", "Jd")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Qd")))
        self.assertFalse(r.is_hand_in_range(("Ks", "Ad")))
        self.assertFalse(r.is_hand_in_range(("Ks", "2c")))

        self.assertTrue(r.is_hand_in_range(("Ks", "Kd")))
        self.assertTrue(r.is_hand_in_range(("Js", "Jd")))
        self.assertFalse(r.is_hand_in_range(("As", "Ad")))
        self.assertFalse(r.is_hand_in_range(("8s", "8d")))

    

class TestHandType(unittest.TestCase):

    def test_error(self):
        try:
            hand_type = get_hand_type(["As", "As", "6h", "6h", "Ks"])
            self.fail()
        except:
            self.assertTrue(True)

    def test_no_cards(self):
        self.assertEqual(get_hand_type([]), HandType.HIGHCARD)

    def test_high_card(self):
        self.assertEqual(get_hand_type(["Ah", "3d", "6s", "Jc", "Ks"]), HandType.HIGHCARD)

    def test_pair(self):
        self.assertEqual(get_hand_type(["Ah", "Ad", "6s", "Jc", "Ks"]), HandType.PAIR)

    def test_two_pair(self):
        self.assertEqual(get_hand_type(["Ah", "Ad", "6s", "6c", "Ks"]), HandType.TWOPAIR)

    def test_three_of_a_kind(self):
        self.assertEqual(get_hand_type(["Ah", "Ad", "As", "6c", "Ks"]), HandType.THREEOFAKIND)
    
    def test_straight_low(self):
        self.assertEqual(get_hand_type(["Ah", "2d", "3s", "4c", "5s"]), HandType.STRAIGHT)

    def test_straight_high(self):
        self.assertEqual(get_hand_type(["Ah", "Kd", "Qs", "Jc", "Ts"]), HandType.STRAIGHT)

    def test_flush(self):
        self.assertEqual(get_hand_type(["Ah", "Kh", "Qh", "Jh", "9h"]), HandType.FLUSH)

    def test_full_house(self):
        self.assertEqual(get_hand_type(["Ah", "Ad", "As", "Tc", "Ts"]), HandType.FULLHOUSE)

    def test_four_of_a_kind(self):
        self.assertEqual(get_hand_type(["Ah", "Ad", "As", "Ac", "Ts"]), HandType.FOUROFAKIND)

    def test_straight_flush(self):
        self.assertEqual(get_hand_type(["Ah", "Kh", "Qh", "Jh", "Th"]), HandType.STRAIGHTFLUSH)