# project_interpreter

## Documentation
<details>

<summary>Declare a variable</summary>
due to the principle of immutability, variable assignments are not supported. Instead, values are passed directly to functions, and results are returned without modifying any state. This ensures that all data remains unchanged throughout the execution of the program.
#### Example of Immutability:

```python
defun add(a, b) { a + b }
add(3, 4))
```
In this example, instead of assigning the result to a variable, the result is directly printed.

</details>
<br /> 
<details>

<summary>Working with Lambda Expressions</summary>
Lambda expressions (anonymous functions) are defined and used inline without variable assignments. This aligns with the immutability principle.

#### Example of Lambda Expression:
lambd(x, y) (x + y)(3, 4)
This lambda function takes two arguments, x and y, adds them, and the result is immediately used.

You can use lambda expressions directly within other expressions or function calls, but they cannot be assigned to variables due to the immutability constraint.
#### Another Example:
lambd(x) (x * x)(5)
This squares the number 5 and prints the result.

</details>
<br /> 
<details>
  
<summary>Function declaration and calling</summary>

To declare a function, use the keyword 'defun'. To call a function, write its name with the correct arguments.

### Basic Function Declaration and Calling
```
defun multiply(x, y) { x * y }
multiply(4, 5)
```
output:
```
20
```
You could also preform recursion:
```
defun factorial(n) { n ==0 || n * factorial(n - 1) }
factorial(4)
```
output:
```
24
```

### Functions return 
Functions can return an int:
```
defun square(a) {
    a * a
}
square(5)
```

output:
```
25
```
And can return a boolean value:
```
zap eq(a,b){
    return a == b;
}
println(eq(6,6));
```
output:
```
True
```
And their values can be used just like any other value for calculation or logic:
```
defun isEqual(a, b) {
    a == b
}
isEqual(6, 6)
```

</details>
<br/>
<details>

<summary>If statements</summary>
The language supports basic conditional logic using if statements. Here's how to use them:

### Basic Syntax
if condition
expression1
else
expression2
### Examples
```bash
1. Simple if statement:
if 5 > 3 10 else 20
```
This will return `10`.

</details>
<br/>
<details>

<summary> Simple Functional Language Interpreter</summary>

This interpreter offers two main modes of operation: an interactive mode (REPL) and file execution.

## 1. Interactive Mode (REPL)

This mode allows you to enter and execute code line by line.

To start the REPL:

```bash
python repl.py
```
After launching, you'll see the calc> prompt and can start entering commands:

```bash
calc> defun multiply(x, y) { x * y }
None
calc> multiply(4, 5)
20
```
Notes:

Function definitions return None.
Results of expressions and function calls are displayed immediately.

## 2. Running a Program File
To run a program from a file:

Save your code in a file with a .lambda extension, e.g., program.lambda.
Run the following command in the terminal:
```bash
python file_runner.py program.lambda
```
*Example:*
Contents of program.lambda:
```bash
defun factorial(n) { n == 0 || n * factorial(n - 1) }
factorial(5)
3 + 5
```
*Output:*
```bash
120
8
```
