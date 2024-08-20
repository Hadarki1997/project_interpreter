#Q6

from functools import reduce

count_palindromes = lambda list_of_lists: list(map(lambda sublist: reduce(lambda count, word: count + 1 if word == word[::-1] else count, sublist, 0), list_of_lists))

list_of_lists = [["madam", "apple", "level"], ["hello", "noon", "world"], ["abba", "xyz"]]
result = count_palindromes(list_of_lists)
print(result)  
