import re

string = "Was it a car or a cat I saw?"
string2 = "Severus was impressed at Harry's Occlumency skills but he did not show it."
# re.match() will return None
print(re.match("cat", string))

# re.search() will return a match object
print(re.search("cat", string))

# re.match() will return a match object
print(re.match("Severus", string2))

# re.search() will return a match object
print(re.search("Severus", string2))