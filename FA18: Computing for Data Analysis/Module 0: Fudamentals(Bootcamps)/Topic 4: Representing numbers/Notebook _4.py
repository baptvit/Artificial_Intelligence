'''
Exercise 0 (3 points).
Write a function, eval_strint(s, base).
It takes a string of digits s in the base given by base. It returns its value as an integer.
'''

def eval_strint(s, base=2):
    assert type(s) is str
    assert 2 <= base <= 36
    return int(s, base)
'''
Exercise 1 (4 points). 
Suppose a string of digits s in base base contains up to one fractional point. Complete the function, eval_strfrac(s, base), so that it returns its corresponding floating-point value. 
Your function should always return a value of type float, even if the input happens to correspond to an exact integer.
'''


def is_valid_strfrac(s, base=2):
    return all([is_valid_strdigit(c, base) for c in s if c != '.']) \
           and (len([c for c in s if c == '.']) <= 1)


def eval_strfrac(s, base=2):
    assert is_valid_strfrac(s, base), "'{}' contains invalid digits for a base-{} number.".format(s, base)

    s_parts = s.split('.')

    assert len(s_parts) <= 2

    value_int = eval_strint(s_parts[0], base)
    if len(s_parts) == 2:
        r = len(s_parts[1])
        value_frac = eval_strint(s_parts[1], base) * (float(base) ** (-r))
    else:
        value_frac = 0
    return float(value_int) + value_frac

'''
Exercise 2 (4 points). Write a function, fp_bin(v), that determines the IEEE-754 tuple representation of any double-precision floating-point value, v. That is, given the variable v such that type(v) is float, it should return a tuple with three components, (s_sign, s_bin, v_exp) such that

s_sign is a string representing the sign bit, encoded as either a '+' or '-' character;
s_signif is the significand, which should be a string of 54 bits having the form, x.xxx...x, where there are (at most) 53 x bits (0 or 1 values);
v_exp is the value of the exponent and should be an integer.
'''


def fp_bin(v):
    assert type(v) is float
    sign = '-' if v < 0 else '+'
    v = abs(v).hex()[2:]
    significand, exponent = v.split('p')
    exponent = int(exponent)
    signif_lead, signif_rem = significand.split('.')


    signif_rem = ''.join([hex2bin(x, 4) for x in signif_rem])
    signif = signif_lead + '.' + signif_rem
    signif += '0' * (54 - len(signif))
    return sign, signif, exponent


def hex2bin(num, width=4):
    return bin(int(num, base=16))[2:].zfill(width)

'''
Exercise 3 (2 points). Suppose you are given a floating-point value in a base given by base and in the form of the tuple, (sign, significand, exponent), where

sign is either the character '+' if the value is positive and '-' otherwise;
significand is a string representation in base-base;
exponent is an integer representing the exponent value.
'''

def eval_fp(sign, significand, exponent, base=2):
    assert sign in ['+', '-'], "Sign bit must be '+' or '-', not '{}'.".format(sign)
    assert is_valid_strfrac(significand, base), "Invalid significand for base-{}: '{}'".format(base, significand)
    assert type(exponent) is int

    v_sign = 1.0 if sign == '+' else -1.0
    v_significand = eval_strfrac(significand, base)
    return v_sign * v_significand * (base ** exponent)



'''
Exercise 4 (2 points). Suppose you are given two binary floating-point values, u and v, in the tuple form given above. That is, u == (u_sign, u_signif, u_exp) and v == (v_sign, v_signif, v_exp), where the base for both u and v is two (2). 
Complete the function add_fp_bin(u, v, signif_bits), so that it returns the sum of these two values with the resulting significand truncated to signif_bits digits
'''


def add_fp_bin(u, v, signif_bits):
    u_sign, u_signif, u_exp = u
    v_sign, v_signif, v_exp = v

    print('sign: ', u_sign, v_sign)
    print('signif ', u_signif, v_signif)
    print('exp ', u_exp, v_exp)

    assert u_signif[:2] == '1.' and len(u_signif) == (signif_bits + 1)
    assert v_signif[:2] == '1.' and len(v_signif) == (signif_bits + 1)

    u_value = eval_fp(u_sign, u_signif, u_exp, base=2)
    v_value = eval_fp(v_sign, v_signif, v_exp, base=2)
    w_value = u_value + v_value
    w_sign, w_signif, w_exp = fp_bin(w_value)
    w_signif = w_signif[:(signif_bits + 1)]
    return (w_sign, w_signif, w_exp)

