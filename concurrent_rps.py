from random import choice
from time import time
from concurrent.futures import ThreadPoolExecutor


class RPSPlayer:

    figures = ['rock', 'paper', 'scissors']

    def __init__(self, name: str, preference: str):
        self.name = name
        self.score = 0
        self.preference = preference
        self.last_choice = None

    @property
    def pattern(self):
        other_figures = __class__.figures[:]
        other_figures.remove(self.preference)
        return 6 * [self.preference] + 3 * other_figures


def rps(player1: RPSPlayer, player2: RPSPlayer):
    outcomes = (('rock', 'scissors'), ('scissors', 'paper'), ('paper', 'rock'))
    player1.last_choice = choice(player1.pattern)
    player2.last_choice = choice(player2.pattern)
    if player1.last_choice == player2.last_choice:
        print(f'Both players chose {player1.last_choice} - it\'s a draw!')
        return
    if (player1.last_choice, player2.last_choice) in outcomes:
        player1.score += 1
        print(f'{player1.name} won with {player1.last_choice}!')
    else:
        player2.score += 1
        print(f'{player2.name} won with {player2.last_choice}!')


john, jack = RPSPlayer('John', 'rock'), RPSPlayer('Jack', 'paper')

start = time()
with ThreadPoolExecutor(max_workers=10) as executor:
    for _ in range(10000):
        derp = executor.submit(rps, john, jack)
end = time()
phase1 = end - start

start = time()
for _ in range(10000):
    rps(john, jack)
end = time()
phase2 = end - start

print(f'Final score is... {john.name}: {john.score}, {jack.name}: {jack.score}')
print(f'10,000 games using ThreadPoolExecutor took {phase1} seconds.')
print(f'10,000 games using a single loop took {phase2} seconds.')
# turns out that concurrent.futures is needless overhead for such a simple function :)
