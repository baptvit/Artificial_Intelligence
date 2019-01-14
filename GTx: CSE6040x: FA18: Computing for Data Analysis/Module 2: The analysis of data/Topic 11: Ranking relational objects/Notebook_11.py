'''
Exercise 0 (3 points). 
As a warmup to familiarize yourself with this dataset, complete the following exercise, which has two subparts.

First, use the airport_codes data frame to figure out the integer airport codes (not the three-letter codes) for Atlanta's Hartsfield-Jackson International (ATL) and Los Angeles International (LAX). Store these codes in variables named ATL_ID and LAX_ID, respectively.

Next, determine all direct flight segments that originated at ATL and traveled to LAX. Store the result in a dataframe named flights_atl_to_lax, which should be the corresponding subset of rows from flights.
'''

ATL_ID = 10397
LAX_ID = 12892

ATL_DESC = airport_codes[airport_codes['Code'] == ATL_ID]['Description'].iloc[0]
LAX_DESC = airport_codes[airport_codes['Code'] == LAX_ID]['Description'].iloc[0]
print("{}: ATL -- {}".format(ATL_ID, ATL_DESC))
print("{}: LAX -- {}".format(LAX_ID, LAX_DESC))

is_atl_origin = (flights['ORIGIN_AIRPORT_ID'] == ATL_ID)
is_lax_dest = (flights['DEST_AIRPORT_ID'] == LAX_ID)
is_atl_to_lax = is_atl_origin & is_lax_dest
flights_atl_to_lax = flights[is_atl_to_lax]

# Displays a few of your results
print("Your code found {} flight segments.".format(len(flights_atl_to_lax)))
display(flights_atl_to_lax.head())
#Your code found 586 flight segments.

'''
Exercise 1 (3 points). 
Construct a dataframe, origins_top10, containing the top 10 airports in descending order of outgoing segments. This dataframe should have three columns:

ID: The ID of the airport
Count: Number of outgoing segments.
Description: The plaintext descriptor for the airport that comes from the airport_codes dataframe.
'''
# Rank each origin
origin_ranks = np.argsort(-origins['ORIGIN_COUNT'])
origins_top10 = origins.iloc[origin_ranks[:10]]
origins_top10 = origins_top10.rename(columns={'ORIGIN_AIRPORT_ID': 'ID', 'ORIGIN_COUNT': 'Count'})
origins_top10 = origins_top10.merge(airport_codes, how='left', left_on='ID', right_on='Code')
del origins_top10['Code']

# Prints the top 10, according to your calculation:
origins_top10

'''
Exercise 2 (2 points). 
The preceding code computed a tibble, origins, containing all the unique origins and their number of outgoing flights. Write some code to compute a new tibble, dests, which contains all unique destinations and their number of incoming flights. Its columns should be named DEST_AIRPORT_ID (airport code) and DEST_COUNT (number of direct inbound segments).

The test cell that follows prints the number of unique destinations and the first few rows of your result, as well as some automatic checks.
'''

dests = segments[['DEST_AIRPORT_ID', 'FL_COUNT']].groupby('DEST_AIRPORT_ID', as_index=False).sum()
dests.rename(columns={'FL_COUNT': 'DEST_COUNT'}, inplace=True)

print("Number of unique destinations:", len(dests))
dests.head()

'''
Exercise 3 (2 points). 
Compute a tibble, dests_top10, containing the top 10 destinations (i.e., rows of dests) by inbound flight count. 
The column names should be the same as origins_top10 and the rows should be sorted in decreasing order by count.
'''

dest_ranks = np.argsort(-dests['DEST_COUNT'])
dests_top10 = dests.iloc[dest_ranks[:10]]
dests_top10 = dests_top10.rename(columns={'DEST_AIRPORT_ID': 'ID', 'DEST_COUNT': 'Count'})
dests_top10 = dests_top10.merge(airport_codes, how='left', left_on='ID', right_on='Code')
del dests_top10['Code']

print("Your computed top 10 destinations:")
dests_top10

'''
Exercise 4 (1 point). 
Analogous to the preceding procedure, create a new column called segments['DEST_INDEX'] to hold the integer index of each segment's destination.
'''

