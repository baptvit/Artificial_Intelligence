'''
Exercise 11 (0 points). 
Implement a function to compute the Hessian of the log-likelihood. The signature of your function should be,
'''

def hess_log_likelihood(theta, y, X):
    """Returns the Hessian of the log-likelihood."""
    z = X.dot(theta)
    A = np.multiply(X, logistic(z))
    B = np.multiply(X, logistic(-z))
    return -A.T.dot(B)

'''
Exercise 12 (0 points). 
Finish the implementation of a Newton-based MLE procedure for the logistic regression problem.
'''

MAX_STEP = 10

# Get the data coordinate matrix, X, and labels vector, l
X = points
y = labels.astype(dtype=float)

# Store *all* guesses, for subsequent analysis
thetas_newt = np.zeros((3, MAX_STEP+1))

for t in range(MAX_STEP):
    theta_t = thetas_newt[:, t:t+1]
    g_t = grad_log_likelihood(theta_t, y, X)
    H_t = hess_log_likelihood(theta_t, y, X)
    s_t = np.linalg.solve(H_t, -g_t)
    thetas_newt[:, t+1:t+2] = theta_t + s_t
theta_newt = thetas_newt[:, MAX_STEP:]
print ("Your (hand) solution:", my_theta.T.flatten())
print ("Computed solution:", theta_newt.T.flatten())

print ("\n=== Comparisons ===")
display (Math (r'\dfrac{\theta_0}{\theta_2}:'))
print ("Your manual (hand-picked) solution is", my_theta[0]/my_theta[2], \
      ", vs. MLE (via Newton's method), which is", theta_newt[0]/theta_newt[2])
display (Math (r'\dfrac{\theta_1}{\theta_2}:'))
print ("Your manual (hand-picked) solution is", my_theta[1]/my_theta[2], \
      ", vs. MLE (via Newton's method), which is", theta_newt[1]/theta_newt[2])

print ("\n=== The MLE solution, visualized ===")
newt_labels = gen_lin_discr_labels(points, theta_newt)
df_newt = df.copy()
df_newt['label'] = mark_matches(newt_labels, labels).astype (dtype=int)
plot_lin_discr(theta_newt, df_newt)