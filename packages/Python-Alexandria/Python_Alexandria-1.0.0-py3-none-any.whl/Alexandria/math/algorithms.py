import itertools


"""
Algorithms
"""


def prime_factors(n):
    for i in itertools.chain([2], itertools.count(3, 2)):
        if n <= 1:
            break
        while n % i == 0:
            n //= i
            yield i


def largest_prime_factor(n):
    return list(prime_factors(n))[-1]
