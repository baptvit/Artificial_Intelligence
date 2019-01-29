'''
Exercise 1 (2 points). 
Let  A  be an  m×n  matrix stored in column-major format. Let  B  be an  m×n  matrix stored in row-major format.

Based on the preceding discussion, recall that these objects will be mapped to 1-D arrays of length  mn , behind the scenes. Let's call the 1-D array representations  A^  and  B^ . Thus, the  (i,j)  element of  a ,  aij , will map to some element  a^u  of  A^ ; similarly,  bij  will map to some element  b^v  of  B^ .

Determine formulae to compute the 1-D index values,  u  and  v , in terms of  {i,j,m,n} . Assume that all indices are 0-based, i.e.,  0≤i≤m−1 ,  0≤j≤n−1 , and  0≤u,v≤mn−1 .
'''

def linearize_colmajor(i, j, m, n): # calculate `u`
    """
    Returns the linear index for the `(i, j)` entry of
    an `m`-by-`n` matrix stored in column-major order.
    """
    return i + j*m

def linearize_rowmajor(i, j, m, n): # calculate `v`
    """
    Returns the linear index for the `(i, j)` entry of
    an `m`-by-`n` matrix stored in row-major order.
    """
    return i*n + j

'''
Exercise 2 (1 point). 
Given a matrix  A , write a function that scales each column,  A(:,j)  by  j . 
Then compare the speed of applying that function to matrices in row and column major order.
'''

def scale_colwise(A):
    """Given a Numpy matrix `A`, visits each column `A[:, j]`
    and scales it by `j`."""
    assert type(A) is np.ndarray
    
    n_cols = A.shape[1] # number of columns
    
    for j in range(n_cols):
        A[:, j] *= j
    
    return A
#311 ms ± 3.08 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) row-major 'C'
#28.3 ms ± 202 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)  Columm-major  'F'

'''
Exercise 3 (3 points). 
Implement a matrix-vector product that operates on native Python lists. 
Assume the 1-D column-major storage of the matrix.
'''

def matvec_py(m, n, A, x):
    """
    Native Python-based matrix-vector multiply, using lists.
    The dimensions of the matrix A are m-by-n, and x is a
    vector of length n.
    """
    y = [0.] * m
    
    for j in range(n):
        for i in range(m):
            y[i] += A[i + j*m] * x[j]
    
    return y
#1.66 s ± 30.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)