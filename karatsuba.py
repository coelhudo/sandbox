#Understanding karatsuba multiplication
#https://en.wikipedia.org/wiki/Karatsuba_algorithm

import math
import unittest

def number_of_digits(number):
    #from http://stackoverflow.com/a/2189827/174605
    if number < 1:
        return 1
    return int(math.log10(number))+1        

def separate_number(number):
    digits = number_of_digits(number) 
    if digits == 1:
        return number, 1

    digits = digits - 1 if digits % 2 else digits
    digits_separation = 10 ** (digits/2)
    first = number // digits_separation
    second = number - first * digits_separation
    return first, second
    

def karatsuba(x, y):
    x_n = number_of_digits(x)
    y_n = number_of_digits(y)
    if x_n == 1 and x_n == 1:
        return x * y

    first_coef = 10 ** (x_n)
    second_coef = 10 ** (x_n/2)
    a, b = separate_number(x)
    c, d = separate_number(y)

    ac = karatsuba(a,c)
    bd = karatsuba(b,d)
    ad_bc = karatsuba(a+b, c+d) - ac - bd

    return first_coef * ac + second_coef * ad_bc + bd

class TestGeneral(unittest.TestCase):

    def test_number_of_digits(self):
        self.assertEqual(1, number_of_digits(1))
        self.assertEqual(2, number_of_digits(10))
        self.assertEqual(3, number_of_digits(100))
        self.assertEqual(4, number_of_digits(1000))

    def test_separate_number(self):
        self.assertEqual((1,1), separate_number(1))
        self.assertEqual((1,0), separate_number(10))
        self.assertEqual((10,0), separate_number(1000))
        self.assertEqual((12,34), separate_number(1234))
        self.assertEqual((56,78), separate_number(5678))

    def test_multiplication(self):
        self.assertEqual(1*1, karatsuba(1, 1))
        self.assertEqual(12*12, karatsuba(12, 12))
        self.assertEqual(1234*5678, karatsuba(1234, 5678))

if __name__ == '__main__':
    unittest.main()
