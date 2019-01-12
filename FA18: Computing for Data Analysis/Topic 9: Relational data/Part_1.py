'''
Exercise 1 (2 points). 
Create a string, query, containing an SQL query that will return the number of complaints by type. 
The columns should be named type and freq, and the results should be sorted in descending order by freq

What is the most common type of complaint? What, if anything, does it tell you about NYC?
A:  Heat/Hot water with 241430 complains.

'''


del query

# Define a variable named `query` containing your solution
query = '''
	SELECT ComplaintType AS type, COUNT(*) AS freq
    FROM data
    GROUP BY type
    ORDER BY -freq
'''

# Runs your `query`:
df_complaint_freq = pd.read_sql_query(query, disk_engine)
df_complaint_freq.head()

'''
Exercise 2 (2 points). 
Create a string variable, query, that contains an SQL query that will return the top 10 cities with the largest number of complaints, in descending order. 
It should return a table with two columns, one named name holding the name of the city, and one named freq holding the number of complaints by that city.
'''

del query

# Define your `query`, here:
query = '''
  SELECT City AS name, COUNT(*) AS freq
    FROM data
    GROUP BY name
    ORDER BY -freq LIMIT 10
'''
# Runs your `query`:
df_whiny_cities = pd.read_sql_query(query, disk_engine)
df_whiny_cities

'''
Exercise 3 (1 point). 
Implement a function that takes a list of strings, str_list, and returns a single string consisting of each value, str_list[i], enclosed by double-quotes and separated by a comma-space delimiters. 
'''

def strs_to_args(str_list):
    quoted = ['"{}"'.format(s) for s in str_list]
    return ', '.join(quoted)

'''
Exercise 4 (3 points). 
Suppose we want to look at the number of complaints by type and by city for only the top cities, i.e., those in the list TOP_CITIES computed above. 
Execute an SQL query to produce a tibble named df_complaints_by_city with the variables {complaint_type, city_name, complaint_count}.
'''

query = """
SELECT complainttype AS complaint_type, city AS city_name, COUNT(*) AS complaint_count
FROM data
WHERE city IN ({})
GROUP BY City, complainttype
ORDER BY City, complaint_count
""".format(strs_to_args(TOP_CITIES))

df_complaints_by_city = pd.read_sql_query(query, disk_engine)


# Previews the results of your query:
display(df_complaints_by_city.head(10))

'''
Exercise 5 (2 points). 
Suppose we want to create a different stacked bar plot that shows, for each complaint type  t  and city  c , the fraction of all complaints of type  t  that occurred in city  c . Store your result in a dataframe named df_plot_fraction. 
It should have the same columns as df_plot, except that the complaint_count column should be replaced by one named complaint_frac, which holds the fractional values.
'''

df_plot_fraction = df_plot.copy()
df_plot_fraction['complaint_frac'] = df_plot['complaint_count'] / df_plot['freq']
del df_plot_fraction['complaint_count']

df_plot_fraction.head()

'''
Exercise 6 (3 points). 
Construct a tibble called df_complaints_by_hour, which contains the total number of complaints during a given hour of the day. 
That is, the variables should be {hour, count} where each observation is the total number of complaints (count) that occurred during a given hour.

Interpret hour as follows: when hour is 02, that corresponds to the open time interval [02:00:00, 03:00:00.0).
'''

# Your task: Construct `df_complaints_by_hour` as directed.
query = '''
  SELECT strftime ('%H', CreatedDate) AS hour, COUNT(*) AS count
    FROM data 
    GROUP BY hour
'''
df_complaints_by_hour = pd.read_sql_query (query, disk_engine)

# Displays your answer:
display(df_complaints_by_hour)

#Problem with default timestamp 00:00:00
'''
Exercise 7 (2 points). 
What is the most common hour for noise complaints? Compute a tibble called df_noisy_by_hour whose variables are {hour, count} and whose observations are the number of noise complaints that occurred during a given hour. Consider a "noise complaint" to be any complaint string containing the word noise. 
Be sure to filter out any dates without an associated time, i.e., a timestamp of 00:00:00.000.
'''
#23h has the most complait count.

query = '''
  SELECT strftime('%H', CreatedDate) AS hour,
         COUNT(*) AS count
    FROM data
    WHERE (ComplaintType LIKE '%noise%')
      AND (strftime('%H:%M:%f', CreatedDate) <> '00:00:00.000')
    GROUP BY hour 
    ORDER BY count
'''
df_noisy_by_hour = pd.read_sql_query(query, disk_engine)

display(df_noisy_by_hour)