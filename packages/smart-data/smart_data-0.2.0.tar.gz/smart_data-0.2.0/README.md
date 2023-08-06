# SMART DATA

SMART DATA is a package to make your live easier. For example you want to test many JSON (or any other) results from some API in Python.
There are plenty of great Python packages to find a differences between two complex structres but sometimes you need omit some their parts.
This package help you to write this kind of code easier.

## Requirements

No package dependecy.

## Installation

```
pip install smart_data
```

## Functions

### list_diff = include(got, expected) 
* got       - structure to check
* expected  - structure that is required in 'got' structure. Any difference will be in returned list.
* list_diff - list with differences, e.g. 
  `['/attributes/temperature/<20.1 vs 22.2>']`

Try to check if 'expected' structure includes 'got' structure. Any additional keys from 'got' will be igroned.
This situation can be expected if you don't want to check some parts of complex structure (e.g. in tests).

The structures should contain dictionaries, lists, objects, simple types or any comparable structures (`__str__` and `__eq__` implementation).
Additionally 'expected' can be or can contains compiled regular expression (re package) to check e.g. if you don't want mocking datetime objects.

## Example of usage

So let's try test some endpoint:
```
import re
re_datetime = re.compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$")

def test_add_new(self, client):
    with client:
        res = client.post(
            '/air_state',
            json = {
                'data': {
                    'type': 'air_state',
                    'attributes': {
                        'temperature': 20.1,
                        'humidity': 51.2,
                        'location': 'kitchen',
                        'device': 'dev1_esp',
                    },
                },
            },
            content_type = 'application/vnd.api+json',
        )
        assert 201 == res.status_code
        res_json = res.get_json()
        
        assert res_json['data']['type'] == 'air_state'
        assert res_json['data']['id'] == '1'
        assert res_json['data']['attributes']['temperature'] == '20.1'
        assert res_json['data']['attributes']['humidity'] == '51.2'
        assert res_json['data']['attributes']['location'] == 'kitchen'
        assert res_json['data']['attributes']['device'] == 'dev1_esp'
        assert re_datetime.search(res_json['data']['attributes']['created'])

```
You need write buch of asserts for many items in result structure. Many lines of code. If bigger structure then more code.

Now you can write it in another way using smart_data package:
```
from smart_data import include
from re import compile

def test_add_new(self, client):

    payload = {
        'type': 'air_state',
        'attributes': {
            'temperature': 20.1,
            'humidity': 51.2,
            'location': 'kitchen',
            'device': 'dev1_esp',
        },
    }

    with client:
        res = client.post(
            '/air_state',
            json = { 'data': payload },
            content_type = 'application/vnd.api+json',
        )
        assert 201 == res.status_code

        payload['attributes']['id'] = 1
        payload['attributes']['created'] = compile(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d$")
        res_json = res.get_json()
        assert include(got=res_json['data'], expected=payload) == []
```
This is simple example with really small amount of data to test. For more complex structure the benefit is higher. 

Next benefit is readable output from broken assert during tests. For example:
```
    def test_foo():
        expected = {
            'foo': 1.1,
            'bar': [42, {'baz': 22}],
            'zoo': None,
            'zar': [[1, 3], [5, 8]],
        }
        got = {
            'foo': 1.1,
            'bar': [42, {'baz': 2}],
            'zoo': None,
            'zar': [[1, 3], [5, 8]],
        }
>       assert include(got, expected) == []
E       AssertionError: assert ['/bar/1/baz/<2 vs 22>'] == []
E         Left contains one more item: '/bar/1/baz/<2 vs 22>'
E         Full diff:
E         - []
E         + ['/bar/1/baz/<2 vs 22>']

tests/test_include.py:38: AssertionError
```


