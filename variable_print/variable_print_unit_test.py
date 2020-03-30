import unittest
from variable_print import variable_print

class TestStringMethods(unittest.TestCase):

    def test_file_not_created(self):
        pass

    def test_file_contents_correct(self):
        pass

    def test_print_is_correct(self):
        pass

if __name__ == '__main__':
    unittest.main()







def trial_func(a, b, c):
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
