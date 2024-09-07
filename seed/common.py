#
# This module is meant for helper functions
#
import re

def get_num_words(description:str):
    """ Get the number of words in a description. Words are separated by white space """

    # Split by words
    num_words = len(re.split(r'\s+', description))
    return num_words

def get_fibonacci(n:int):
    """
    Calculate the nth Fibonacci number using recursion.

    Args:
        n (int): The position of the Fibonacci number to calculate (0-indexed).

    Returns:
        int: The Fibonacci number at position n.

    Raises:
        ValueError: If n is negative.
    """

    # Don't allow negative numbers
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    if n <= 1:
        return n

    # Recursive case: fib(n) = fib(n-1) + fib(n-2)
    return get_fibonacci(n - 1) + get_fibonacci(n - 2)


def is_fibonacci(n:int):
    """
    Check if a given integer is a Fibonacci number.

    This function uses the property that every Fibonacci number
    (except 0) is of the form (5*m^2 + 4) or (5*n^2 - 4) for some integers m or n.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is a Fibonacci number, False otherwise.
    """

    if n < 0:
        return False

    if n <= 1:
        return True

    # Calculate the discriminant
    discriminant = 5 * n * n + 4

    # Check if discriminant is a perfect square
    m = int(discriminant ** 0.5)
    if m * m == discriminant:
        return True

    # Calculate the discriminant for the second form
    discriminant = 5 * n * n - 4

    # Check if this discriminant is a perfect square
    m = int(discriminant ** 0.5)
    if m * m == discriminant:
        return True

    # If neither form results in a perfect square, n is not a Fibonacci number
    return False


def get_next_fibonacci(n:int):
    """Get the next number in the fibonacci sequence after n
    Args:
        n (int): The fibonacci number to start

    Returns:
        n (int): The next number in the fibonacci sequence after n
    """
    # Handle base cases
    if n <= 0:
        return 1
    elif n == 1:
        return 1

    # Initialize the first two Fibonacci numbers
    a, b = 0, 1

    # Find the Fibonacci number closest to or just above n
    while b < n:
        a, b = b, a + b

    # If b equals n, return the next Fibonacci number
    if b == n:
        return a + b
    # If b is greater than n, b is the next Fibonacci number
    else:
        return b
