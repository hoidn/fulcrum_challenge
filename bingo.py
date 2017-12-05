import pdb
from functools import reduce
import random


afunc = lambda a, b: a and b
ofunc = lambda a, b: a or b


def get_rows(arr):
    return [arr[3 * i: 3 * i + 3] for i in range(3)]

def get_cols(arr):
    return list(map(list, list(zip(*get_rows(arr)))))
 
def get_diags(arr):
    down = [arr[i * 3 + i] for i in range(3)]
    up = [arr[6 - 3 * i + i] for i in range(3)]
    return [down, up]

class Board:
    def __init__(self, arr):
        self.arr = arr
        self.status = [0 for _ in range(9)]

    def check_rows(self):
        return reduce(ofunc,
            [reduce(afunc, col) for col in get_rows(self.status)])

    def check_cols(self):
        return reduce(ofunc,
            [reduce(afunc, col) for col in get_cols(self.status)])

    def check_diags(self):
        return reduce(ofunc,
            [reduce(afunc, col) for col in get_diags(self.status)])

    def is_won(self):
        return reduce(ofunc, [self.check_rows(),
            self.check_cols(), self.check_diags()])

    def move(self):
        lst = list(range(1, 7))
        val = random.choice(lst) + random.choice(lst)
        arr = [v1 * (1 - v2) for v1, v2 in zip(self.arr, self.status)]
        hits = indices(arr, val)
        if hits:
            #pdb.set_trace()
            i = random.choice(hits)
            self.status[i] = 1
        return self.is_won()


def divisors(n):
    # get factors and their counts
    factors = {}
    nn = n
    i = 2
    while i*i <= nn:
        while nn % i == 0:
            if not i in factors:
                factors[i] = 0
            factors[i] += 1
            nn //= i
        i += 1
    if nn > 1:
        factors[nn] = 1

    primes = list(factors.keys())

    # generates factors from primes[k:] subset
    def generate(k):
        if k == len(primes):
            yield 1
        else:
            rest = generate(k+1)
            prime = primes[k]
            for factor in rest:
                prime_to_i = 1
                # prime_to_i iterates prime**i values, i being all possible exponents
                for _ in range(factors[prime] + 1):
                    yield factor * prime_to_i
                    prime_to_i *= prime

    # in python3, `yield from generate(0)` would also work
    for factor in generate(0):
        yield factor

def valid_divisors(n):
    if n <= 12:
        return list(divisors(n))[1:]
    else:
        return list(divisors(n))[1:-1]

def roll_prob(n):
    return float(min(map(abs, [13 - n, n - 1]))) / 36

probs = [roll_prob(i) for i in range(2, 13)]

def bingo_prob(n):
    probs = [roll_prob(i) for i in range(2, 13)]
    divisor_indices = [val - 2 for val in valid_divisors(n)]
    print(divisor_indices)
    return sum(probs[i] for i in divisor_indices)

def n_scores():
    return sorted([(bingo_prob(i), i) for i in range(2, 20)])

def play_game(arrs):
    boards = [Board(a) for a in arrs]
    winners = []
    while 1:
        for i, b in enumerate(boards):
            if b.move():
                winners.append(i)
        if winners:
            return winners

def tally_winners(arrs, ngames):
    winners = list(reduce(lambda a, b: a + b, [play_game(arrs) for _ in range(ngames)]))
    tally = []
    for i, b in enumerate(arrs):
        tally.append((b, winners.count(i)))
    return tally
        
            
def indices(lst, val):
    d = list(map(valid_divisors, lst))
    return [i for i in range(len(lst)) if val in d[i]]
