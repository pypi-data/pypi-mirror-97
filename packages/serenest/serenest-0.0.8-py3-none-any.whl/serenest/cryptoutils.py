#!/usr/bin/env python3

import random

def gcd(a,b):
    """
    Math already provides an implementation, no need to reinvent the wheel
    """
    return math.gcd(a,b)

def xgcd(a,b):
    prevx, x = 1, 0
    prevy, y = 0, 1
    while b:
        q = a//b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a%b
    return a, prevx, prevy

def modinverse(a, prime):
    if not (is_prime(prime)):
        return "the second argument is a composite"
    if (a == 0):
        return 0
    _, inverse, _ = xgcd(a, prime)
    if (inverse < 0):
        inverse += prime
    return inverse


def legendre(a, prime):
    """
    Determines whether a is a quadratic residue modulo prime
    In other words, makes sure a has a square root mod prime
    """
    if not(is_prime(prime)):
        return "the second argument is a composite"
    if (a == 0):
        return 0
    return pow(a, (prime-1)//2, prime)

def is_prime(candidate):
    """
    Just an alias for Rabin-Miller
    """
    return rabin_miller(candidate)

def rabin_miller(candidate, number_of_rounds = 100):
    """
    see https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test for details
    Returns False if the number is found to be a composite;
    Returns True if the number is likely to be a prime.
    The higher the number of rounds, the more accurate the test will be.
    """
    if (candidate == 2 or candidate == 3 or candidate == 5 or candidate == 7):
        return True
    if (candidate % 2 == 0 or candidate % 3 == 0 or candidate % 5 == 0 or candidate % 7 == 0):
        return False
    r, s = 0, candidate - 1
    while s%2 == 0:
        r += 1
        s //= 2
    for _ in range(number_of_rounds):
        random_integer = random.randrange(2, candidate - 1)
        x = pow(random_integer, s, candidate)
        if (x == 1 or x == candidate - 1):
            continue
        for _ in range(r-1):
            x = pow(x, 2, candidate)
            if (x == candidate-1):
                break
        else:
            return False
    return True

#TODO: tonelli-shanks





