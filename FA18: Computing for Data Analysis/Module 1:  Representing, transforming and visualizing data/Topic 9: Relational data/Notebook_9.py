'''Exercise 1 (2 points). 
Suppose we wish to maintain a second table, called Takes, which records classes that students have taken and the grades they earn.

In particular, each row of Takes stores a student by his/her GT ID, the course he/she took, and the grade he/she earned in terms of GPA (i.e. 4.0, 3.0, etc). More formally, suppose this table is defined as follows:'''

data = [
    (123, 'CSE 6040', 4.0),
    (123, 'ISYE 6644', 3.0),
    (123, 'MGMT 8803', 1.0),
    (991, 'CSE 6040', 4.0),
    (991, 'ISYE 6740', 4.0),
    (456, 'CSE 6040', 4.0),
    (456, 'CSE 6740', 2.0),
    (456, 'MGMT 8803', 3.0)
]
c.executemany('INSERT INTO Takes VALUES (?, ?, ?)', data)
conn.commit()
conn.close()


c.execute('SELECT * FROM Takes')
results = c.fetchall()
print("Your results:", len(results), "\nThe entries of Takes:", results)

'''
INNER JOIN(A, B): Keep rows of A and B only where A and B match
OUTER JOIN(A, B): Keep all rows of A and B, but merge matching rows and fill in missing values with some default (NaN in Pandas, NULL in SQL)
LEFT JOIN(A, B): Keep all rows of A but only merge matches from B.
RIGHT JOIN(A, B): Keep all rows of B but only merge matches from A.
'''

'''
Exercise 2 (2 points). 
Define a query to select only the names and grades of students who took CSE 6040. The code below will execute your query and store the results in a list results1 of tuples, where each tuple is a (name, grade) pair; 
thus, you should structure your query to match this format.
'''

# Define `query` with your query:
query = '''
        SELECT Students.name, Takes.grade
        FROM Students, Takes
        WHERE Students.gtid = Takes.gtid AND Takes.course = 'CSE 6040'
'''

c.execute(query)
results1 = c.fetchall()
print(results1)

'''
Exercise 3 (2 points). 
Execute a LEFT JOIN that uses Students as the left table, Takes as the right table, and selects a student's name and course grade. 
Write your query as a string variable named query, which the subsequent code will execute.
'''

# Define `query` string here:
query = '''
        SELECT Students.name, Takes.grade
        FROM Students LEFT JOIN Takes ON
        Students.gtid = Takes.gtid
'''

# Executes your `query` string:
c.execute(query)
matches = c.fetchall()
for i, match in enumerate(matches):
    print(i, "->", match)