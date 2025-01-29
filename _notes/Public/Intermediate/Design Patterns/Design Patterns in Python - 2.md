---
title: Design Patterns in Python - 2
feed: show
date: 15-03-2024
---

### Creational Patterns - The Factory Method

In the previous article - [[Design Patterns in Python - 1]]  , I wrote about the simplest creational pattern - The Singleton. In this edition, we look at another way to create objects - the Factory method.

Again, we start with examining the meaning of the word and why it would have been used for the behavior to follow. A _factory_ in the common usage of the word is a place where products are manufactured, where the factory is the entity doing the manufacturing.

Similarly, in the software world, the Factory pattern involves a base class with some properties that can be extended by children classes with their own implementations of those inherited properties.

But why is it required to begin with? Let us look at an example of a case where I’d like to assemble a team of X-Men.

```python
class Telepathy:
    @staticmethod
    def use_power(name: str) -> str:
        return f"{name} is reading minds with telepathy."


class Telekinesis:
    @staticmethod
    def use_power(name: str) -> str:
        return f"{name} is lifting objects using the power of the mind."


class OpticBlast:
    @staticmethod
    def use_power(name: str) -> str:
        return f"{name} is firing powerful optic blasts from the eyes."


class XMen:
    def __init__(self, name: str, power: str):
        self.name = name
        self.power = power

    def use_power(self) -> str:
        return self.power.use_power(self.name)


# Client code example

def showcase_power(mutation_type: str, name: str) -> str:
    if mutation_type == "telepath":
        power = Telepathy
    elif mutation_type == "telekinetic":
        power = Telekinesis
    elif mutation_type == "optic_blast":
        power = OpticBlast
    else:
        raise ValueError("Invalid X-Men power provided")

    xmen = XMen(name, power)
    return xmen.use_power()

print(showcase_power("telepath", "Professor X"))
print(showcase_power("optic_blast", "Cyclops"))
```

**Output -**

```bash
Professor X is reading minds with telepathy.
Cyclops is firing powerful optic blasts from the eyes.
```

This example uses **no known design pattern**. At best, one could argue that it uses some variation of the Strategy Pattern but even that is a stretch.

Now, what is the problem with writing code like this? After all, the output is correct, right?

❌ The problem comes when we’ll need to introduce another “skill” a new X-Men member comes to possess i.e. if the code needs to be extended, here we directly need to edit the Client code and add another if clause.

This goes against the Open/Closed principle of the [SOLID principles](https://en.wikipedia.org/wiki/SOLID) of coding .

[It’s a principle for object oriented design first described by Bertrand Meyer that says that](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.) _[“software entities (classes, modules, functions, etc.) should be](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.) **[open](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.)** [for extension, but](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.) **[closed](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.)** [for modification”](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.)_[.](http://joelabrahamsson.com/a-simple-example-of-the-openclosed-principle/#:~:text=It%E2%80%99s%20a%20principle%20for%20object%20oriented%20design%20first%20described%20by%20Bertrand%20Meyer%20that%20says%20that%20%E2%80%9Csoftware%20entities%20(classes%2C%20modules%2C%20functions%2C%20etc.)%20should%20be%20open%20for%20extension%2C%20but%20closed%20for%20modification%E2%80%9D.)

To remedy this, we introduce the usage of the Factory pattern. Let’s rewrite this code using a parent class with an abstract method for a generic XMen character -

```python
from abc import abstractmethod

class XMen:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def use_power(self):
        pass


class Telepath(XMen):
    def use_power(self):
        print(f"{self.name}  is reading minds with telepathy.")


class Telekinesis(XMen):
    def use_power(self):
        print(f"{self.name} is lifting objects using the power of the mind.")


class OpticBlast(XMen):
    def use_power(self):
        print(f"{self.name} is firing powerful optic blasts from the eyes.")


class XMenFactory:
    @staticmethod
    def create_xmen(mutation_type, name):
        if mutation_type == "telepath":
            return Telepath(name)
        elif mutation_type == "telekinetic":
            return Telekinesis(name)
        elif mutation_type == "optic_blast":
            return OpticBlast(name)
        else:
            raise ValueError("Invalid X-Men power provided")


# Client example
def showcase_powers(mutation_type, name):
    xmen = XMenFactory.create_xmen(mutation_type, name)
    xmen.use_power()


showcase_powers("telepath", "Professor X")
showcase_powers("optic_blast", "Cyclops")
```

💡 **Now what is the difference here?**

First notice that we’ve moved away from standalone classes for each kind of _Power_ to an Abstract Base Class - `XMen` - and concrete children classes that implement and extend the `XMen` class based on the power that we want to describe.

✅ Additionally, if a new _Power_ is to be added, the Client code - `showcase_powers` - can remain completely oblivious to this and the XMenFactory can simply be extended to have one more if-clause along with another Concrete class for the _Power_ itself. This satisfies the Open/Closed principle mentioned above as well.

**Summary :**

In cases where you’d want to separate the creation of an object from where it is being used, a Factory pattern is the way to go. Additionally and perhaps more importantly, if it’s likely that your code is evolving with having to add more classes that effectively perform the same functions but vary in the implementation of the functions themselves, you should resort to a Factory pattern.

For example, think of the case where you need to implement the training-of and prediction-using different models in a Machine Learning use-case. It is likely that your initial codebase might implement some rudimentary models like Decision Trees and Linear Regression etc. Both of these models will need to implement their own versions of training and prediction. But eventually you might need to add more complex models. This should ideally not involve modification of the code where these models are being **used**. A factory pattern will make this a whole lot easier and the code more readable.