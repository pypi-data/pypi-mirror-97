# PyPat-Console
A simple and sexy way to make an console interface

# How to setup
First install the package with the command (make sure you have Python 3.6 or higher)
```
pip install pypatconsole
```
Then you can import ``pypatconsole`` in Python. The package lets you import three functions: ``menu``, ``list_local_cases`` and ``clear_screen``. Usage of ``menu`` will be illustrated below. ``list_local_cases`` takes the output from ``locals()`` and lists all the functions in the local scope. ``clear_screen`` clears your screen, hence the name.

# How to implement
Simply implement the cases (as functions) in a Python file, then to initialize the interface you simply use the ``menu`` function at the bottom
```python
from pypatconsole import menu

            .
            .
            .

menu(locals(), title=' Main menu title here ', main=True)
```
You can import whatever modules, classes and functions you want in the file without them interfering with the functions defined your file. You will need to implement docstrings to every case. The first line of text in the docstring will be used as the description in the console interface.

The order of the cases is alphabetically sorted by the function name.

The function signature of ``menu`` along with its docstring is as follows:
```python
def menu(cases: Union[list, dict, ModuleType], title: str=' Title ',
                blank_proceedure: Union[str, Callable]='return',
                decorator: Callable=None, run: bool=True, main: bool=False):
    '''
    Factory function for the CLI class. This function initializes a menu.

    Parameters
    ------------
    cases: Can be output of locals() (a dictionary) from the scope of the cases

           Or a list functions

           Or a module containing the case functions

    title: title of menu

    blank_proceedure: What to do the when given blank input. Can be user defined
                      function, or it can be a string. Available string options
                      are:

                      'return', will return to parent menu, if you are at main
                      menu, this will exit the program

                      'pass', does nothing. This should only be used for the
                      main menu

                      'exit', exits the program

    decorator: Whether to decorate functions

    run: To run menu instantly or not

    Returns
    --------
    CLI (Command Line Interface) object. Use .run() method to activate menu.
    '''
```

### Examples

Say we are editing console.py
```python
from random import randint
from time import sleep
from pypatconsole import menu

def case1():
    '''
    FizzBuzz!

    When you get the urge to fizz your buzz
    if you know what I mean
    '''
    for i in range(21):
        stringy = ''

        fizz = i % 3 == 0
        buzz = i % 5 == 0

        if fizz:
            stringy = stringy + 'Fizz'
        if buzz:
            stringy = stringy + 'Buzz'
        if not (fizz or buzz):
            stringy = i

        print(stringy)
        sleep(0.1)

def case2():
    '''
    Print a small random integer
    '''
    print(randint(0,9))
    sleep(0.5)

menu(locals(), title=' Main menu ', main=True, blank_proceedure='pass')
```

will result with this when running: ```python console.py```:

```
-------------- Main menu ---------------
1. FizzBuzz!
2. Print a small random integer

Input:
```
## Special cases
Entering ``..`` will exit the current menu, effectively moving you to the parent menu if you are implementing nested cases. If you are in the main menu it will exit the program.

Entering ``q`` will exit the program (of course Ctrl+C works as well)

Entering ``h`` will display this text that explains the special cases.

Enter ``-1`` or any integer will "reverse" the choices, such that you take the last choice. This is motivated by Python lists where you can index like list[-1]

## Arguments
The cases can take arguments as well! Simply implement them as functions with type hints (type hints are mandatory for the case functions):
````python
from pypatconsole import menu

def case1(a: int, b: int):
    '''Add two integers'''
    print(a+b)

def case1(a: str, b: str):
    '''Append two strings'''
    print(a+b)

def case3(a: list):
    '''Print elements in list and their types'''
    [print(f'Element {i}: {elem}, type: {type(elem)}') for i, elem
                                                        in enumerate(a)]

menu(locals(), title=' Main menu ', main=True)
````
Then simply give the arguments along with the choice:
````
-------------- Main menu ---------------
1. Add two integers
2. Append two strings
3. Print elements in list and their types


Input: 1 60 9

69
````
````
Input: 2 "cat and dog" mathemathics

cat and dogmathemathics

