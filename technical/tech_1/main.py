'''
Initiator of Discount

input: prices(str)
output: index(int)

constraints:
-> 1 <= N <= 100
-> 1 <= price <= 50000

summary:
The first task in this function is to transform a string of numbers into a list.

I use split(), a built-in function with no parameter passed since the default behaviour of 
this function is to split the string according to the whitespaces.

Some validations are also included, the first validation checks whether the input is a string, 
and the second validates whether it is an empty input.

There are 2 conditions stated to tell if the price has dropped, the first one if the current price
is less than the previous price, and the second one if the current price is lower than the starting price.

Based on the conditions, I eliminate the first condition because the price could be reduced without
being lower than the starting price due to a price increment. Hence, the only matter condition is the second one.

For the iteration I use enumerate() as it keeps the index of each element, 
and float instead of integer for precision.
'''

def initiator_of_discount(prices: str) -> int:

    # input validation, if the input is not string, return default
    if not isinstance(prices, str):
        return 0
    
    # breakdown the string into list
    prices = prices.split()

    # input validation, if no data provided, return default
    if len(prices) == 0:
        return 0
    
    initial_price = float(prices[0])

    # enumerate will provide the index of each element, which is beneficial for this case
    for index, price in enumerate(prices):

        # return the index when the price drop below the initial price
        if float(price) < initial_price:
            return index
    
    # default return when no price drop
    return 0

