'''
Exercise 0 (2 points). 
Complete the function below so that it computes  αα  and  ββ  for the univariate model,  y∼α⋅x+βy∼α⋅x+β , given observations stored as NumPy arrays y[:] for the responses and x[:] for the predictor.

Use the linear regression formulas derived in class.
'''

def linreg_fit(x, y):
    """Returns (alpha, beta) s.t. y ~ alpha*x + beta."""
    from numpy import ones
    m = len(x) ; assert len(y) == m
    
    u = ones(m)
    alpha = x.dot(y) - u.dot(x)*u.dot(y)/m
    alpha /= x.dot(x) - (u.dot(x)**2)/m
    beta = u.dot(y - alpha*x)/m

    return (alpha, beta)

# Compute the coefficients for the LSD data:
x, y = df['lsd_concentration'], df['exam_score']
alpha, beta = linreg_fit(x, y)

print("alpha:", alpha)
print("beta:", beta)
