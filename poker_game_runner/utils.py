from enum import IntEnum
from typing import List, Tuple
import eval7

RANKS = '23456789TJQKA'
SUITS = 'cdhs'

class HandType(IntEnum):
    STRAIGHTFLUSH = 1
    FOUROFAKIND = 2
    FULLHOUSE = 3
    FLUSH = 4
    STRAIGHT = 5
    THREEOFAKIND = 6
    TWOPAIR = 7
    PAIR = 8
    HIGHCARD = 9

class Range:
    def __init__(self, rangeStr) -> None:
        self.range = eval7.HandRange(rangeStr)

    def is_hand_in_range(self, handCards: Tuple[str]) -> bool:
        evalHand = tuple(map(eval7.Card, handCards))
        rangeHands = [hand[0] for hand in self.range.hands]
        return evalHand in rangeHands

def get_hand_type(cards: List[str]):
    evalCards = list(map(eval7.Card, cards))
    handTypeStr = eval7.handtype(eval7.evaluate(evalCards))
    return hand_str_to_enum(handTypeStr)

def card_num_to_str(card_num: int):
    rank_num = int(card_num / 4)
    suit_num = card_num % 4
    return RANKS[rank_num] + SUITS[suit_num]

def hand_str_to_enum(handStr: str):
    if handStr.lower == "high card":
        return HandType(9)
    elif handStr.lower == "pair":
        return HandType(8)
    elif handStr.lower == "two pair":
        return HandType(7)
    elif handStr.lower == "three of a kind":
        return HandType(6)
    elif handStr.lower == "straight":
        return HandType(5)
    elif handStr.lower == "flush":
        return HandType(4)
    elif handStr.lower == "full house":
        return HandType(3)
    elif handStr.lower == "four of a kind":
        return HandType(2)
    elif handStr.lower == "straight flush":
        return HandType(1)