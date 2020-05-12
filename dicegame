from abc import ABCMeta, abstractmethod
from random import randint
from typing import List, Type


class Die(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.value = None
        self.sides: int = 0

    @abstractmethod
    def roll(self):
        self.value = randint(1, self.sides)
        return self.value


class D6(Die):
    def __init__(self):
        super().__init__()
        self.sides = 6

    def roll(self):
        return super().roll()


class Cup:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, dice_kind: Type[Die], dice_amount: int):
        self.dice: List[Die] = [dice_kind() for _ in range(dice_amount)]
        self.result = None

    def roll(self):
        self.result = sum([die.roll() for die in self.dice])
        return self.result


class App:
    def __init__(self):
        self.player_name = input('Hello! What is your name?\n> ')
        self.balance = 100
        print('''These are the rules of the dice game:
        * player wages an amount ("wager"), which is deducted from the balance
        * random value ("target") between 1 and 100 (inclusive) is chosen
        * player chooses how many six-sided dice they want to roll
        * dice are rolled, producing a total value ("result")
        ** if result is equal to target, player wins 10x the wager
        ** if result is between target-3 and target-1 (inclusive), player wins 3x wager)
        ** if result is between target-10 and target-4 (inclusive), player wins 2x wager''')

    def gameloop(self):
        _exit = False
        while not _exit:
            if self.balance < 1:
                print('Player has ran out of money. How unfortunate!')
                _exit = True
                continue
            print('\nStarting a new round...')
            wager = input('What amount do you want to wage (type \'quit\' to quit)? > ')
            if wager.lower() == "quit":
                _exit = True
                continue
            if wager.isdigit():
                wager = int(wager)
                self.balance -= wager
            else:
                print('Unrecognized amount!')
                continue
            target = randint(1, 100)
            dice_amount = input(f'The target is {target}. How many dice do you wish to roll?? > ')
            if dice_amount.isdigit():
                dice_amount = int(dice_amount)
            else:
                print('Unrecognized amount!')
                continue
            cup = Cup(D6, dice_amount)
            print('The result is', str(result := cup.roll()) + '.')
            if result == target:
                self.balance += wager * 10
                print(f'Result matches precisely! Player wins {wager * 10}! New balance is {self.balance}.')
            elif 0 < target - result <= 3:
                self.balance += wager * 3
                print(f'Result is within first range! Player wins {wager * 3}! New balance is {self.balance}.')
            elif 0 < target - result <= 10:
                self.balance += wager * 2
                print(f'Result is within second range! Player wins {wager * 2}! New balance is {self.balance}.')
            elif target - result < 0:
                print(f'Player loses... overshoot! New balance is {self.balance}.')
            else:
                print(f'Player loses... not enough. New balance is {self.balance}.')
        print(f'Final balance is {self.balance}. Goodbye!')


if __name__ == '__main__':
    app = App()
    app.gameloop()
