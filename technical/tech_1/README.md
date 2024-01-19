
# Initiator of Discount
Environment:
- python version: `3.19.13`
- dependencies: `requirements.txt`
  
input: `prices(str)`

output: `index(int)`

constraints:
 - 1 <= N <= 100
 - 1 <= price <= 50000

  

## summary

The first task in this function is to transform a string of numbers into a list.

I use split(), a built-in function with no parameter passed since the default behaviour of this function is to split the string according to the whitespaces.

Some validations are also included, the first validation checks whether the input is a string, and the second validates whether it is an empty input.

There are 2 conditions stated to tell if the price has dropped, the first one if the current price is less than the previous price, and the second one if the current price is lower than the starting price.

Based on the conditions, I eliminate the first condition because the price could be reduced without being lower than the starting price due to a price increment. Hence, the only matter condition is the second one.

For the iteration I use enumerate() as it keeps the index of each element, and float instead of integer for precision.

## Test
The test run using pytest and the data for testing stored in data.csv
```sh
pytest main_test.py
```
