import numpy as np
import pyspiel
from bots import randombot, foldBot, callBot
from typing import List, Tuple
from collections import namedtuple

BlindScheduleElement = namedtuple('BlindScheduleElement', 'nextBlindChange smallBlind bigBlind ante')
Player = namedtuple('Player', 'botImpl stack')
 

def playHand(players: List[Player], blinds: List[int]):

    game = pyspiel.load_game("universal_poker", {
        "betting": "nolimit",
        "bettingAbstraction": "fullgame",
        "numPlayers": len(players),
        "stack": " ".join(str(player.stack) for player in players),
        "blind": " ".join(str(blind) for blind in blinds),
        "numRounds": 4,
        "numHoleCards": 2,
        "numBoardCards": "0 3 1 1",
        "numSuits": 4,
        "numRanks": 13,
        "firstPlayer": "3 1 1 1" if len(players) > 2 else "1 1 1 1"
    })
    state = game.new_initial_state()

    while not state.is_terminal():
        if state.is_chance_node():
            state.apply_action(np.random.choice(state.legal_actions()))
            continue
        current_idx = state.current_player()
        action = players[current_idx].botImpl.act(state, state.legal_actions())
        if not action in state.legal_actions():
            if 0 in state.legal_actions():
                action = 0
            else:
                action = 1
        state.apply_action(action)

    return map(int, state.rewards())

def playTournamentTable(bots, startStack: int, blindSchedule: Tuple[BlindScheduleElement]):

    activePlayers = [Player(bot,startStack) for bot in bots]
    np.random.shuffle(activePlayers)

    results = []
    handCount = 0
    blindsIter = iter(blindSchedule)
    currentBlinds = next(blindsIter)
    if currentBlinds.bigBlind > startStack:
        print("bigblind cannot be bigger than startStack")
        return []

    while len(activePlayers) > 1:
        print(sorted([player.botImpl.getName() for player in activePlayers]))

        rewards = playHand(activePlayers, getBlindsInput(currentBlinds, len(activePlayers)))

        if handCount == currentBlinds.nextBlindChange:
            currentBlinds = next(blindsIter)

        defeatedPlayers, activePlayers = updateActivePlayers(activePlayers, rewards, currentBlinds.bigBlind)

        results = results + defeatedPlayers
        activePlayers = activePlayers[1:] + [activePlayers[0]]
        handCount += 1
    
    results = results + [activePlayers[0].botImpl.getName()]
    results.reverse()
    return results

def updateActivePlayers(activePlayers: List[Player], rewards: List[int], bigBlind: int):    
    updatedPlayers = [Player(player.botImpl, int(player.stack+r)) for player,r in zip(activePlayers, rewards)]

    defeatedPlayers = [player.botImpl.getName() for player in updatedPlayers if player.stack < bigBlind]
    activePlayers = [player for player in updatedPlayers if player.stack >= bigBlind]
    return defeatedPlayers, activePlayers

def getBlindsInput(currentBlinds: BlindScheduleElement, playerCount: int) -> List[int]:
    return [currentBlinds.smallBlind, currentBlinds.bigBlind] + ([currentBlinds.ante] * (playerCount-2))

bots = [callBot, callBot, callBot, callBot, callBot]
res = playTournamentTable(bots, 500, [BlindScheduleElement(i, i, 2*i, 0) for i in range(1,100)])
print(res)