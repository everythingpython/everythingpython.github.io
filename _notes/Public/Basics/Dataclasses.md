---
title: Dataclasses
feed: show
date: 2024-11-19
tags:
  - TIL
---
###  19th Nov 2024

I was trying to write an article on Dataclasses[^2] and I looked up an example on the official website[^1]

Easy enough on the face of it, but it led me into quite a rabbit hole.

A dataclass allows for the creation of "special methods" for a class when the annotation @dataclass is sighted. 

So if I have a class "Superhero" with the annotation : 

```python

@dataclass
class Superhero:
    """
    A class of superheroes and properties about their appearance in Marvel movies
    """
    name: str
    superpower: str
    appearances: int = 0

    def beckon(self):
	    print(f"{self.name} with the super power - {self.superpower} has appeared in Marvel movies {self.appearances} times")
         

superhero = Superhero("Aquaman","Underwater breathing",2)
superhero.beckon()
```


It effectively means that : 

The `__init__ ` function, `__repr__` function and many more are created for it automatically. 

---

Here's something cool though. 

I created one more function without dataclasses - 

```python
class Superhero_nodc():
    """
    A class of superheroes and properties about their appearance in Marvel movies
    """
    def __init__(self, name, superpower,appearances=0):
         
        self.name = name
        self.superpower = superpower
        self.appearances = appearances

    def beckon(self):
	    print(f"{self.name} with the super power - {self.superpower} has appeared in Marvel movies {self.appearances} times")
         
```

---

Now when I check the attributes of each of these classes using - 

```python
attributes_dc = dir(Superhero)
attributes_nodc = dir(Superhero_nodc)
```

As a result of understanding what dataclasses do, seeing that the following were the attributes for Superhero wasn't surprising - 

```markdown
['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

But when we try to see what the attributes of the vanilla class **Superhero_nodc** are versus **Superhero**

```python
>>> from pprint import pprint # For pretty printing
>>> pprint([i for i in attr_dc if i not in attr_nodc])
['__annotations__',
 '__dataclass_fields__',
 '__dataclass_params__',
 '__match_args__',
 '__replace__',
 'appearances']
```

The dataclass fields and params are understandable and I will look into why annotations and `__replace__` show up, but the thing that caught my attention was the presence of **appearances** . 

Turns out that the default values set during definition of a dataclass end up manifesting as class attributes and thereby populate the `__dict__` of the class. 
Hence it shows up when `dir` is called. 

---

I also learnt about the interactive Help that the Python REPL offers along the way - 
![Alt Text](/assets/img/basics/help_repl.png)


Also here's a neat little experiment I ended up doing - Comparing the attributes for a dataclass and a regular class using tabs in Textual[^3] !
![Alt Text](/assets/img/basics/tabs_textual.gif)

### References 

[^1]: https://docs.python.org/3/library/dataclasses.html#mutable-default-values
[^2]: https://peps.python.org/pep-0557/
[^3]: https://textual.textualize.io/widgets/tabbed_content/#__tabbed_1_2
