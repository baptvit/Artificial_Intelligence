'''
Exercise 1 (3 points). 
Implement a function, solve_neq(X, y) that implements Algorithm 1. It should return a Numpy vector containing the model parameter estimates.

Recall the steps of the algorithm as previously outlined:

1.Form the Gramian of  X ,  C≡XTX .
2.Form  b≡XTy .
3.Solve  Cθ∗=b  for  θ∗ .
'''

def solve_neq(X, y):
    C = X.T.dot(X)
    b = X.T.dot(y)
    theta_est = sp.linalg.solve(C, b, sym_pos=True)
    return theta_est

theta_neq = solve_neq(X, y)

print("Your implementation's solution versus the true solution:")
show_2vecs_tibble(theta_neq, theta_true, xname='theta_neq', yname='theta_true', error=True)

'''
Exercise 2 
(1 point). Write a function to calculate the residual norm,  ∥r∥2=∥Xθ∗−y∥2 .
'''

def calc_residual_norm(X, y, theta):
    ### BEGIN SOLUTION
    from numpy.linalg import norm
    return norm(X.dot(theta) - y, ord=2)
    ### END SOLUTION

r_norm_neq = calc_residual_norm(X, y, theta_neq)
print("\nThe squared residual norm:", r_norm_neq)

'''
Exercise 4 
(2 points). Implement a function that returns an  m×n  matrix whose entries are uniformly randomly distributed in the interval,  [0,ϵ]  for a given value of  ϵ .
'''

def random_mat (m, n, eps):
    
    return np.random.random((m, n)) * eps
    

print(random_mat(3, 2, 1e-3))

'''
Exercise 5 (2 points). 
Use your random_mat() function to write another function, perturb_system(X, y, eps), that creates two "perturbations" to the system defined by X and y.

Let  ΔX  be the first perturbation. It should have the same dimensions as  X , and its entries should lie in the interval  [−ϵ,ϵ] . The value of  ϵ  is given by eps.
The second is  Δy , a small perturbation to the response variable,  y . Its entries should also lie in the same interval,  [−ϵ,ϵ] ,
Your function should return a perturbed system,  X+ΔX  and  y+Δy , as a pair.
'''

def perturb_system(X, y, eps):
    
    Delta_X = random_mat(X.shape[0], X.shape[1], 2*eps) - eps
    Delta_y = random_mat(y.shape[0], y.shape[1], 2*eps) - eps
    return X + Delta_X, y + Delta_y
   

EPSILON = 0.1
X_perturbed, y_perturbed = perturb_system(X, y, EPSILON)

Delta_X = X_perturbed - X
Delta_y = y_perturbed - y
display(Math(r'\Delta X = {}, \quad \Delta y = {}'.format(nparray_to_bmatrix(Delta_X[:5, :]),
                                                          nparray_to_bmatrix(Delta_y[:5]))))