'''
Exercise 0 (1 point). 
Implement the Python function, f(x0, x1), so that it computes  f(x) 
'''
def f(x0, x1):
    return x0*x0 + x1*x1

'''
Exercise 1 (1 point). 
Implement a function, grad_f(x0, x1), that implements the gradient  ∇xf(x)  shown above. 
It should return a pair of values since the gradient for this  f(x)  has two components.
'''

def grad_f(x0, x1):
    return (2*x0, 2*x1)
    