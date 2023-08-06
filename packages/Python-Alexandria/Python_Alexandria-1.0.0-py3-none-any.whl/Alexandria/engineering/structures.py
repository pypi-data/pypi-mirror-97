def macauley(x, k):
    return x - k if x - k >= 0 else 0


def macauley0(x, k):
    return 1 if x - k >= 0 else 0