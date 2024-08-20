#Q1


fibonacci = lambda n, a=0, b=1: [a] if n == 1 else [a] + fibonacci(n-1, b, a+b)

print(fibonacci(10))  
