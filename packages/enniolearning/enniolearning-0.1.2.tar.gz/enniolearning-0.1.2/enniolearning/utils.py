import numpy as np
from functools import reduce
from operator import or_
import pandas as pd
import torch


# https://www.geeksforgeeks.org/longest-common-subarray-in-the-given-two-arrays/
# Python program to DP approach
# to above solution

# Function to find the maximum
# length of equal subarray
#A and B should be 1 dimension arrays (not 2D arrays) as equality between arrays (even very small) is very long to verify
def FindMaxLength(A, B):
    n = len(A)
    m = len(B)
    # Auxillary dp[][] array
    dp = np.zeros((n + 1, m + 1))  # [[0 for i in range(n + 1)] for i in range(m + 1)]

    # Updating the dp[][] table
    # in Bottom Up approach
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            # If A[i] is equal to B[i]
            # then dp[i][j]= dp[i + 1][j + 1]+1
            if equals(A[i], B[j]):
                dp[i][j] = dp[i + 1][j + 1] + 1
    maxm = 0

    # Find maximum of all the values
    # in dp[][] array to get the
    # maximum length
    for i in dp:
        for j in i:
            # Update the length
            maxm = max(maxm, j)

            # Return the maximum length
    return maxm

def equals(elementA, elementB):
    equality = (elementA == elementB)
    if type(equality) in [bool, np.bool_] :
        return equality
    if type(equality) is np.ndarray:
        return equality.all()
    if type(equality) is torch.Tensor:
        return equality.all().item()
    raise TypeError(f"Unsupported equality type {type(equality)}") 

# # Driver's Code
# if __name__ == '__main__':
# 	A =[1, 2, 8, 2, 1]
# 	B =[8, 2, 1, 4, 7]

# 	# Function call to find
# 	# maximum length of subarray
# 	print(FindMaxLength(A, B))

def detect_repetitions(array, min_pattern_len=2, start_detection_index=0):
    """keys in returns dict is a serialized np.array, which means elements are separated by ' ' (space)"""
    repetitions_count = {}

    for i in range(start_detection_index, len(array) - min_pattern_len + 1):
        #         pattern_len = min_pattern_len #keep increasing it
        #         sub_array = array[i:i+pattern_len]
        #         count_of_sub_array = count_seq(array, sub_array)
        #         if is_repetition(count_of_sub_array, n):
        #             sub_array_key = str(sub_array)
        #             repetitions_count[sub_array_key] = max(count_of_sub_array, repetitions_count.get(sub_array_key, 0))
        recursive_detect_repetitions(array, min_pattern_len, i, repetitions_count)
    #     print(repetitions_count)
    return repetitions_count


def recursive_detect_repetitions(array, pattern_len, from_array_index, repetitions_count):
    if from_array_index + pattern_len < len(array):
        sub_array = array[from_array_index:from_array_index + pattern_len]
        count_of_sub_array = count_seq(array, sub_array)
        if is_repetition(count_of_sub_array, len(array)):
            sub_array_key = str(np.array(sub_array))
            repetitions_count[sub_array_key] = max(count_of_sub_array, repetitions_count.get(sub_array_key, 0))
            recursive_detect_repetitions(array, pattern_len + 1, from_array_index, repetitions_count)


# True if a pattern is found more than 3 times
def is_repetition(nb, total_len):
    return nb > 5


# count_seq([1,4,8,1,2,3,1,2,3,1,2,3,7,4,1,2,3,1,2,3,1,2,3,1,2,3,1,2,3], [1,2,3]) --> 8
def count_seq(array, sub_array):
    n = len(array)
    m = len(sub_array)
    c = 0
    for i in range(n - m + 1):
        #         print("exploring", array[i:i+m])
        if equals(array[i:i + m], sub_array):
            c += 1
    return c


# can be improved with decision algo. now it is only based on key length.
# note that the dict returned by detect_repetitions() has keys iff it fits is_repetition() condition
def reject_for_repetition(array, max_acceptable_repetition_len=15, min_pattern_len=5):
    return reduce(
        or_,  # step 3 : if some repetition is too long (gave True in step 2), reject the sample array
        map(
            lambda l: l > max_acceptable_repetition_len,
            # step 2 : is the repetition too long to be acceptable (in element count) ?
            map(
                lambda k: k.count(' ') + 1,  # get nb of elements in the repetition. np.array serialization puts space between elements
                detect_repetitions(array, min_pattern_len=min_pattern_len).keys()  # step 1 : get repetitions in array
            )
        )
        , False)


#https://github.com/keras-team/keras/blob/e8946d5240f3b18528d4d34668ee615907879953/keras/utils/np_utils.py
def to_categorical(y, num_classes=None, dtype='float32'):
    """Converts a class vector (integers) to binary class matrix.

    E.g. for use with categorical_crossentropy.

    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.
        dtype: The data type expected by the input, as a string
            (`float32`, `float64`, `int32`...)

    # Returns
        A binary matrix representation of the input. The classes axis
        is placed last.

    # Example

    ```python
    # Consider an array of 5 labels out of a set of 3 classes {0, 1, 2}:
    > labels
    array([0, 2, 1, 2, 0])
    # `to_categorical` converts this into a matrix with as many
    # columns as there are classes. The number of rows
    # stays the same.
    > to_categorical(labels)
    array([[ 1.,  0.,  0.],
           [ 0.,  0.,  1.],
           [ 0.,  1.,  0.],
           [ 0.,  0.,  1.],
           [ 1.,  0.,  0.]], dtype=float32)
    ```
    """

    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=dtype)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical


def label_to_int(y):
    """takes a list of labels.
    Returns list of category codes. Easy to combine then with to_categorical()
    """
    df = pd.DataFrame(y, columns=['label'])
    df['label'] = df['label'].astype('category')
    return df['label'].cat.codes