""" Why use conftest.py?
    -> Sharing fixture functions
If during implementing your tests you realize that you want to use a fixture
function from multiple test files you can move it to a conftest.py file.
You don’t need to import the fixture you want to use in a test, it
automatically gets discovered by pytest.
The discovery of fixture functions starts at test classes, then test modules,
then conftest.py files and finally builtin and third party plugins.
You can also use the conftest.py file to implement local per-directory plugins.
    -> Sharing Test Data
If you want to make test data from files available to your tests, a good way
to do this is by loading these data in a fixture for use by your tests.
This makes use of the automatic caching mechanisms of pytest.
    -> Scope of Fixture
You can declare the scope of any fixture by providing the scope argument.
Default scope is "function".
    1. @pytest.fixture(scope = "function")
        fixture function to be invoked once per test function, meaning every
        test function (name prefixed with `test_`) gets 1 fixture of this kind.
    2. @pytest.fixture(scope = "class")
        fixture function to be invoked once per test class, meaning every test
        class gets 1 fixture of this kind.
    3. @pytest.fixture(scope = "module")
        fixture function to be invoked once per test module, meaning every
        test file (module) gets 1 fixture of this kind.
    4. @pytest.fixture(scope = "package")
        WARNING: this is a experimental feature, and maybe removed in future
        version.
        fixture function to be invoked once per test package, meaning every
        test package gets 1 fixture of this kind.
    5. @pytest.fixture(scope = "session")
        fixture function to be invoked once per test session, meaning all
        tests during the test session
        gets the same fixture of this kind.
Appropriate use of fixture scope will significantly improve the test efficiency.
Note: Higher-scoped fixtures are instantiated first. For example, `session`
scoped fixtures are instantiated first then `class` scoped fixtures gets
instantiated.
    -> Fixture finalization / teardown
    https://docs.pytest.org/en
    /latest/fixture.html#fixture-finalization-executing-teardown-code
"""
from serialize-mcr import serialize-mcr


# serialize-mcrrs
class TestNameParameter(serialize-mcr):
    schema = [
        # success cases
        {'name': 'var1', 'type': (str,)},
        {'name': 'var2', 'type': (str,)}
    ]

class TestTypeParameter(serialize-mcr):
    test_regex = "^[A-Za-z]{1}[0-9]{1}$"
    schema = [
        {'name': 'var1', 'type': (int,), 'optional': True},
        {'name': 'var2', 'type': (int, range(1, 10, 3)), 'optional': True},
        {'name': 'var3', 'type': (float,), 'optional': True},
        {'name': 'var4', 'type': (bool,), 'optional': True},
        {'name': 'var5', 'type': (str,), 'optional': True},
        {'name': 'var6', 'type': (str, 'url'), 'optional': True},
        {'name': 'var7', 'type': (str, 'uuid'), 'optional': True},
        {'name': 'var8', 'type': (str, 'email'), 'optional': True},
        {'name': 'var9', 'type': (str, 'ipv4'), 'optional': True},
        {'name': 'var10', 'type': (str, 'ipv6'), 'optional': True},
        {'name': 'var11', 'type': (str, test_regex), 'optional': True},
        {'name': 'var12', 'type': (str, ('SUCCESS', 'FAILURE')), 'optional': True},
        {'name': 'var13', 'type': (int, lambda x: x > 4), 'optional': True}
    ]


class TestNullableParameter(serialize-mcr):
    schema = [
        {'name': 'var1', 'type': (str,), 'nullable': False},
        {'name': 'var2', 'type': (str,), 'nullable': True}
    ]


class TestOptionalParameter(serialize-mcr):
    schema = [
        {'name': 'var1', 'type': (str,), 'optional': True},
        {'name': 'var2', 'type': (str,), 'optional': False}
    ]


class TestDefaultParameter(serialize-mcr):
    test_regex = '^[A-Za-z0-9]{3}$'
    schema = [
        {'name': 'var1', 'type': (str,), 'optional': True, 'default': 'string'},
        {'name': 'var2', 'type': (str, test_regex), 'optional': True, 'default': 'abc'},
        {'name': 'var3', 'type': (str, ('SUCCESS', 'FAILURE')), 'optional': True, 'default': 'FAILURE'},
        {'name': 'var4', 'type': (int,), 'optional': True, 'default': 1},
        {'name': 'var5', 'type': (float,), 'optional': True, 'default': 1.2},
        {'name': 'var6', 'type': (bool,), 'optional': True, 'default': True},
        {'name': 'var7', 'type': (int, range(1, 4)), 'optional': True, 'default': 3},
        {'name': 'var8', 'type': (int, lambda x: x > 0), 'optional': True, 'default': 2}
    ]


