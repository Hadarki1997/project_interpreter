#Q2

from functools import reduce

combine_with_space = lambda lst: reduce(lambda x, y: x + " " + y, lst)
lst2 = ["hello", "world", "people"]
print(combine_with_space(lst2)) 
