print("=== Day 8: NumPy ===")

import numpy as np

numbers = np.array([1, 2, 3, 4, 5])

print(numbers)
print(type(numbers))
print(numbers + 10)
print(numbers *2)
print(numbers ** 2)

print(f"Sum: {numbers.sum()}")
print(f"Mean: {numbers.mean()}")
print(f"Min: {numbers.min()}")
print(f"Max: {numbers.max()}")
print(f"Std: {round(numbers.std(), 2)}")

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix)
print(f"Shape: {matrix.shape}")
print(matrix[0])
print(matrix[0][1])
print(matrix[1][2])

print(matrix)
print(matrix.T)

a = np.array([
    [1, 2],
    [3, 4]])

b = np.array([
    [5, 6],
    [7, 8]
])


print(np.dot(a, b))

zeros = np.zeros((3, 3))
ones = np.ones((2, 4))
random = np.random.rand(3, 3)

print(zeros)
print(ones)
print(random)

flat = np.array([1, 2, 3, 4, 5, 6])
print(flat)
print(flat.shape)

reshaped = flat.reshape(2, 3)
print(reshaped)
print(reshaped.shape)

numbers = np.array([10, 20 ,30 ,40, 50])

print(numbers[1:4])
print(numbers[:3])
print(numbers[2:])

matrix = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])

print(matrix[0:2, :])

print(matrix[:, 1])