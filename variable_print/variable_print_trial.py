"""
Distributed under my own will

Author: Severn Anderson
"""

from variable_print import variable_print

@variable_print(True, True, False)
def variable_print_trial(a, b, c):
    a = 10
    b= 15
    c = 20
    d = 2 * 45

    def inner_func():
        inner = 25
        inner += 1
        return inner

    z = inner_func()
    
    return d

if __name__ == "__main__":
    variable_print_trial(11, 16, 21)
