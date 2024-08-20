#Q8

prime_numbers_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x**0.5) + 1))], reverse=True)

numbers = [3, 4, 7, 10, 11, 13, 16, 17, 19]
result = prime_numbers_desc(numbers)
print(result) 
