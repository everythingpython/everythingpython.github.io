---
title : Using Decorators
feed: show
date : 08-03-2023
---
#### 8th March 2024

In Python, a decorator is a way to modify or extend the behavior of a function or class without changing its source code. Decorators are a powerful tool for adding functionality to existing code, and they are especially useful when you want to apply the same behavior to multiple functions or classes.

### How Decorators Work
In Python, functions are first-class objects, which means they can be assigned to variables, passed as arguments to other functions, and returned as values from other functions. This makes it possible to define a decorator function that takes another function as an argument, modifies its behavior in some way, and then returns the modified function.

Here's an example of a simple decorator that adds logging to a function:

```python
def log_function(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Called {func.__name__} with args {args} and kwargs {kwargs}. Result: {result}")
        return result
    return wrapper

@log_function
def my_function(x, y):
    return x + y
```

In this example, log_function is a decorator that takes a function as an argument and returns a new function that logs the arguments and result of the original function. The `@log_function` syntax is a shorthand way of applying the decorator to the my_function function.

### Using Decorators with Classes
Decorators can also be used with classes in Python. Here's an example of a decorator that adds logging to a class method:

```python
def log_method(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"Called {func.__name__} with args {args} and kwargs {kwargs}. Result: {result}")
        return result
    return wrapper

class MyClass:
    @log_method
    def my_method(self, x, y):
        return x + y
```

In this example, `log_method` is a decorator that takes a method as an argument and returns a new method that logs the arguments and result of the original method. The `@log_method` syntax is a shorthand way of applying the decorator to the my_method method.

### Learning More About Decorators
Decorators are a powerful tool for extending the functionality of Python functions and classes. If you want to learn more about decorators, here are some resources to get you started:

- [Python Decorators: A Step-by-Step Introduction](https://realpython.com/primer-on-python-decorators/)
- [Decorators in Python: A Complete Guide](https://realpython.com/primer-on-python-decorators/)
- [Python Decorators: A Complete Guide](https://realpython.com/primer-on-python-decorators/)

Thanks for reading! Let me know if you have any questions or suggestions for future blog posts.