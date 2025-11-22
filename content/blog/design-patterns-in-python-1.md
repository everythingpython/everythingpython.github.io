---
title: "Design Patterns in Python - 1"
date: 2024-03-14
slug: design-patterns-in-python-1
---

If you’ve been using Python in production for a while like I have, you’ve either intentionally or inadvertently used some design patterns in your code. But what are they anyway?

Design Patterns are well, patterns or reusable structures of code (templates) - that can be employed to implement solutions to software problems.

These patterns have been bucketed into 3 main categories :

- Creational Patterns
- Structural Patterns
- Behavioural Patterns

On what basis though? What do each of these words mean in a programmatic sense? I will deal with each of the meanings as we come across patterns that fall under them.  
  
The first one in this [ ] (list, heh) is “_Creational Patterns_”. Simplest to explain, they pertain to patterns that involve the **creation** of one or more objects.

The following patterns come under the Creational Patterns ☂️ -

- Singleton
- Factory Method
- Abstract Factory
- Builder
- Prototype

## Singleton

The Singleton patterns derives its origin (as most of the others do) from its introduction in the 1990s book “[Design Patterns: Elements of Reusable Object-Oriented Software](https://en.wikipedia.org/wiki/Design_Patterns)” written by the “Gang of Four” - Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides.

In the book, the Singleton pattern is described as a creational pattern that ensures a class has only one instance and provides a global point of entry to that instance.

Dutifully, that is how we use it in Python as well.

```python
# singleton
class Batman:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance
```

The `__new__` method is a special method (commonly referred to as magic method/dunder method) used to create a new instance of a class. In this implementation we’re overriding the default __new__ method to prevent the creation of an instance of the class if one already exists.

The `cls.instance = super().__new__(cls)` line is used to create a new instance of the object using Batman’s parent class’ implementation of the __new__ method.

> 💡 Trivia question : _What is Batman’s parent class called? And no, it’s not Thomas or Martha Wayne_ 😁

Hence, if we execute the following :

```python
b1 = Batman()
b2 = Batman()
print(f"b1 is b2 = {b1 is b2}")  
```

Results in :

```python
b1 is b2 = True
```

Because even when two objects of the class Batman are created, only class `b1` is created and `b2` is simply initialized to `b1` when attempted to be created.

**Where is it used?**

Okay great, so now we know what a Singleton is. But where is it used?  
Technically, it can be used anywhere there is a need to use the same object throughout the scope of the code, for example, **a logger object**. But for trivial implementations such as a single file program, you need not resort to a Singleton class or even a class at all. A simple global instance of your class will suffice.

Here’s an example accomplishing the same action without a singleton pattern but also note something simple but critical in the process -

```python
class Batman:

    def __init__(self):
        self.name = "Bruce Wayne"

    def who_am_i(self):
        print(f"I'm vengeance. I am the night. I am {self.name}")


batman_obj = Batman()
```

Now save this file as `call_batman.py` and import the instance `batman_obj`

```bash
Python 3.12.2 | packaged by Anaconda, Inc. | (main, Feb 27 2024, 17:28:07) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

>>> from call_batman import batman_obj
>>> batman_obj.who_am_i()
I'm vengeance. I am the night. I am Bruce Wayne
```

While this works, there is a missing element that prevents this from being a singleton-equivalent. (Can you spot it?)

The flaw here is that while we’ve imported batman_obj, it’s not the only instance of the class Batman that can be created, thereby defeating the workaround’s efficacy. i.e. I can totally create a second object

```python
>>> from call_batman import Batman, batman_obj
>>> batman_obj2 = Batman()
>>> batman_obj is batman_obj2
False
```

The point however is that `batman_obj` can be used _like_ a singleton even though the design pattern isn’t adhered to.

**Summary :**

In cases where you would need to write logger statements or for state management etc, the Singleton makes for a great pattern and coding practice to employ!

Feel free to send me examples of code snippets of how you use Singletons in your codebase/ projects :)

Thanks for reading Everything Python! Subscribe for free to receive new posts and support my work.