import numpy as np

'''
Exercise 0 (ungraded).
One reason to consider Numpy is that it "can be much faster," as noted above.
But how much faster is that? Run the experiment below to see.
'''

n = 1000000

L = range(n)
%timeit [i**2 for i in L]
# 269 ms ± 729 µs per loop (mean ± std. dev. of 7 runs, 1 loop each)

np.arange(10)  # Moral equivalent to `range`

A = np.arange(n)
%timeit A**2

#699 µs ± 5.51 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

'''
Exercise 1 (ungraded). 
The following code creates an identity matrix in two different ways, which are found to be equal according to the assertion. 
But in fact there is a subtle difference between the I and I_u matrices created below; can you spot it?
'''
n = 3
I = np.eye(n)

print("==> I = eye(n):")
print(I)

u = [1] * n
I_u = np.diag(u)

print("\n==> u:\n", u)
print("==> I_u = diag (u):\n", I_u)

assert np.all(I_u == I)

#Difference is between types, eyes is a float-point numbers, while daig is integer.

'''
Exercise 2 (5 points). Consider the following  6×66×6  matrix, which has 4 different subsets highlighted.
For each subset illustrated above, write an indexing or slicing expression that extracts the subset. 
Store the result of each slice into Z_green, Z_red, Z_orange, and Z_cyan.
'''

Z= np.array([[0,1,2,3,4,5],[10,11,12,13,14,15],[20,21,22,23,24,25],[30,31,32,33,34,35],[40,41,42,43,44,45],[50,51,52,53,54,55]])

# Construct `Z_green`, `Z_red`, `Z_orange`, and `Z_cyan`:
Z_orange = Z[0, 3:5]
Z_red = Z[:, 2]
Z_green = Z[2::2, ::2]
Z_cyan = Z[4:, 4:]

'''
Exercise 3 (1 point). 
Given the input array, x[:], above, create an array, mask_mult_3[:] such that mask_mult_3[i] is true only if x[i] is a positive multiple of 3.
'''

mask_mult_3 = (x > 0) & (x % 3 == 0)

'''
Exercise 4 (3 points). Complete the prime number sieve algorithm, which is illustrated below.
'''

from math import sqrt


def sieve(n):
    """
    Returns the prime number 'sieve' shown above.

    That is, this function returns an array `X[0:n+1]`
    such that `X[i]` is true if and only if `i` is prime.
    """
    is_prime = np.empty(n + 1, dtype=bool)  # the "sieve"

    # Initial values
    is_prime[0:2] = False  # {0, 1} are _not_ considered prime
    is_prime[2:] = True  # All other values might be prime

    # Implement the sieving loop

    for k in range(2, int(sqrt(n)) + 1):
        is_prime[2 * k::k] = False


    return is_prime


# Prints your primes
print("==> Primes through 20:\n", np.nonzero(sieve(20))[0])