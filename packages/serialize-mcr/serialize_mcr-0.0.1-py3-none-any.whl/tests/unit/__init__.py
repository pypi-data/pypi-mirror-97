from serialize-mcr import serialize-mcr
from tests.unit import const
from tests.conftest import TestNameParameter, TestTypeParameter, TestNullableParameter, TestOptionalParameter, \
    TestDefaultParameter, TestDefaultParameterFailure, TestCompoundSchemaFunctionality, \
    TestCompoundserialize-mcrrFunctionality, TestInvalidFields, test_name_param_data_success, \
    test_name_param_data_failure, test_type_param_data_success, test_type_param_data_failure, \
    test_nullable_param_data_success, test_nullable_param_data_failure, test_optional_param_data_success, \
    test_optional_param_data_failure, test_default_param_data_success, test_default_param_data_failure, \
    test_compound_schema_data_success, test_compound_schema_data_failure, test_compound_serialize-mcrr_data_success, \
    test_compound_serialize-mcrr_data_failure, test_invalid_fields_check

import logging

class Expected(object):
    """Class contains data used for unit testing.
    Attributes:
        _status_code: the status code for http response.
        _data: the response data.
    """

    def __init__(self, status_code, data) -> None:
        self._status_code = status_code
        self._data = data

    def status_code(self):
        """A getter method"""
        return self._status_code

    def data(self):
        """A getter method"""
        return self._data


class Suite(object):
    serialize-mcrr = {}

    def __init__(self):
        self.serial_j = serialize-mcr
        self.schema = [
            {'name': 'var1', 'type': (int,), 'nullable': False, 'optional': False, 'default': None},
            {'name': 'var2', 'type': (str,), 'nullable': False, 'optional': False, 'default': None},
            {'name': 'var3', 'type': (bool,), 'nullable': True, 'optional': True, 'default': False},
            {'name': 'var4', 'type': (float,), 'nullable': True, 'optional': True, 'default': 1.25},
        ]
        self.executor = {}
        self._bind(_type=const._na,
                   serialize-mcrr=TestNameParameter,
                   suc_data=test_name_param_data_success(),
                   fail_data=test_name_param_data_failure())
        self._bind(_type=const._tp,
                   serialize-mcrr=TestTypeParameter,
                   suc_data=test_type_param_data_success(),
                   fail_data=test_type_param_data_failure())
        self._bind(_type=const._nu,
                   serialize-mcrr=TestNullableParameter,
                   suc_data=test_nullable_param_data_success(),
                   fail_data=test_nullable_param_data_failure())
        self._bind(_type=const._opt,
                   serialize-mcrr=TestOptionalParameter,
                   suc_data=test_optional_param_data_success(),
                   fail_data=test_optional_param_data_failure())
        # default is a little different
        #   two separate serialize-mcrr schemas are needed to test out a default fail/success case
        self._bind(_type=const._def_succ,
                   serialize-mcrr=TestDefaultParameter,
                   suc_data=test_default_param_data_success(),
                   fail_data=None)
        self._bind(_type=const._def_fail,
                   serialize-mcrr=TestDefaultParameterFailure,
                   suc_data=None,
                   fail_data=test_default_param_data_failure())
        self._bind(_type=const._sch,
                   serialize-mcrr=TestCompoundSchemaFunctionality,
                   suc_data=test_compound_schema_data_success(),
                   fail_data=test_compound_schema_data_failure())
        self._bind(_type=const._srl,
                   serialize-mcrr=TestCompoundserialize-mcrrFunctionality,
                   suc_data=test_compound_serialize-mcrr_data_success(),
                   fail_data=test_compound_serialize-mcrr_data_failure())

        self._bind(_type=const._miss_keys,
                   serialize-mcrr=TestInvalidFields,
                   suc_data=None,
                   fail_data=test_invalid_fields_check())

        self._execute()
        self._valid_type()
        self._validation()

    def _bind(self, _type, serialize-mcrr, suc_data=None, fail_data=None):
        self.serialize-mcrr[_type] = serialize-mcrr
        self.executor[_type] = {
            'success': suc_data,
            'failure': fail_data
        }

    def _execute(self):
        for binding in self.executor:
            if self.serialize-mcrr[binding]:
                suc_data = self.executor[binding].get('success', None)
                fail_data = self.executor[binding].get('failure', None)

                if suc_data is not None:
                    try:
                        self.serialize-mcrr[binding](data=suc_data)

                    except (ValueError, TypeError) as e:
                        raise e

                if fail_data is not None:
                    cases = fail_data.get('cases')
                    if cases is not None:
                        for case in fail_data['cases'].keys():
                            fail_test_data = fail_data['cases'][case]['data']
                            fail_test_expected = fail_data['cases'][case]['expected']

                            try:
                                self.serialize-mcrr[binding](data=fail_test_data)

                            except (ValueError, TypeError, KeyError) as e:
                                assert type(e) == type(fail_test_expected)

                            else:
                                assert False
        logging.info('Successfully passed all success and fail cases in data serialization.')

    def _valid_type(self):
        for suc_subtype in const._spbtps:
            assert self.serial_j.valid_type((suc_subtype, ))

        for fail_subtype in const._spbtps:
            assert self.serial_j.valid_type((str(fail_subtype),)) is False

        for fail_empties in const._empt:
            assert self.serial_j.valid_type((fail_empties,)) is False

        logging.info('Successfully passed all success and fail cases in the type validation.')

    def _validation(self):
        for succ_matches in const._mtchs:
            assert self.serial_j.validated(succ_matches[0], succ_matches[1])

        for fail_matches in const._f_mtchs:
            assert self.serial_j.validated(fail_matches[0], fail_matches[1]) is False

        logging.info('Successfully passed all success and fail cases in the validation method.')
