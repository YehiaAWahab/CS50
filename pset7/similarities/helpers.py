from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""
    a_list = set(a.split("\n"))
    b_list = set(b.split("\n"))

    return a_list & b_list


def sentences(a, b):
    """Return sentences in both a and b"""
    result = []
    a_list = set(sent_tokenize(a))
    b_list = set(sent_tokenize(b))

    return a_list & b_list


def get_substring_list(s, n):
    result = []
    for i in range(len(s) - n + 1):
        a = s[i:n]
        result.append(a)
        n += 1
    return result


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    result = []
    a_list = set(get_substring_list(a, n))
    b_list = set(get_substring_list(b, n))

    return a_list & b_list