'''
Exercise 0 (2 points). 
Given a  m×(d+1)m×(d+1)  matrix of augmented points (i.e., the  XX  matrix) and a column vector  θθ  of length  d+1d+1 , implement a function to compute the value of the linear discriminant at each point. That is, the function should return a (column) vector  yy  where the  yi=θTx̂ iyi=θTx^i .
'''

def lin_discr (X, theta):
    return X.dot(theta)

'''
Exercise 1 (2 points). Implement the heaviside function,  H(y)H(y) . Your function should allow for an arbitrary matrix of input values and should apply the heaviside function to each element. In the returned matrix, the elements should have a floating-point type.

Example, the code snippet

    A = np.array([[-0.5, 0.2, 0.0],
                  [4.2, 3.14, -2.7]])
    print(heaviside(A))
should display

    [[ 0.  1.  0.]
     [ 1.  1.  0.]]
'''

def heaviside(Y):
    return 1.0*(Y > 0.0)

'''
Exercise 2 (2 points). 
For the synthetic data you loaded above, try by hand to find a value for  θθ  such that  H(θTx)H(θTx)  "best" separates the two clusters. Store this  θθ  in a variable named my_theta, which should be a Numpy column vector. That is, define my_theta here using a line like:
'''

def np_col_vec (list_values):
    """Returns a Numpy column vector for the given list of scalar values."""
    return np.array ([list_values]).T

# Redefine `my_theta` as instructed above to reduce the number of mismatches:
my_theta = np_col_vec([-1., 3., 0.]) # 123 mismatches

my_theta = np_col_vec([-6.5, -1., -1.35]) # 5 mismatches
my_theta = np_col_vec([-2., -0.5, -0.55]) # 5 mismatches
