def fibosum(number):
    """
    Returns the sum of the Fibonacci sequence
    """
    try:
        n1, n2 = 0, 1
        count = 0

        fibonacci_sum = 0
        sequence = [0, 1]

        if number <= 0:
            return False
        elif number == 1:
            fibonacci_sum = n2
        else:
            while count <= number:
                sequence.append(n1)
                nth = n1 + n2
                n1 = n2
                n2 = nth
                count += 1

            fibonacci_sum = sum(sequence)
        return fibonacci_sum
    except TypeError:
        return False
