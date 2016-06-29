import unittest
import operator
import random

def divide(number):
    if len(number) > 1:
        half = len(number) // 2
        return number[:half], number[half:]

    return number, []

def merge(first, second, op=operator.gt):
    #return recursive_merge(first, second, op)
    return iterative_merge(first, second, op)


def recursive_merge(first, second, op):
    if not (first and second):
        result = first if first else second
        return result

    if op(first[0], second[0]):
        result = second[:1]
        result.extend(recursive_merge(first, second[1:], op))
        return result

    result = first[:1]
    result.extend(recursive_merge(first[1:], second, op))
    return result

def iterative_merge(first, second, op):
    if not (first and second):
        result = first if first else second
        return result

    first_it = iter(first)
    second_it = iter(second)
    i = next(first_it)
    j = next(second_it)
    result = list()
    while True:
        if op(i,j):
            result.append(j)
            try:
                j = next(second_it)
            except StopIteration:
                result.append(i)
                result.extend(first_it)
                break
        else:
            result.append(i)
            try:
                i = next(first_it)
            except StopIteration:
                result.append(j)
                result.extend(second_it)
                break

    return result
                
def sort(input, op=operator.gt):
    if len(input) < 2:
        return input

    first, second = divide(input)
    first_sorted = sort(first, op)
    second_sorted = sort(second, op)
    return merge(first_sorted, second_sorted, op)

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
        self.assertEqual([], sort([]))
        self.assertEqual([1], sort([1]))
        self.assertEqual([1,2], sort([1,2]))
        self.assertEqual([1,2], sort([2,1]))
        self.assertEqual([1,2,3], sort([1,2,3]))
        self.assertEqual([1,2,3], sort([2,3,1]))
        self.assertEqual([1,2,3], sort([3,2,1]))
        self.assertEqual([1,2,3], sort([3,1,2]))
        self.assertEqual([1,2,3,4,5,6,7,8], sort([5,4,1,8,7,2,6,3]))
        self.assertEqual([8,7,6,5,4,3,2,1], sort([5,4,1,8,7,2,6,3], op=operator.lt))

    def test_random_sort(self):
        sample = [int(1000*random.random()) for i in range(10000)]
        sample_copy = sample.copy()
        sample_copy.sort()
        self.assertEqual(sample_copy, sort(sample))



if __name__ == '__main__':
    unittest.main()
