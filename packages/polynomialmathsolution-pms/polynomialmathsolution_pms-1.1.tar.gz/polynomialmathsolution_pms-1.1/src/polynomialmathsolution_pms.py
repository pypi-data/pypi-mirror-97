# + poly[1]x(n-2) + .. + poly[n-1]

def solution(poly, n, x):
    # Initialize result

    result = poly[0]

    # Evaluate value of polynomial

    # using Horner's method

    for i in range(1, n):
        result = result * x + poly[i]

    return result