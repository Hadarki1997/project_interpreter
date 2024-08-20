#Q4

from functools import reduce

def cumulative_function(op):
    return lambda seq: reduce(op, seq)

factorial = cumulative_function(lambda x, y: x * y)

exponentiation = cumulative_function(lambda x, y: x ** y)

print(factorial([1, 2, 3, 4, 5]))  
print(exponentiation([2, 3, 2]))   
