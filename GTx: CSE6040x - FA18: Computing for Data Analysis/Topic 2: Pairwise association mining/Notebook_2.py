latin_text = """
Sed ut perspiciatis, unde omnis iste natus error sit
voluptatem accusantium doloremque laudantium, totam
rem aperiam eaque ipsa, quae ab illo inventore
veritatis et quasi architecto beatae vitae dicta
sunt, explicabo. Nemo enim ipsam voluptatem, quia
voluptas sit, aspernatur aut odit aut fugit, sed
quia consequuntur magni dolores eos, qui ratione
voluptatem sequi nesciunt, neque porro quisquam est,
qui dolorem ipsum, quia dolor sit amet consectetur
adipisci[ng] velit, sed quia non numquam [do] eius
modi tempora inci[di]dunt, ut labore et dolore
magnam aliquam quaerat voluptatem. Ut enim ad minima
veniam, quis nostrum exercitationem ullam corporis
suscipit laboriosam, nisi ut aliquid ex ea commodi
consequatur? Quis autem vel eum iure reprehenderit,
qui in ea voluptate velit esse, quam nihil molestiae
consequatur, vel illum, qui dolorem eum fugiat, quo
voluptas nulla pariatur?

At vero eos et accusamus et iusto odio dignissimos
ducimus, qui blanditiis praesentium voluptatum
deleniti atque corrupti, quos dolores et quas
molestias excepturi sint, obcaecati cupiditate non
provident, similique sunt in culpa, qui officia
deserunt mollitia animi, id est laborum et dolorum
fuga. Et harum quidem rerum facilis est et expedita
distinctio. Nam libero tempore, cum soluta nobis est
eligendi optio, cumque nihil impedit, quo minus id,
quod maxime placeat, facere possimus, omnis voluptas
assumenda est, omnis dolor repellendus. Temporibus
autem quibusdam et aut officiis debitis aut rerum
necessitatibus saepe eveniet, ut et voluptates
repudiandae sint et molestiae non recusandae. Itaque
earum rerum hic tenetur a sapiente delectus, ut aut
reiciendis voluptatibus maiores alias consequatur
aut perferendis doloribus asperiores repellat.
"""

print("First 100 characters:\n  {} ...".format(latin_text[:100]))

'''
Exercise 1 (normalize_string_test: 2 points). 
Complete the following function, normalize_string(s). The input s is a string (str object). The function should return a new string with 
(a) all characters converted to lowercase and 
(b) all non-alphabetic, non-whitespace characters removed.
'''

def normalize_string(s):
    assert type(s) is str
    s = s.replace(',' , '')
    s = s.replace('.', '')
    s = s.replace('[', '')
    s = s.replace(']', '')
    s = s.replace('?', '')
    s = s.lower()
    return s

# Demo:
print(latin_text[:100], "...\n=>", normalize_string(latin_text), "...")

'''
Exercise 2 (get_normalized_words_test: 1 point). Implement the following function, get_normalized_words(s). It takes as input a string s 
(i.e., a str object). It should return a list of the words in s, after normalization per the definition of normalize_string(). 
(That is, the input s may not be normalized yet.)
'''

def get_normalized_words (s):
    assert type (s) is str
    s = s.split()
    s = list(s)
    return s

# Demo:
print ("First five words:\n{}".format (get_normalized_words (latin_text)[:5]))

'''
Exercise 3 (make_itemsets_test: 2 points). Implement a function, make_itemsets(words). The input, words, is a list of strings. 
Your function should convert the characters of each string into an itemset and then return the list of all itemsets. 
These output itemsets should appear in the same order as their corresponding words in the input.
'''

def make_itemsets(words):
    return [set(w) for w in words]

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


'''
Exercise 6 (filter_rules_by_conf_test: 2 points).
Given tables of item-pair counts and individual item counts, as well as a confidence threshold,
return the rules that meet the threshold. The returned rules should be in the form of a dictionary whose key is the tuple,  (a,b)(a,b)  corresponding to the rule  a⇒ba⇒b , and whose value is the confidence of the rule,  conf(a⇒b)conf(a⇒b) .

You may assume that if  (a,b)(a,b)  is in the table of item-pair counts, then both  aa  and  bb  are in the table of individual item counts.
'''

def filter_rules_by_conf (pair_counts, item_counts, threshold):
    rules = {} # (item_a, item_b) -> conf (item_a => item_b)
    for (a, b) in pair_counts:
        conf_ab = pair_counts[(a, b)] / item_counts[a]
        if conf_ab >= threshold:
            rules[(a, b)] = conf_ab

    return rules

'''
Exercise 7 (find_assoc_rules_test: 3 points). Using the building blocks you implemented above, complete a function find_assoc_rules so that it implements the basic association rule mining algorithm and returns a dictionary of rules.

In particular, your implementation may assume the following:

As indicated in its signature, below, the function takes two inputs: receipts and threshold.
1.The input, receipts, is a collection of itemsets: for every receipt r in receipts, r may be treated as a collection of unique items.
2.The input threshold is the minimum desired confidence value. That is, the function should only return rules whose confidence is at least threshold.
3.The returned dictionary, rules, should be keyed by tuples  (a,b)(a,b)  corresponding to the rule  a⇒ba⇒b ; each value should the the confidence  conf(a⇒b)conf(a⇒b)  of the rule.
'''

def find_assoc_rules(receipts, threshold):
    pair_counts = defaultdict(int)
    item_counts = defaultdict(int)
    for itemset in receipts:
        update_pair_counts(pair_counts, itemset)
        update_item_counts(item_counts, itemset)

    rules = filter_rules_by_conf(pair_counts, item_counts, threshold)
    return  rules

'''
Exercise 8 (latin_rules_test: 2 points). 
For the Latin string, latin_text, use your find_assoc_rules() function to compute the rules whose confidence is at least 0.75. 
Store your result in a variable named latin_rules.
'''

latin_words = get_normalized_words(latin_text)
latin_itemsets = make_itemsets(latin_words)
latin_rules = find_assoc_rules(latin_itemsets, 0.75)

print_rules(latin_rules)