class TestDefaultParameterFailure(serialize-mcr):
    test_regex = '^[A-Za-z0-9]{3}$'
    schema = [
        {'name': 'var1', 'type': (str,), 'optional': True, 'default': 1},
        {'name': 'var2', 'type': (str, test_regex), 'optional': True, 'default': 3},
        {'name': 'var3', 'type': (str, ('SUCCESS', 'FAILURE')), 'optional': True, 'default': 'PENDING'},
        {'name': 'var4', 'type': (int,), 'optional': True, 'default': True},
        {'name': 'var5', 'type': (float,), 'optional': True, 'default': 'string'},
        {'name': 'var6', 'type': (bool,), 'optional': True, 'default': 'string'},
        {'name': 'var7', 'type': (int, range(1, 4)), 'optional': True, 'default': 6},
        {'name': 'var8', 'type': (int, lambda x: x > 0), 'optional': True, 'default': -1}
    ]


class TestCompoundSchemaFunctionality(serialize-mcr):
    schema = [
        {'name': 'var1', 'is_compound': True,
         'compound_schema': [
             {'name': 'num1', 'optional': True},
             {'name': 'num2', 'optional': False}
         ]},
        {'name': 'var2', 'is_compound': True,
         'compound_schema': [
             {'name': 'num1', 'optional': True},
             {'name': 'num2', 'nullable': False}
         ]}
    ]


class Compoundserialize-mcrrHelper(serialize-mcr):
    schema = [
        {'name': 'num1', 'type': (int,)}
    ]


class TestCompoundserialize-mcrrFunctionality(serialize-mcr):
    schema = [
        {'name': 'var1', 'is_compound': True, 'compound_serialize-mcrr': Compoundserialize-mcrrHelper}
    ]

class TestInvalidFields(serialize-mcr):
    schema = [
        # success cases
        {'name': 'var1', 'type': (str,)},
        {'name': 'var2', 'type': (str,)},
    ]

# test data
# success cases
def test_name_param_data_success():
    return {
        'var1': 'string',
        'var2': 'string'
    }


def test_type_param_data_success():
    return {
        'var1': 1,
        'var2': 4,
        'var3': 1.23,
        'var4': True,
        'var5': 'string',
        'var6': 'https://www.someurl.com',
        'var7': '06dc0746-d0b6-4fcf-8087-df3245d1991f',
        'var8': 'someemail@email.com',
        'var9': '255.255.255.0',
        'var10': '2001:0db8:85a3:0000:0000:8a2e:0370:7334',
        'var11': 'A9',
        'var12': 'SUCCESS',
        'var13': 6
    }


def test_nullable_param_data_success():
    return {
        'var1': 'string',
        'var2': None
    }


def test_optional_param_data_success():
    return {
        'var1': None,
        'var2': 'string'
    }


def test_default_param_data_success():
    return {}


def test_compound_schema_data_success():
    return {
        'var1': {
            'num1': 1,
            'num2': 2
        },
        'var2': {
            'num1': 3,
            'num2': 4
        }
    }


def test_compound_serialize-mcrr_data_success():
    return {
        'var1': {
            'num1': 1
        }
    }


# fail cases
def test_name_param_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'variable1': 'string',
                    'var2': 'string'
                },
                'expected': ValueError(f"Property 'var1' not found in None.")
            }, 2: {
                'data': {
                    'var1': 'string',
                    'variable2': 'string'
                },
                'expected': KeyError(f"The following fields were invalid or misspelled: '[variable2]'.")
            }, 3: {
                'data': {},
                'expected': ValueError(f"Property 'var1' not found in None.")
            }, 4: {
                'data': {
                    True: 'string',
                    False: 'string'
                },
                'expected': ValueError(f"Property 'var1' not found in None.")
            }, 5: {
                'data': {
                    1: 'string',
                    2: 'string'
                },
                'expected': ValueError(f"Property 'var1' not found in None.")
            }, 6: {
                'data': {
                    (1, 2): 'string',
                    (3, 4): 'string'
                },
                'expected': ValueError(f"Property 'var1' not found in None.")
            }
        }
    }


