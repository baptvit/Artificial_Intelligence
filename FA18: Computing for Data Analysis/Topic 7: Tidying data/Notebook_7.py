'''
Exercise 1 (ungraded). Run the following commands to understand what each one does. 
If it's not obvious, try reading the Pandas documentation or going online to get more information.
'''

print("\n=== `irises.describe()`: Prints summary statistics ===\n\n{}".format(irises.describe()))
print("\n=== `irises['sepal length'].head()`: Dumps the first few rows of a given column ===\n\n{}".format(irises['sepal length'].head()))
print('\n=== `irises[["sepal length", "petal width"]].head()`: Dumps the first few rows of several specific columns ===\n\n{}'.format(irises[["sepal length", "petal width"]].head()))
print("\n=== `irises.iloc[5:10]`: Selects rows at a certain integer offset and range ===\n\n{}".format(irises.iloc[5:10]))
print('\n=== `irises[irises["sepal length"] > 5.0]`: Selects the subset of rows satisfying some condition (here, where sepal length is strictly more than 5) ===\n\n{}'.format(irises[irises["sepal length"] > 5.0]))
print('\n=== `irises["sepal length"].max()`: Returns the largest value of a given column ===\n\n{}'.format(irises["sepal length"].max()))
print("\n=== `irises['species'].unique()`: Returns a list of unique values in a given column ===\n\n{}".format(irises['species'].unique()))
print('\n=== `irises.sort_values(by="sepal length", ascending=False).head(1)`: Returns the observation with the longest sepal length ===\n\n{}'.format(irises.sort_values(by="sepal length", ascending=False).head(1)))
print('\n=== `irises.sort_values(by="sepal length", ascending=False).iloc[5:10]`: Returns the observations whose ranks, in highest sepal length, are 5-9 inclusive ===\n\n{}'.format(irises.sort_values(by="sepal length", ascending=False).iloc[5:10]))
print('\n=== `irises.sort_values(by="sepal length", ascending=False).loc[5:10]`: Returns the observations between the one whose row ID is 5 and the one that is 10, in order of sepal-length, 5 and 10 are inclusive ===\n\n{}'.format(irises.sort_values(by="sepal length", ascending=False).loc[5:10]))

irises['x'] = 3.14
print("\n=== `irises['x'] = 3.14`: Creates a new column (variable) named ‘x’ and sets all values in column = 3.14 ===\n\n{}".format(irises.head()))

irises2 = irises.rename(columns={'species': 'type'})
print("\n=== irises.rename(columns={{'species': 'type'}}): Change the name of a column (variable) ===\n\n{}".format(irises2))

del irises['x']
print("\n=== `del irises['x']`: Removes a column ===\n\n{}".format(irises.head()))

'''
Exercise 2 (2 points). Suppose you wish to compute the prevalence, which is the ratio of cases to the population.

The simplest way to do it is as follows:

    G['prevalence'] = G['cases'] / G['population']
However, for this exercise, try to figure out how to use apply() to do it instead. To figure that out, you'll need to consult the documentation for apply() or go online to find some hints.

Implement your solution in a function, calc_prevalence(G), which given G returns a new copy H that has a column named 'prevalence' holding the correctly computed prevalence values
'''

def calc_prevalence(G):
    assert 'cases' in G.columns and 'population' in G.columns
    
    def calc_ratio(observation):
        return observation['cases'] / observation['population']
    
    H = G.copy()
    H['prevalence'] = H.apply(calc_ratio, axis=1)
    return H

'''
Exercise 3 (3 points). Write a function, canonicalize_tibble(X), that, given a tibble X, returns a new copy Y of X in canonical order. We say Y is in canonical order if it has the following properties.

The variables appear in sorted order by name, ascending from left to right.
The rows appear in lexicographically sorted order by variable, ascending from top to bottom.
The row labels (Y.index) go from 0 to n-1, where n is the number of observations.
'''

