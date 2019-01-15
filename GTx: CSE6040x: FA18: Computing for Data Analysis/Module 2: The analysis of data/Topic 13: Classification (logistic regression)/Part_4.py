'''
Exercise 8 (2 points). 
Implement a function to compute the gradient of the log-likelihood. Your function should have the signature,
'''

def grad_log_likelihood(theta, y, X):
    """Returns the gradient of the log-likelihood."""
    
    return X.T.dot(y - logistic(X.dot(theta)))

'''
Exercise 9 (4 points). 
Implement the gradient ascent procedure to determine  θ , and try it out on the sample data.

Recall the procedure (repeated from above):
'''

ALPHA = 0.1
MAX_STEP = 250

# Get the data coordinate matrix, X, and labels vector, y
X = points
y = labels.astype(dtype=float)

# Store *all* guesses, for subsequent analysis
thetas = np.zeros((3, MAX_STEP+1))

for t in range(MAX_STEP):
    # Fill in the code to compute thetas[:, t+1:t+2]

    theta_t = thetas[:, t:t+1]
    delta_t = grad_log_likelihood(theta_t, y, X)
    delta_t = delta_t / np.linalg.norm(delta_t, ord=2)
    thetas[:, t+1:t+2] = theta_t + ALPHA*delta_t
    
    
theta_ga = thetas[:, MAX_STEP:]
print("Your (hand) solution:", my_theta.T.flatten())
print("Computed solution:", theta_ga.T.flatten())

print("\n=== Comparisons ===")
display(Math (r'\dfrac{\theta_0}{\theta_2}:'))
print("Your manual (hand-picked) solution is", my_theta[0]/my_theta[2], \
      ", vs. MLE (via gradient ascent), which is", theta_ga[0]/theta_ga[2])
display(Math (r'\dfrac{\theta_1}{\theta_2}:'))
print("Your manual (hand-picked) solution is", my_theta[1]/my_theta[2], \
      ", vs. MLE (via gradient ascent), which is", theta_ga[1]/theta_ga[2])

print("\n=== The MLE solution, visualized ===")
ga_labels = gen_lin_discr_labels(points, theta_ga)
df_ga = df.copy()
df_ga['label'] = mark_matches(ga_labels, labels).astype (dtype=int)
plot_lin_discr(theta_ga, df_ga)