---
title: Alias Creation in Windows Using Python
feed: show
date: 17-02-2025
tags:
  - application
---

One thing I've missed in Windows post my switch from Linux is the ability to create aliases for commands.

In Linux, you can create an alias for a command by adding the following line to your `.bashrc` or `.bash_profile` file -

```bash
alias ll='ls -l'
```

This would allow you to use `ll` instead of `ls -l` in your terminal.

In Windows, you can create a similar alias by creating a batch file and adding it to your PATH environment variable.

Here's a simple Python script that can help you create a batch file that can be used as an alias -

```python
import os

# Creating a folder in the user's home directory to store the aliases

home_dir = os.path.expanduser('~')
alias_dir = os.path.join(home_dir, 'aliases')
os.makedirs(alias_dir, exist_ok=True)

# Adding the alias folder to the PATH environment variable in Windows

os.system(f'setx PATH "%PATH%;{alias_dir}"')

def create_alias(alias_name, command):
    with open(f'{os.path.join(alias_dir,alias_name)}.bat', 'w') as f:
        f.write(f'@echo off\n{command}')

if __name__ == '__main__':
    alias_name = input('Enter the alias name: ')
    command = input('Enter the command: ')
    create_alias(alias_name, command)
    print(f'Alias {alias_name} created successfully!')
```

You can run this script and provide the alias name and the command you want to run when the alias is called.

For example, if you want to create an alias `ll` for `dir`, you can run the script and provide `ll` as the alias name and `@dir %*` as the command.


This will create a batch file called `ll.bat` that you can add to your PATH environment variable and use `ll` as an alias for `dir` in your terminal.
```