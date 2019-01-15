'''
Exercise 3 (2 points). 
Implement the logistic function. Inspect the resulting plot of  G(y)G(y)  in 1-D and then the contour plot of  G(θTx)G(θTx) . Your function should accept a Numpy matrix of values, Y, and apply the sigmoid elementwise.
'''
def logistic(Y):
    return 1.0 / (1.0 + np.exp (-Y))
    
# Plot your function for a 1-D input.
y_values = np.linspace(-10, 10, 100)

mpl.rc("savefig", dpi=120) # Adjust for higher-resolution figures
sns.set_style("darkgrid")
y_pos = y_values[y_values > 0]
y_rem = y_values[y_values <= 0]
plt.plot(y_rem, heaviside (y_rem), 'b')
plt.plot(y_pos, heaviside (y_pos), 'b')
plt.plot(y_values, logistic (y_values), 'r--')
#sns.regplot (y_values, heaviside (y_values), fit_reg=False)
#sns.regplot (y_values, logistic (y_values), fit_reg=False)

