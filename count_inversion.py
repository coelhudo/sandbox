import unittest
import operator
import random

def divide(number):
    if len(number) > 1:
        half = len(number) // 2
        return number[:half], number[half:]

    return number, []

def merge(first, second, op=operator.gt):
    if not (first and second):
        result = first if first else second
        return result, 0

    result = list()
    
    i = 0
    j = 0
    inversion = 0
    len_second = len(second)
    len_first = len(first)
    while True:
        if op(first[i], second[j]):
            result.append(second[j])

            inversion += len(first[i:])
            j += 1
            if j == len_second:
                result.extend(first[i:])
                break
        else:
            result.append(first[i])

            i += 1
            if i == len_first:
                result.extend(second[j:])
                break

    return result, inversion
                
def sort(input, op=operator.gt):
    if len(input) < 2:
        return input, 0

    first, second = divide(input)
    first_sorted, left_inversion = sort(first, op)
    second_sorted, right_inversion = sort(second, op)
    sorted, cross_inversion = merge(first_sorted, second_sorted, op)
    return sorted, left_inversion + right_inversion + cross_inversion

class TestSort(unittest.TestCase):

    def test_divide(self):
        self.assertEqual(([], []), divide([]))
        self.assertEqual(([1], []), divide([1]))
        self.assertEqual(([1], [2]), divide([1,2]))
        self.assertEqual(([1], [2,3]), divide([1,2,3]))
        self.assertEqual(([1,2], [3,4]), divide([1,2,3,4]))
        self.assertEqual(([1,2], [3,4,5]), divide([1,2,3,4,5]))

    def dtest_merge(self):
        self.assertEqual([], merge([], []))
        self.assertEqual([1], merge([], [1]))
        self.assertEqual([1], merge([1], []))
        self.assertEqual([1,2], merge([1], [2]))
        self.assertEqual([1,2], merge([2], [1]))
        self.assertEqual([1,2,3], merge([1], [2,3]))
        self.assertEqual([1,2,3], merge([1,2], [3]))
        self.assertEqual([1,4,5,8], merge([4,5], [1,8]))
        self.assertEqual([1,4,5,7,8], merge([4,5,7], [1,8]))
        self.assertEqual([1,2,3,4,5,6,7,8], merge([1,4,5,8], [2,3,6,7]))

        self.assertEqual([2,1], merge([1], [2], op=operator.lt))

    def test_sort(self):
        self.assertEqual(([], 0), sort([]))
        self.assertEqual(([1], 0), sort([1]))
        self.assertEqual(([1,2], 0), sort([1,2]))
        self.assertEqual(([1,2], 1), sort([2,1]))
        self.assertEqual(([1,2,3], 0), sort([1,2,3]))
        self.assertEqual(([1,2,3], 2), sort([2,3,1]))
        self.assertEqual(([1,2,3], 3), sort([3,2,1]))
        self.assertEqual(([1,2,3], 2), sort([3,1,2]))
        self.assertEqual(([1,2,3,6,9], 4), sort([2,3,6,9,1]))
        self.assertEqual(([1,2,3,4,5], 3), sort([2,4,1,3,5]))
        self.assertEqual(([1,2,3,4,5,6], 3), sort([1,3,5,2,4,6]))
        self.assertEqual(([1,1,1,2,3,4,5,6], 9), sort([1,3,5,1,2,4,1,6]))
        self.assertEqual(([1,2,3,4,5,6,7,8], 15), sort([5,4,1,8,7,2,6,3]))
        self.assertEqual(([8,7,6,5,4,3,2,1], 13), sort([5,4,1,8,7,2,6,3], op=operator.lt))

    def dtest_random_sort(self):
        sample = [int(1000*random.random()) for i in range(10000)]
        sample_copy = sample.copy()
        sample_copy.sort()
        sorted_sample, inversion = sort(sample)
        self.assertEqual(sample_copy, sorted_sample)

    def test_coursera_assignment_one(self):
        with open('intarray.txt') as file_handler:
            int_array_content = file_handler.read().splitlines()
            int_array_content = [int(item) for item in int_array_content]
            _, count_inverted = sort(int_array_content)
            print(count_inverted)
            

if __name__ == '__main__':
    unittest.main()
