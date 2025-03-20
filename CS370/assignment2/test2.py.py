import numpy as np

# Define the input and output matrices
V = np.array([[1, -1, 0], [1, 0, -1], [-8, 6, -3]])
W = np.array([[1, 2, 6], [3, 4, 1], [1, 1, -1]])

# Calculate the matrix A
A = np.dot(W, np.linalg.inv(V))

print(A)
