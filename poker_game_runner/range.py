
from typing import Tuple
from poker_game_runner.state import RANKS, SUITS


class Range:

    def __init__(self, rangeStr: str) -> None:
        self.rangeList = rangeStr.split(", ")
        self.expandedRangeList = []
        for rangeElem in self.rangeList:
            if rangeElem[0] == rangeElem[1] and rangeElem[0] in RANKS: #pair
                if len(rangeElem) == 2: # single combo
                    self.expandedRangeList.append(rangeElem)
                else:
                    startIndex = RANKS.index(rangeElem[0])
                    if len(rangeElem) == 3 and rangeElem[2] == '+': # X and above combo
                        endIndex = 12
                    elif len(rangeElem) == 5 and rangeElem[2] == '-' and rangeElem[3] == rangeElem[4]: # X_low to X_high combo
                        endIndex = RANKS.index(rangeElem[3])
                    else:
                        raise ValueError
                    includedRanks = RANKS[startIndex:endIndex+1]
                    self.expandedRangeList += [rank + rank for rank in includedRanks]
            elif rangeElem[0] in RANKS and rangeElem[1] in RANKS and rangeElem[2] in "os": #non pair
                if len(rangeElem) == 3: #single combo
                    self.expandedRangeList.append(rangeElem)
                else:
                    highCardIndex = RANKS.index(rangeElem[0])
                    startIndex = RANKS.index(rangeElem[1])
                    if len(rangeElem) == 4 and rangeElem[3] == '+':
                        endIndex = highCardIndex - 1
                    elif len(rangeElem) == 7 and rangeElem[3] == '-' and rangeElem[0] == rangeElem[4] and rangeElem[5] in RANKS and rangeElem[6] == rangeElem[2]:
                        endIndex = highCardIndex - 1
                    else:
                        raise ValueError
                    includedRanks = RANKS[startIndex:endIndex+1]
                    self.expandedRangeList += [rangeElem[0] + rank + rangeElem[2] for rank in includedRanks]
            else:
                raise ValueError

    def isHandInRange(self, handCards: Tuple[str]) -> bool:
        if len(handCards) != 2:
            raise ValueError
        for card in handCards:
            if not self.__validateCard(card):
                raise ValueError

        handCardsLst = list(handCards)
        handCardsLst.sort(key=lambda x: RANKS.index(x[0]))
        highCard = handCardsLst[0]
        lowCard = handCardsLst[1]
        handStr = highCard[0] + lowCard[0]

        if highCard[0] != lowCard[0]: #not pair
            if highCard[1] == lowCard[1]: #suited
                handStr += 's'
            else:
                handStr += 'o'
        
        return handStr in self.expandedRangeList

    def __validateCard(self, cardStr):
        if not len(cardStr) == 2 or cardStr[0] not in RANKS or cardStr[1] not in SUITS:
            return False
        else:
            return True