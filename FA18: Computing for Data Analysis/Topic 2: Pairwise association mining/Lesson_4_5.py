'''
Exercise 4 (update_pair_counts_test: 2 points).
Start by implementing a function that enumerates all item-pairs within an itemset and updates,
in-place, a table that tracks the counts of those item-pairs.
'''

from collections import defaultdict
from itertools import combinations # Hint!

def update_pair_counts (pair_counts, itemset):
    """
    Updates a dictionary of pair counts for
    all pairs of items in a given itemset.
    """
    assert type (pair_counts) is defaultdict
    for a, b in combinations(itemset, 2):
        pair_counts[(a, b)] += 1
        pair_counts[(b, a)] += 1

'''
Exercise 5 (update_item_counts_test: 2 points). 
Implement a procedure that, given an itemset, updates a table to track counts of each item.

As with the previous exercise, you may assume all items in the given itemset (itemset) are distinct, i.e., 
that you may treat it as you would any set-like collection. You may also assume the table (item_counts) is a default dictionary.
'''

def update_item_counts(item_counts, itemset):
    for a in itemset:
        item_counts[a] += 1