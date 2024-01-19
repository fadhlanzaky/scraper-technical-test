'''
Smallest Less Five

input: numbers(str)
output: smallest_number(int)

constraints:
-> -999999999 <= numbers <= 999999999
-> at least one digit of '5'

summary:
The goal of this function is to return the smallest possible number after removing one digit of '5'.

I assume that the original number is excluded from the comparison, hence math.inf used as the initial
smallest number for later comparison. In the function I use min() to get the smallest number, that's why math.inf
is the perfect value for the initial comparison.

The strategy I use in this function is to iterate the numbers trying to find the '5',
when found, I use slicing to exclude the said '5' from the numbers, creating a new number, 
and compare it to the current smallest number.

Using min(), I replace the current smallest number to the new number if the new number is lower than
the current smallest number.

When finish iterating, the function returns the smallest possible number.

*Responding to the guidance* about focusing on the correctnes rather than performance. Why?
That's because we work with data, and data require precision, let alone numbers. A small incorrectness could
ruin the whole analysis. For example in accounting, missing one zero in one account can lead to imbalance. 
Therfore, prioritizing correctness ensures the reliability of the analysis and prevents potentiallly
costly errors.
'''

import math

def smallest_less_five(numbers: str) -> int:

    # input validation
    if not isinstance(numbers, str):
        return numbers
    
    # initialize the first smallest number as math.inf as it represents infinity (max)
    smallest_number = math.inf

    for index, char in enumerate(numbers):
        if char == '5':

            # removing the '5' using slice
            new_number = numbers[:index] + numbers[(index + 1):]
            
            # when '5' is the only char, and it's removed, return 0. No number to compare
            if new_number == '':
                return 0
            
            # compare the new number after removing the '5' to the current smallest number
            smallest_number = min(smallest_number, int(new_number))

    return smallest_number
