'''
Exercise 1 (ungraded). Explain what the following code cell does.
'''

edges_raw_trans = pd.DataFrame({'Source': edges_raw['Target'],
                                'Target': edges_raw['Source']})
edges_raw_symm = pd.concat([edges_raw, edges_raw_trans])
edges = edges_raw_symm.drop_duplicates()

V_names = set(edges['Source'])
V_names.update(set(edges['Target']))

num_edges = len(edges)
num_verts = len(V_names)
print("==> |V| == {}, |E| == {}".format(num_verts, num_edges))

#Convert a data (a,b) in (b,a) and set a construct with unics values

'''
Exercise 2 (3 points). 
Implement a function to compute  y←Ax . 
Assume that the keys of the sparse matrix data structure are integers in the interval  [0,s)  where  s  is the number of rows or columns as appropriate.
'''

def spmv(A, x, num_rows=None): 
    if num_rows is None:
        num_rows = max(A.keys()) + 1
    y = dense_vector(num_rows) 
    
    # Recall: y = A*x is, conceptually,
    # for all i, y[i] == sum over all j of (A[i, j] * x[j])
        
    for i, row_i in A.items():
        s = 0.
        for j, a_ij in row_i.items():
            s += a_ij * x[j]
        y[i] = s
        
    return y

'''
Exercise 3 (3 points). 
Given id2name and name2id as computed above, convert edges into a sparse matrix, G, where there is an entry G[s][t] == 1.0 wherever an edge (s, t) exists.
'''

G = sparse_matrix()

for i in range(len(edges)): 
    s = edges['Source'].iloc[i]
    t = edges['Target'].iloc[i]
    s_id = name2id[s]
    t_id = name2id[t]
    G[s_id][t_id] = 1.0

'''
Exercise 4 (3 points). 
In the above, we asked you to construct G using integer keys. However, since we are, after all, using default dictionaries, we could also use the vertex names as keys. 
Construct a new sparse matrix, H, which uses the vertex names as keys instead of integers.
'''

H = sparse_matrix()

for i in range(len(edges)): 
    s = edges['Source'].iloc[i]
    t = edges['Target'].iloc[i]
    H[s][t] = 1.0

'''
Exercise 5 (3 points). 
Implement a sparse matrix-vector multiply for matrices with named keys. In this case, it will be convenient to have vectors that also have named keys; assume we use dictionaries to hold these vectors as suggested in the code skeleton, below.
'''

def vector_keyed(keys=None, values=0, base_type=float):
    if keys is not None:
        if type(values) is not list:
            values = [base_type(values)] * len(keys)
        else:
            values = [base_type(v) for v in values]
        x = dict(zip(keys, values))
    else:
        x = {}
    return x

def spmv_keyed(A, x):
    """Performs a sparse matrix-vector multiply for keyed matrices and vectors."""
        
    y = vector_keyed(keys=A.keys(), values=0.0)
    
    for i, A_i in A.items():
        for j, a_ij in A_i.items():
            y[i] += a_ij * x[j]
        
    return y

'''
Exercise 6 (3 points). 
Convert the edges[:] data into a coordinate (COO) data structure in native Python using three lists, coo_rows[:], coo_cols[:], and coo_vals[:], to store the row indices, column indices, and matrix values, respectively. Use integer indices and set all values to 1.
'''

coo_rows = [name2id[s] for s in edges['Source']]
coo_cols = [name2id[t] for t in edges['Target']]
coo_vals = [1.0]*len(edges)

'''
Exercise 7 (3 points). 
Implement a sparse matrix-vector multiply routine for COO implementation.
'''

def spmv_coo(R, C, V, x, num_rows=None):
    """
    Returns y = A*x, where A has 'm' rows and is stored in
    COO format by the array triples, (R, C, V).
    """
    if num_rows is None:
        num_rows = max(R) + 1
    
    y = dense_vector(num_rows)
    
    for i, j, a_ij in zip(R, C, V):
        y[i] += a_ij * x[j]
    
    return y

#174 ms ± 5.82 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

'''
Exercise 8 (3 points). 
Now create a CSR data structure, again using native Python lists. Name your output CSR lists csr_ptrs, csr_inds, and csr_vals.

It's easiest to start with the COO representation. We've given you some starter code. Unlike most of the exercises, instead of creating a function, you have to compute csr_ptrs here
'''

from operator import itemgetter
C = sorted(zip(coo_rows, coo_cols, coo_vals), key=itemgetter(0))
nnz = len(C)
assert nnz >= 1

csr_inds = [j for _, j, _ in C]
csr_vals = [a_ij for _, _, a_ij in C]

C_rows = [i for i, _, _ in C] # sorted rows
csr_ptrs = [0] * (num_verts + 1)
i_cur = -1
for k in range(nnz):
    if C_rows[k] != i_cur:
        i_cur = C_rows[k]
        csr_ptrs[i_cur] = k

from itertools import accumulate
csr_ptrs = list(accumulate(csr_ptrs, max))
csr_ptrs[-1] = nnz

'''
Exercise 9 (3 points). Now implement a CSR-based sparse matrix-vector multiply.
'''

def spmv_csr(ptr, ind, val, x , num_rows=None):
	 y = dense_vector(num_rows)
    
        for i in range(num_rows):
        for k in range(ptr[i], ptr[i+1]):
            y[i] += val[k] * x[ind[k]]
    
    return y

#188 ms ± 5.8 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)