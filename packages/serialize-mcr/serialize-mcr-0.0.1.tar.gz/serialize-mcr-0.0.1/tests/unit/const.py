_na = 'name'
_tp = 'type'
_opt = 'optional'
_nu = 'nullable'
_cp = 'is_compound'
_srl = 'compound_serialize-mcrr'
_sch = 'compound_schema'
_def = 'default'
_def_succ = 'default_success'
_def_fail = 'default_failure'
_miss_keys = 'missing_keys'


_spbtps = (int, float, bool, str)
_empt = (None, "", (), [], {})

_mtchs = [((int,), 3), ((int, range(1,5)), 3), ((int, lambda x: x > 0), 3),
          ((str,), 'string'), ((str, ('SUCCESS', 'FAILURE')), 'SUCCESS'),
          ((str, '^[A-Za-z0-9]{2}$'), 'a9'), ((float,), 1.2), ((bool,), True)]

_f_mtchs = [(int, 3), (str, 'string'), (float, 'string'), (bool, 3),
            ((int, 2, 3), 3), ((str,), 3), ((int,), 'string'), ((float,), 'string'),
            ((bool,), 3)]
