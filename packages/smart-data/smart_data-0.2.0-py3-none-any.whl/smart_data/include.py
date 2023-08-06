from re import compile as re_compile

# Taken from re.py (Python 3.6).
_pattern_type = type(re_compile("", 0))


# TODO: add optional parameter: find_in_list (True, False; default False).
# TODO: think about yield version instead of recursive version of 'include'.
def include(got, expected, path=''):

    def _eq_types(got_struct, expected_struct, struct_type):
        if isinstance(got_struct, struct_type) and isinstance(expected_struct, struct_type):
            return True
        return False

    diff_paths = []

    # Complex types:
    if _eq_types(got, expected, dict):
        for key in expected:

            if key in got:
                res = include(got[key], expected[key], f"{path}/{key}")
                diff_paths.extend(res)
            else:
                diff_paths.append(f'{path}/<lack of {key}>')

    elif _eq_types(got, expected, list):
        # Comparing lists lengths.
        len_got = len(got)
        len_expected = len(expected)
        if len_got != len_expected:
            diff_paths.append(f'{path}/<list length diff>')

        # Comparing lists elements.
        # Always get smaller length.
        range_loop = len_expected if len_expected <= len_got else len_got 
        for i in range(range_loop):
            res = include(got[i], expected[i], f"{path}/{i}")
            diff_paths.extend(res)

        # or find each got element in expected list (no matter len comparsion and comparsion items one by one).
        # If some element doesn't exist in expected list then add it to diff_paths.

    # Reqular expression check expectations.
    elif isinstance(expected, _pattern_type):
        got_str = str(got)
        if not expected.search(got_str):
            diff_paths.append(f"{path}/<{got} not matched to regex {expected}>")

    # Simple types:
    elif type(got) == type(expected):
        if got != expected:
            diff_paths.append(f'{path}/<{got} vs {expected}>')

    else:
        diff_paths.append(f'{path}/<type diff>')

    return diff_paths
