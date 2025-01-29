
import re

string = "Was it a car or a cat I saw?"
string2 = "Hello, World!"
# re.match() will return None because the pattern does not match the beginning of the string
print(re.match("cat", string))

# re.match() will return a match object with the first match - checking in string 2
print(re.match("Hello", string2))


# re.search() will return a match object with the first match
print(re.search("cat", string))

# re.findall() will return a list of all matches as strings
print(re.findall("cat", string))

# re.finditer() will return an iterator of all matches as match objects
for match in re.finditer("cat", string):
    print(match)

# re.fullmatch() will return None because the pattern does not match the entire string
print(re.fullmatch("cat", string))

# re.split() will return a list of strings split by the pattern provided
print(re.split(" ", string))

# re.sub() will return a string with the substitution made
print(re.sub("cat", "dog", string))