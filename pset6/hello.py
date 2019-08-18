from sys import argv
from cs50 import get_string

name = get_string("What is your name?\n")
print("hello, {}".format(name))