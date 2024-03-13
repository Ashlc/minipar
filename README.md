# PyC Language Interpreter

PyC is a simple language that is similar to Python, but with a few differences. The interpreter is written in Python and is able to interpret and execute PyC code.

## :sparkles: Differential features 

:rock: - **Static typing**: PyC is statically typed, which means that the type of a variable must be declared before it is used.

:straight_ruler: - **No indentation**: PyC does not use indentation to define blocks of code. Instead, it uses curly braces.

## :keyboard: Syntax

Here is an example of a PyC program that calculates the factorial of a number:

```cpp
int factorial(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

factorial(5);
```