def canonicalize_tibble(X):
    # Enforce Property 1:
    var_names = sorted(X.columns)
    Y = X[var_names].copy()

    Y.sort_values(by=var_names, inplace=True)
    
    Y.reset_index(drop=True, inplace=True)
    return Y

 '''
Exercise 4 (1 point). Write a function, tibbles_are_equivalent(A, B) to determine if two tibbles, A and B, are equivalent. "Equivalent" means that A and B have identical variables and observations, up to permutations. 
If A and B are equivalent, then the function should return True. Otherwise, it should return False.
 '''

 def tibbles_are_equivalent(A, B):
    """Given two tidy tables ('tibbles'), returns True iff they are
    equivalent.
    """
    ### BEGIN SOLUTION
    A_hat = canonicalize_tibble(A)
    B_hat = canonicalize_tibble(B)
    equal = (A_hat == B_hat)
    return equal.all().all()

'''
Exercise 5 (4 points). Implement the melt operation as a function,

    def melt(df, col_vals, key, value):
        ...
It should take the following arguments:

df: the input data frame, e.g., table4 in the example above;
col_vals: a list of the column names that will serve as values; column 1999 & 2000 in example table
key: name of the new variable, e.g., year in the example above;
value: name of the column to hold the values. cases in the example above
'''

def melt(df, col_vals, key, value):
    assert type(df) is pd.DataFrame
   
    keep_vars = df.columns.difference(col_vals)
    melted_sections = []
    for c in col_vals:
        melted_c = df[keep_vars].copy()
        melted_c[key] = c
        melted_c[value] = df[c]
        melted_sections.append(melted_c)
    melted = pd.concat(melted_sections)
    return melted

'''
Exercise 6 (4 points). Implement a function to cast a data frame into a tibble, given a key column containing new variable names and a value column containing the corresponding cells.

We've given you a partial solution that

verifies that the given key and value columns are actual columns of the input data frame;
computes the list of columns, fixed_vars, that should remain unchanged; and
initializes and empty tibble.
'''
def cast(df, key, value, join_how='outer'):
    """Casts the input data frame into a tibble,
    given the key column and value column.
    """
    assert type(df) is pd.DataFrame
    assert key in df.columns and value in df.columns
    assert join_how in ['outer', 'inner']
    
    fixed_vars = df.columns.difference([key, value])
    tibble = pd.DataFrame(columns=fixed_vars) # empty frame
    
  
    new_vars = df[key].unique()
    for v in new_vars:
        df_v = df[df[key] == v]
        del df_v[key]
        df_v = df_v.rename(columns={value: v})
        tibble = tibble.merge(df_v,
                              on=list(fixed_vars),
                              how=join_how)
      
    return tibble

'''
Exercise 6 (3 points). Write a function that takes a data frame (df) and separates an existing column (key) into new variables (given by the list of new variable names, into).

How will the separation happen? The caller should provide a function, splitter(x), that given a value returns a list containing the components. 
Observe that the partial solution below defines a default splitter, which uses the regular expression, (\d+\.?\d+), to find all integer or floating-point values in a string input x.
'''
import re

def default_splitter(text):
    """Searches the given spring for all integer and floating-point
    values, returning them as a list _of strings_.
    
    E.g., the call
    
      default_splitter('Give me $10.52 in exchange for 91 kitten stickers.')
      
    will return ['10.52', '91'].
    """
    fields = re.findall('(\d+\.?\d+)', text)
    return fields

def separate(df, key, into, splitter=default_splitter):
    """Given a data frame, separates one of its columns, the key,
    into new variables.
    """
    assert type(df) is pd.DataFrame
    assert key in df.columns
    
    # Hint: http://stackoverflow.com/questions/16236684/apply-pandas-function-to-column-to-create-multiple-new-columns

    
    def apply_splitter(text):
        fields = splitter(text)
        return pd.Series({into[i]: f for i, f in enumerate (fields)})

    fixed_vars = df.columns.difference([key])
    tibble = df[fixed_vars].copy()
    tibble_extra = df[key].apply(apply_splitter)
    return pd.concat([tibble, tibble_extra], axis=1)
    