dest_indices = airport_codes[['Code']].rename(columns={'Code': 'DEST_AIRPORT_ID'})
dest_indices['DEST_INDEX'] = airport_codes.index
   
segments = segments.merge(dest_indices, on='DEST_AIRPORT_ID', how='left') #Doing the letf join in the tibble
# Visually inspect your result:
segments.head()

'''
Exercise 5 (3 points). 
Add a new column named OUTDEGREE to the segments tibble that holds the outdegrees,  {di}{di} . That is, for each row whose airport index (as opposed to code) is  ii , its entry of OUTDEGREE should be  didi .

For instance, the rows of segments corresponding to airport ABE (code 10135 and matrix index 119) would look like this:
'''

# This `if` removes an existing `OUTDEGREE` column
# in case you run this cell more than once.
if 'OUTDEGREE' in segments.columns:
    del segments['OUTDEGREE']

outdegrees = segments[['ORIGIN_INDEX', 'DEST_INDEX']].groupby('ORIGIN_INDEX', as_index=False).count()
outdegrees.rename(columns={'DEST_INDEX': 'OUTDEGREE'}, inplace=True)
segments = segments.merge(outdegrees, on='ORIGIN_INDEX', how='left')

# Visually inspect the first ten rows of your result:
segments.head(10)

'''
Exercise 6 (2 points). 
With your updated segments tibble, construct a sparse matrix, P, corresponding to the state-transition matrix  PP . Use SciPy's scipy.sparse.coo_matrix() function to construct this matrix.

The dimension of the matrix should be n_airports by n_airports. If an airport does not have any outgoing segments in the data, it should appear as a row of zeroes.
'''

P = sp.sparse.coo_matrix((segments['WEIGHT'],
                          (segments['ORIGIN_INDEX'], segments['DEST_INDEX'])),
                         shape=(n_airports, n_airports))
spy(P)

'''
Exercise 7 (1 point). 
At time  t=0t=0 , suppose the random flyer is equally likely to be at any airport with an outbound segment, i.e., the flyer is at one of the "actual" origins. Create a NumPy vector x0[:] such that x0[i] equals this initial probability of being at airport i.
'''

# Your task: Create `x0` as directed above.

x0 = np.zeros(n_airports)
actual_airport_indices = segments['ORIGIN_INDEX'].unique()
x0[actual_airport_indices] = 1.0 / n_actual

# Visually inspect your result:
def display_vec_sparsely(x, name='x'):
    i_nz = np.argwhere(x).flatten()
    df_x_nz = pd.DataFrame({'i': i_nz, '{}[i] (non-zero only)'.format(name): x[i_nz]})
    display(df_x_nz.head())
    print("...")
    display(df_x_nz.tail())
    
display_vec_sparsely(x0, name='x0')

'''
Exercise 8 (2 points). Given the state-transition matrix P, an initial vector x0, and the number of time steps t_max, complete the function eval_markov_chain(P, x0, t_max) so that it computes and returns  x(tmax)x(tmax) .
'''

def eval_markov_chain(P, x0, t_max):
    x = x0
    for t in range(t_max):
        x = P.T.dot(x)
    return x

T_MAX = 50
x = eval_markov_chain(P, x0, T_MAX)
display_vec_sparsely(x)

print("\n=== Top 10 airports ===\n")
ranks = np.argsort(-x)
top10 = pd.DataFrame({'Rank': np.arange(1, 11),
                      'Code': airport_codes.iloc[ranks[:10]]['Code'],
                      'Description': airport_codes.iloc[ranks[:10]]['Description'],
                      'x(t)': x[ranks[:10]]})
top10[['x(t)', 'Rank', 'Code', 'Description']]



'''
Final Analysy
'''
top10_with_ranks = top10[['Code', 'Rank', 'Description']].copy()

origins_top10_with_ranks = origins_top10[['ID', 'Description']].copy()
origins_top10_with_ranks.rename(columns={'ID': 'Code'}, inplace=True)
origins_top10_with_ranks['Rank'] = origins_top10.index + 1
origins_top10_with_ranks = origins_top10_with_ranks[['Code', 'Rank', 'Description']]

top10_compare = top10_with_ranks.merge(origins_top10_with_ranks, how='outer', on='Code',
                                       suffixes=['_MC', '_Seg'])
top10_compare