'''
Exercise 6 (2 points). 
Implement the log-likelihood function in Python by defining a function with the following signature:
'''
def log_likelihood(theta, y, X):
    u = np.ones((len (X), 1)) # column of all ones
    z = X.dot(theta)
    return y.T.dot(z) + u.T.dot(np.log(logistic(-z)))

def log_likelihood_alt(theta, y, X):
    z = X.dot(theta)
    g = logistic(z)
    return y.T.dot(np.log(g)) + (1.0-y).T.dot(np.log(1.0-g))