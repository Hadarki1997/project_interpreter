# Q7
# The purpose of a generator is to save memory space.
# In the context of eager evaluation, all data is stored in memory upfront.
# In contrast, with lazy evaluation, each value is computed only when needed, 
# thereby avoiding the pre-storage of everything in memory.


def generate_values():
    print('Generating values...')
    yield 1
    yield 2
    yield 3


def square(x):
    print(f'Squaring {x}')


    return x * x

print('Eager evaluation:')
values = list(generate_values())
squared_values = [square(x) for x in values]
print(squared_values)

print('\nLazy evaluation:')
squared_values = [square(x) for x in generate_values()]
print(squared_values)