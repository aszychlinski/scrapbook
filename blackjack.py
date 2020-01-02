from random import shuffle
from typing import Tuple
from time import sleep


SUITS = ['♠', '♣', '♥', '♦']
RANKS = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
        self.value: int = RANKS[rank]

    def __repr__(self):
        return f'{self.rank}{self.suit}'


class Deck:
    def __init__(self):
        self.contents = []
        self.prepare()

    def prepare(self):
        self.contents = []
        for suit in SUITS:
            for rank in RANKS:
                self.contents.append(Card(rank, suit))
        shuffle(self.contents)

    def draw(self):
        try:
            return self.contents.pop(0)
        except IndexError:
            print('Deck ran out! Shuffling...')
            self.prepare()
            return self.contents.pop(0)

    def __getitem__(self, item):
        return self.contents[item]

    def __repr__(self):
        return str(self.contents)


class Hand:
    def __init__(self, card1: Card, card2: Card, hidden: bool = False):
        self.cards = [card1, card2]
        self._value = 0
        self.passed = False
        self.hidden = hidden

    def __repr__(self):
        if self.hidden:
            return str(self.cards[0])
        else:
            return str(self.cards)[1:-1] + f' (value: {str(self.value)})'

    def hit(self, card: Card) -> None:
        self.cards.append(card)

    @property
    def value(self) -> int:
        self._value = sum([card.value for card in self.cards])
        aces_count = len([card for card in self.cards if card.rank == 'A'])
        while self._value > 21 and aces_count:
            self._value -= 10
            aces_count -= 1
        return self._value

    @property
    def alive(self) -> bool:
        if not self.passed:
            return True if self.value < 22 else False
        else:
            return False


class Player:
    def __init__(self, name: str):  # TODO: add money?
        self.name = name
        self.hand = None
        self.score = 0
        self.dealer = False


class Game:
    def __init__(self):
        self.player, self.dealer, self.deck = self.welcome()
        self.mainloop()

    @staticmethod
    def welcome() -> Tuple[Player, Player, Deck]:
        name = input('Hello! What is your name? > ')
        print(f'Welcome, {name}. Let\'s get started.')
        print('The game is played with a single deck of cards, which is shuffled as needed.')
        print('Remember that I am obligated to hit until I reach or surpass a hand value of 17.\n')
        player = Player(name)
        dealer = Player('dealer')
        dealer.dealer = True
        deck = Deck()
        return player, dealer, deck

    def mainloop(self):
        actions = {'h': self.hit, 's': self.stand, 'q': self.quit_}

        while True:
            print('-' * 80)
            self.player.hand = self.deal(hidden=False)
            self.dealer.hand = self.deal(hidden=True)
            self.scoreboard()
            self.reveal_hand(self.dealer.hand, dealer=True)
            self.reveal_hand(self.player.hand, dealer=False)
            while self.player.hand.alive:
                action = self.get_action()
                self.dotdotdot()
                actions[action]()
            print('Now it\'s my turn...')
            self.dotdotdot()
            self.reveal_hand(self.dealer.hand, dealer=True)
            while self.dealer.hand.value < 17:
                self.dotdotdot()
                self.hit(dealer=True)
            if self.dealer.hand.alive:
                self.stand(dealer=True)
            self.determine_outcome()

    def deal(self, hidden: bool) -> Hand:
        return Hand(self.deck.draw(), self.deck.draw(), hidden)

    def scoreboard(self):
        print(f'Hands won: [{self.player.name}: {self.player.score}] - [Dealer: {self.dealer.score}]')

    def reveal_hand(self, hand: Hand, dealer: bool):
        if dealer:
            if self.player.hand.alive:
                print(f'My visible card is {hand}. The other one won\'t be revealed until you stand.')
            else:
                self.dealer.hand.hidden = False
                print(f'\nMy other card was {str(self.dealer.hand.cards[1])}. My current hand is... {hand}')
        else:
            print(f'Your current hand is... {hand}')

    @staticmethod
    def get_action():
        action = input('[H]it - [S]tand - [Q]uit > ').lower()
        while action not in ('h', 's', 'q'):
            print('\nUnrecognized command. Please try again.')
            action = input('[H]it - [S]tand - [Q]uit > ')
        return action

    def hit(self, dealer: bool = False):
        player_pronouns = ['You', 'your']
        dealer_pronouns = ['I', 'my']
        pronouns = dealer_pronouns if dealer else player_pronouns
        hand = self.dealer.hand if dealer else self.player.hand

        draw = self.deck.draw()
        hand.hit(draw) if dealer else hand.hit(draw)
        print(f'\n{pronouns[0]} got a {draw}. Now {pronouns[1]} hand is... {hand}')
        if (hand.value if dealer else hand.value) > 21:
            print('That\'s a bust!\n')

    def stand(self, dealer: bool = False):
        pronoun = 'I' if dealer else '\nYou'
        hand = self.dealer.hand if dealer else self.player.hand
        print(f'{pronoun} stood with a hand value of {hand.value}.\n')
        hand.passed = True

    def determine_outcome(self):
        # I know that in "casino rules" house wins even when both go bust but I felt like changing that here
        pvalue, dvalue = self.player.hand.value, self.dealer.hand.value
        if pvalue > 21 and dvalue > 21 or pvalue == dvalue:
            print('It\'s a draw!')
        elif 22 > pvalue > dvalue or dvalue > 21 >= pvalue:
            print(f'{self.player.name} wins the hand!')
            self.player.score += 1
        elif 22 > dvalue > pvalue or pvalue > 21 >= dvalue:
            print('Dealer wins the hand!')
            self.dealer.score += 1
        else:
            raise RuntimeError('Flow should never enter here!')

    @staticmethod
    def dotdotdot():
        for _ in range(3):
            print('.', end='')
            sleep(1)

    @staticmethod
    def quit_():
        print('See ya!')
        quit()


if __name__ == '__main__':
    Game()