def test_type_param_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var1': 'string'
                },
                'expected': ValueError(f"Property: 'var1' with Value: '1' does not conform with Type: {int}.")
            }, 2: {
                'data': {
                    'var2': 3
                },
                'expected': ValueError(f"Property: 'var2' with Value: '3' does not conform with Type: ({int}, "
                                       f"range(1, 10, 3)).")
            }, 3: {
                'data': {
                    'var3': 'string'
                },
                'expected': ValueError(f"Property: 'var3' with Value: 'string' does not conform with Type: {float}.")
            }, 4: {
                'data': {
                    'var4': 1
                },
                'expected': ValueError(f"Property: 'var4' with Value: '1' does not conform with Type: ({bool},).")
            }, 5: {
                'data': {
                    'var5': 1
                },
                'expected': ValueError(f"Property: 'var5' with Value: '1' does not conform with Type: ({str},).")
            }, 6: {
                'data': {
                    'var6': 'someemail@email.com'
                },
                'expected': ValueError(f"Property: 'var6' with Value: 'someemail@email.com' does not conform with "
                                       f"Type: ({str}, 'url').")
            }, 7: {
                'data': {
                    'var7': '1234567890'
                },
                'expected': ValueError(f"Property: 'var7' with Value: '1234567890' does not conform with "
                                       f"Type: ({str}, 'uuid').")
            }, 8: {
                'data': {
                    'var8': 'https://www.someurl.com'
                },
                'expected': ValueError(f"Property: 'var8' with Value: 'https://www.someurl.com' does not conform "
                                       f"with Type: ({str}, 'email').")
            }, 9: {
                'data': {
                    'var9': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
                },
                'expected': ValueError(f"Property: 'var9' with Value: '2001:0db8:85a3:0000:0000:8a2e:0370:7334' does "
                                       f"not conform with Type: ({str}, 'ipv4').")
            }, 10: {
                'data': {
                    'var10': '255.255.255.0'
                },
                'expected': ValueError(f"Property: 'var10' with Value: '255.255.255.0' does not conform with "
                                       f"Type: ({str}, 'ipv6').")
            }, 11: {
                'data': {
                    'var11': 'A&'
                },
                'expected': ValueError(f"Property: 'var11' with Value: 'A&' does not conform with "
                                       f"Type: ({str}, '^[A-Za-z]{{1}}[0-9]{{1}}$').")
            }, 12: {
                'data': {
                    'var12': 'PENDING'
                },
                'expected': ValueError(f"Property: 'var12' with Value: 'PENDING' does not conform with "
                                       f"Type: ({str}, ('SUCCESS', 'FAILURE')).")
            }, 13: {
                'data': {
                    'var13': 2
                },
                'expected': ValueError(f"Property: 'var13' with Value: '2' does not conform with "
                                       f"Type: ({int}, <function TestTypeParameter.<lambda> at 0x10e6cb7b8>).")
            }
        }
    }


def test_nullable_param_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var1': None,
                    'var2': 'string'
                },
                'expected': ValueError(f"Property 'var1' is not nullable.")
            }
        }
    }


def test_optional_param_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var1': 'string'
                },
                'expected': ValueError(f"Property 'var2' is not nullable.")
            }
        }
    }


def test_default_param_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var5': 1.2,
                    'var6': True,
                    'var7': 3,
                    'var8': 2,
                },
                'expected': ValueError(f"Property: 'var1' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 2: {
                'data': {
                    'var1': 'string',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var5': 1.2,
                    'var6': True,
                    'var7': 3,
                    'var8': 2,
                },
                'expected': ValueError(f"Property: 'var2' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 3: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var4': 1,
                    'var5': 1.2,
                    'var6': True,
                    'var7': 3,
                    'var8': 2
                },
                'expected': ValueError(f"Property: 'var3' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 4: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var5': 1.2,
                    'var6': True,
                    'var7': 3,
                    'var8': 2
                },
                'expected': ValueError(f"Property: 'var4' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 5: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var6': True,
                    'var7': 3,
                    'var8': 2
                },
                'expected': ValueError(f"Property: 'var5' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 6: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var5': 1.2,
                    'var7': 3,
                    'var8': 2
                },
                'expected': ValueError(f"Property: 'var6' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 7: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var5': 1.2,
                    'var6': True,
                    'var8': 2
                },
                'expected': ValueError(f"Property: 'var7' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }, 8: {
                'data': {
                    'var1': 'string',
                    'var2': 'abc',
                    'var3': 'FAILURE',
                    'var4': 1,
                    'var5': 1.2,
                    'var6': True,
                    'var7': 3
                },
                'expected': ValueError(f"Property: 'var8' does not have a defaulted value: 1 that is of "
                                       f"type: ({str},).")
            }
        }
    }


def test_compound_schema_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var1': {
                        'num3': 1,
                        'num4': 2
                    },
                    'var2': {
                        'num1': 3,
                        'num2': 4
                    }
                },
                'expected': KeyError(f"The following fields were invalid or misspelled: '[num3, num4]'.")
            }, 2: {
                'data': {
                    'var2': {
                        'num1': 1,
                        'num2': 2
                    }
                },
                'expected': ValueError()
            }, 3: {
                'data': {
                    'var1': None,
                    'var2': {
                        'num1': 1,
                        'num2': 2
                    }
                },
                'expected': ValueError()
            }, 4: {
                'data': {},
                'expected': ValueError()
            }
        }
    }


def test_compound_serialize-mcrr_data_failure():
    return {
        'cases': {
            1: {
                'data': {
                    'var1': {
                        'num1': 'string'
                    }
                },
                'expected': ValueError()
            }, 2: {
                'data': {
                    'var1': {
                        'num2': 2
                    }
                },
                'expected': ValueError()
            }, 3: {
                'data': {
                    'var3': {
                        'num1': 2
                    }
                },
                'expected': ValueError()
            }, 4: {
                'data': {
                    'var1': {
                        'num1': None
                    }
                },
                'expected': ValueError()
            }
        }
    }


def test_invalid_fields_check():
    '''
    technically this is a success case,
    but marked as failure because we expect an exception to be raised
    '''
    return {
        'cases': {
            1: {
                'data': {
                    'var1': 'string',
                    'var2': 'string',
                    'invalid_field': 'string',
                    'ver2': 0,
                    'var5': 'string'
                },
                'expected': KeyError(f"The following fields were invalid or misspelled: 'invalid_field', 'ver2', 'var5'.")
            }
        }
    }
