#Q3

from functools import reduce

square = lambda x: x ** 2
is_even = lambda x: x % 2 == 0
add_squares = lambda total, x: total + square(x)
sum_of_even_squares = lambda lst: reduce(add_squares, filter(is_even, lst), 0)
process_all_sublists = lambda list_of_lists: map(sum_of_even_squares, list_of_lists)

list_of_lists = [[3, 4, 5], [10, 15, 20, 25], [2, 4, 6, 8], [7, 9, 11, 13]]

result = list(process_all_sublists(list_of_lists))
print(result)