Note: Single token strings don't even need quotes
````
````
Input: 3 ['cat',69,420.0]

Element 0: cat, type: <class 'str'>
Element 1: 69, type: <class 'int'>
Element 2: 420.0, type: <class 'float'>

Note: You cannot have any spaces when giving lists, tuples, dicts and such as the input parser will break them.
````

The program will read the desired types from the function signature, then it will convert the input into the appropriate types. The only supported types are the built in Python types:
- str
- int
- float
- tuple
- list
- set
- dict

## Nested cases
If you want to implement nested cases, then you can simply reuse the menu function in the function scope. When doing nested cases, you should not give the keyword ``main=True`` to the ``menu`` function.

```python
from pypatconsole import menu

def parentcase1():
    '''Fizz'''
    def subcase1():
        '''docstring1'''
        pass

    def subcase2():
        '''docstring2'''
        pass

    menu(locals(), title= ' Title here ')
menu(locals(), title=' Main menu ', main=True)
```
You can create another module for the other cases and pass them as well:
```python
from pypatconsole import menu
import other_cases

def samplecase():
    '''Foo'''
    menu(other_cases, title= ' Title here ')
menu(other_cases, title= ' Main menu ', main=True)
```

or you can give a list of functions, which will enable you to force the ordering of the cases as well:
```python
from pypatconsole import menu

def parentcase1():
    '''Fizz'''
    def subcase1():
        '''docstring1'''
        pass

    def subcase2():
        '''docstring2'''
        pass

    menu([subcase2, subcase1], title= ' Title here ')
menu(locals(), title=' Main menu ')
```
## What if want to define functions without having them displayed in the menu?
Of what I can think of: you can either define your functions in another python file and import that, or you can create a class (in the same file as the case functions) that consists of your functions as static methods.

## Optional: Decorator
To enforce a common behavior when entering and leaving a case within a menu, you give a decorator to the ``menu`` function. However, it is important that the decorator  implements the ``__wrapped__`` attribute (this is to handle docstrings of wrappers as arguments for wrapped functions). Generally, it should look like this

```python
import sleep

def case_decorator(func):
    '''Decorator to enforce commmon behavior for cases'''

    def case_wrapper(*args, **kwargs):
        '''Verbosity wrapper'''
        print('Yeah! Going in!')
        sleep(1)
        retobj = func(*args, **kwargs)
        print('Woah! Going out!')
        sleep(1)
        return retobj
    # This is necessary in order to unwrap using inspect module
    case_wrapper.__wrapped__ = func
    return case_wrapper
```
Since the decorator is a function, you cannot have it in the same namespace as the case functions, so you can for example implement it in another file. To use it you do as following:
```python
from pypatconsole import menu
from case_decorator import case_decorator

# A lot of cases here

menu(locals(), decorator=case_decorator, main=True)
```

# Why
Sometimes you want to have a simple console interface so you can do things step by step.
Here are some applications:

## Stock data pipeline
Data scraping and data cleaning pipeline for stock data
```
------------- Mulababy420 --------------
1. Update all data
2. Obtain Oslo Bors quotes and returns
3. Scrape Oslo bors HTML files
4. Scrape Yahoo Finance
5. Backup current data
6. Exit program
Enter choice:
```
Sometimes I don't want to run everything at once. Maybe I just want to backup data instead of doing all everything. PyPat-Console will enable a very quick implementation of a console.
Without the console I would need to find the right file to run (and maybe comment things out first as well). The console organizes everything into one place.

## Database interface
```
------BergenDB------
1. Log rent
2. Log power
3. Print table
4. Plot table
5. Commit changes
6. Discard changes
7. Exit
```
I log my rent and power bills in a SQL database. I have made a Python API to manage the database, and I just do everything through the interface. No need to script anything or write any SQL queries.

## Control your Google Compute VM
```
----------------GCE-----------------                                                                      
1. SSH to personal instance
2. SSH to project instance
3. start/stop personal instance (0 to stop, 1 to start, 2 to restart)
4. start/stop project instance (0 to stop, 1 to start, 2 to restart)
5. Get status personal instance
6. Get status project instance
7. Other instance control      

Entering blank returns to parent menu
Input:
```
