---
title: Class Methods
feed: show
date: 2024-11-17
---
#### 17th Nov 2024

> *I was today years old when I learnt about how to use the classmethod decorator in Python.*
 

I've always thought of a class method as a method in a class - just intuitively. But there's actually a decorator called "@classmethod". 

Imagine you have a class C. A class method in this class would be defined as - 

```python
class C: 
	@classmethod
	def cl_method(cls):
		print(f"I'm in the class method {cls=}")
```

The distinctive marks of a class method are : 
- the decorator - @classmethod
- the first argument to the method is always the class itself - denoted by "cls" but it needn't have been

The execution and the behaviour of the method are :

```python
>>> print(C.cl_method)
I'm in the class method cls=<class '__main__.C'>
```

For a class method, even if an object of the class is used to call the method, the first argument passed is still 'cls'

---

![Alt Text](/assets/img/intermediate/classmethods/wheretho.png)
And This, is the 1024 KB question. 

For the most part, they are used to create "alternative constructors" . This is the response I saw documented throughout the internet wherever I asked the question. Even LLMs seem to be trained to return this as the only known answer . Here's me asking llama3.2  -

![Alt Text](/assets/img/intermediate/classmethods/llama.png)


So what does this mean? 
I went hunting in the standard libraries for usage of this decorator and I didn't have to look far. 

In the datetime library, the date class uses this to implement the `today()` method and this is the definition - 

```python
@classmethod  
def today(cls):  
    "Construct a date from time.time()."  
    t = _time.time()  
    return cls.fromtimestamp(t)
```

So we see it's using the timestamp function from the class `date` to print the current date after fetching the current time using the builtin `time` library. 

When it's called - 

```python
from datetime import date
print(date.today())
```

We get "2024-11-17" .

> I took longer than I'd like to admit to understand how the representation was being printed and I finally realised it's because the `__str__` definition for this class controls the display to be sent as the Isoformat of a date which is `"year-month-day"` . In hindsight, this is perfectly obvious. 🤦

---

To make things interesting, I decided to create a function of my own by extending the date class and came up with this - 

```python
class MyDate(date):  
    @classmethod  
    def yesterday(cls):  
        today = date.today()  
        d = today - timedelta(days=1)  
        return cls.isoformat(d)
        
print(MyDate.yesterday())
```

When executed, it returns, unsurprisingly - "2024-12-16" , which is yesterday's date.

This feels like it could have been introduced in the built in `date` library as well, but that's a rather slippery slope.

Anyway, so that's the @classmethod decorator. I'm sure its brother the @staticmethod is more popular knowledge even if it's even lesser used, but that's a topic for another day.