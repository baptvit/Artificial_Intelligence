'''
Exercise 0 (1 point).
Create a new function that checks whether a given input string is a properly formatted social security number, i.e., has the pattern, XXX-XX-XXXX, including the separator dashes, where each X is a digit.
It should return True if so or False otherwise.
'''

def is_ssn (s):
    parts = s.split('-')
    correct_lengths = [3, 2, 4]
    if len(parts) != len(correct_lengths):
        return False
    for p, n in zip(parts, correct_lengths):
        if not (p.isdigit() and len(p) == n):
            return False
    return True

'''
Exercise 1 (2 points). Write a function parse_email that, given an email address s, returns a tuple, (user-id, domain) corresponding to the user name and domain name.

For instance, given richie@cc.gatech.edu it should return (richie, cc.gatech.edu).

Your function should parse the email only if it exactly matches the email specification. For example, if there are leading or trailing spaces, the function should not match those. See the test cases for examples.

If the input is not a valid email address, the function should raise a ValueError.
'''

def parse_email (s):
    pattern = '''
       ^
       (?P<user>[a-zA-Z][\w.\-+]*)
       @
       (?P<domain>[\w.\-]*[a-zA-Z])
       $
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group('user'), matches.group('domain'))
    raise ValueError("Bad email address")
'''
Exercise 2 (2 points). Write a function to parse US phone numbers written in the canonical "(404) 555-1212" format, i.e., a three-digit area code enclosed in parentheses followed by a seven-digit local number in three-hyphen-four digit format. It should also ignore all leading and trailing spaces, as well as any spaces that appear between the area code and local numbers. However, it should not accept any spaces in the area code (e.g., in '(404)') nor should it in the seven-digit local number.

It should return a triple of strings, (area_code, first_three, last_four).

If the input is not a valid phone number, it should raise a ValueError.
'''

def parse_phone1 (s):
    pattern = '''
       \s*
       \((?P<area>\d{3})\) # (Area code)
       \s*
       (?P<local3>\d{3}) # (3 digits)
       -
       (?P<local4>\d{4}) # (4 digits)
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches:
        return (matches.group('area'), matches.group('local3'), matches.group('local4'))
    raise ValueError("Invalid phone number? '{}'".format(s))

'''
Exercise 3 (3 points). Implement an enhanced phone number parser that can handle any of these patterns.

(404) 555-1212
(404) 5551212
404-555-1212
404-5551212
404555-1212
4045551212

As before, it should not be sensitive to leading or trailing spaces. Also, for the patterns in which the area code is enclosed in parentheses, it should not be sensitive to the number of spaces separating the area code from the remainder of the number.
'''

def parse_phone2(s):
    pattern = '''
        ^\s*               # Leading spaces
        (?P<areacode>
           \d{3}-?         # "xxx" or "xxx-"
           | \(\d{3}\)\s*  # OR "(xxx) "
        )
        (?P<prefix>\d{3})  # xxx
        -?                 
        (?P<suffix>\d{4})  # xxxx
        \s*$               # Trailing spaces
    '''
    matcher = re.compile(pattern, re.VERBOSE)
    matches = matcher.match(s)
    if matches is None:
        raise ValueError("'{}' is not in the right format.".format (s))
    areacode = re.search('\d{3}', matches.group ('areacode')).group()
    prefix = matches.group ('prefix')
    suffix = matches.group ('suffix')
    return (areacode, prefix, suffix)