from smart_data import include
from re import compile as re_compile, search as re_search

expected = {
    'foo': 1.1,
    'bar': [42, {'baz': 2}],
    'zoo': None,
    'zar': [[1, 3], [5, 8]],
}


def test_is_equal():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
        'zaz': 2.2,  # additional key will be ignored
    }
    assert include(got, expected) == []


def test_different_types():
    got = {
        'foo': 1.1,
        'bar': {},
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<type diff>']


def test_lack_of_zoo_key():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}],
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/<lack of zoo>']


def test_longer_list():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 2}, 4],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<list length diff>']


def test_shorter_list():
    got = {
        'foo': 1.1,
        'bar': [42],
        'zoo': None,
        'zar': [[1, 3], [5, 8]],
    }
    assert include(got, expected) == ['/bar/<list length diff>']


def test_different_values():
    got = {
        'foo': 1.1,
        'bar': [42, {'baz': 43}],
        'zoo': None,
        'zar': [[10, 3], [50, 8]],
    }
    assert include(got, expected) == ['/bar/1/baz/<43 vs 2>', '/zar/0/0/<10 vs 1>', '/zar/1/0/<50 vs 5>']


# Try to test structures with objects:
class Foo:
    def __init__(self, foo):
        self.foo = foo

    def __str__(self):
        return str(self.foo)

    def __eq__(self, other):
        if self.foo == other.foo:
            return True
        else:
            return False


def test_equal_objects():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': []
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': []
    }
    assert include(got_with_obj, expected_with_obj) == []


def test_different_objects():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': []
    }

    got_with_obj = {
        'foo': Foo(2),
        'bar': []
    }
    assert include(got_with_obj, expected_with_obj) == ['/foo/<2 vs 1>']


def test_matching_regex():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': "2021-03-05 18:42:42",
    }
    assert include(got_with_obj, expected_with_obj) == []


def test_not_matching_regex():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': "20-03-05",
    }
    assert include(got_with_obj, expected_with_obj) == ["/created/<20-03-05 not matched to regex re.compile('^\\\\d{4}-\\\\d\\\\d-\\\\d\\\\d$')>"]


def test_not_matching_regex_diff_types():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': ["2021-03-05"],
    }
    assert include(got_with_obj, expected_with_obj) == ["/created/<['2021-03-05'] not matched to regex re.compile('^\\\\d{4}-\\\\d\\\\d-\\\\d\\\\d$')>"]


def test_not_matching_regex_with_class():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': Foo("20-03-05"),
    }
    assert include(got_with_obj, expected_with_obj) == ["/created/<20-03-05 not matched to regex re.compile('^\\\\d{4}-\\\\d\\\\d-\\\\d\\\\d$')>"]


def test_matching_regex_with_class():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': Foo("2021-03-05"),
    }
    assert include(got_with_obj, expected_with_obj) == []


# Class without __eq__ and __str__ methods.
class Bar:
    def __init__(self, bar):
        self.bar = bar


def test_not_matching_regex_with_class_without_str_and_eq():
    expected_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': re_compile(r"^\d{4}-\d\d-\d\d$"),
    }

    got_with_obj = {
        'foo': Foo(1),
        'bar': [],
        'created': Bar("2021-03-05"),
    }

    result = include(got_with_obj, expected_with_obj)
    assert len(result) == 1 and re_search(r"Bar object at", result[0])


# pytest -vv
# pytest --cov=smart_data tests/ 
