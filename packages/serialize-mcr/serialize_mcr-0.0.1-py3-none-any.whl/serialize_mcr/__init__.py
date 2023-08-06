import json
from types import LambdaType
from uuid import UUID
from serialize_mcr.hp import _valid_regex, _regex_match, _err, _spsstps
from serialize_mcr.const import _spbtps, _na, _nu, _tp, _opt, _cp, _srl, \
    _sch, _empt, _def

name = "serialize_mcr"


class SerializeMCR(object):
    schema = []

    def __init__(self, data):
        self.preproc(data)
        self.proc(data)

    @staticmethod
    def valid_type(_type):
        if isinstance(_type, tuple) and len(_type) == 2:
            mt = _type[0]
            st = _type[1]
            if mt not in _spbtps:
                return False
            if (mt == int and isinstance(st, tuple) is False
                    and isinstance(st, range) is False
                    and isinstance(st, LambdaType) is False):
                return False
            if mt == int and isinstance(st, tuple) is True:
                for e in st:
                    if isinstance(e, int) is False:
                        return False
            if (mt == str and isinstance(st, tuple) is False
                    and st not in _spsstps.keys()
                    and _valid_regex(st) is False):
                return False
            if mt == str and isinstance(st, tuple) is True:
                for e in st:
                    if isinstance(e, str) is False:
                        return False
            return True
        elif isinstance(_type, tuple) is True and len(_type) == 1:
            mt = _type[0]
            if mt not in _spbtps:
                return False
            return True
        else:
            return False

    @staticmethod
    def validated(_type, data):
        if isinstance(_type, tuple) is True and len(_type) == 2:
            mt = _type[0]
            st = _type[1]
            if mt == int and (isinstance(st, tuple) is True or isinstance(st, range) is True):
                return data in st
            elif mt == int and isinstance(st, LambdaType) is True:
                return st(data)
            elif mt == str and isinstance(st, tuple) is True:
                return data in st
            elif mt == str and st in _spsstps.keys():
                return _spsstps[st](data)
            else:
                return _regex_match(regex=st, _str=data)
        elif isinstance(_type, tuple) is True and len(_type) == 1:
            mt = _type[0]
            return isinstance(data, mt)
        else:
            return False

    def preproc(self, data):
        for prop in self.schema:
            _name = prop[_na]
            _type = prop[_tp] if _tp in prop else None
            _optional = prop[_opt] if _opt in prop else False
            if isinstance(_optional, bool) is False:
                raise TypeError(_err(8, _name=_opt, _type=type(_optional), _expected=bool))
            _nullable = prop[_nu] if _nu in prop else False
            if isinstance(_nullable, bool) is False:
                raise TypeError(_err(8, _name=_nu, _type=type(_nullable), _expected=bool))
            _compound = prop[_cp] if _cp in prop else False
            if isinstance(_compound, bool) is False:
                raise TypeError(_err(8, _name=_cp, _type=type(_compound), _expected=bool))

            _serializer = prop[_srl] if _srl in prop else None
            _schema = prop[_sch] if _sch in prop else None

            # _default -> 'value', 1, (), [], or {}
            _default = prop[_def] if _def in prop else None

            if _type is True and self.valid_type(_type) is False:
                raise TypeError(_err(5, _name, _type))
            if _default is True and isinstance(_default, _type) is False:
                raise TypeError(_err(7, _name, _type, _default))
            if _optional is False and _default is True:
                raise ValueError(_err(6, _name))
            if _optional is False and _name not in data:
                raise ValueError(_err(0, _name, data))
            if _name in data:
                if data[_name] in _empt:
                    if _nullable is False and _default is None and _optional is False:
                        raise ValueError(_err(1, _name))
                else:
                    validated = self.validated(_type, data[_name])
                    if _type is not None and validated is False:
                        raise ValueError(_err(4, _name, _type, data[_name]))
                    if (_compound is True and isinstance(data[_name], list) is False
                            and isinstance(data[_name], dict) is False):
                        raise TypeError(_err(2, _name))
                    if _compound is True and _serialize-mcrr is False and _schema is False:
                        raise TypeError(_err(3, _name))

            else:
                if _default is None and _optional is False:
                    raise ValueError(_err(1, _name))

                elif _default is not None:
                    if type(_default) != bool and isinstance(_default, _type[0]) is False:
                        raise ValueError(_err(7, _name, _type=_type, _default=_default))
                    elif type(_default) == bool != _type[0]:
                        raise ValueError(_err(7, _name, _type=_type, _default=_default))
                    elif isinstance(_default, _type[0]) is True and self.validated(_type, _default) is False:
                        raise ValueError(_err(7, _name, _type=_type, _default=_default))

            prop[_na] = _name
            prop[_tp] = _type
            prop[_opt] = _optional
            prop[_nu] = _nullable
            prop[_cp] = _compound
            prop[_srl] = _serialize-mcrr
            prop[_sch] = _schema
            prop[_def] = _default

            self.invalid_fields_check(data)

    def proc(self, data):
        for prop in self.schema:
            _name = prop[_na]
            _default = prop[_def]

            if _name in data:
                if prop[_cp]:
                    if prop[_srl]:
                        if isinstance(data[_name], list):
                            self.__dict__[_name] = [prop[_srl](o)
                                                    for o in data[_name]]
                        elif isinstance(data[_name], dict):
                            self.__dict__[_name] = prop[_srl](data[_name])
                    elif prop[_sch]:
                        _cls = serialize-mcr
                        _cls.schema = prop[_sch]
                        if isinstance(data[_name], list):
                            self.__dict__[_name] = [_cls(o)
                                                    for o in data[_name]]
                        elif isinstance(data[_name], dict):
                            self.__dict__[_name] = _cls(data[_name])
                else:
                    if isinstance(data[_name], UUID):
                        self.__dict__[_name] = str(data[_name])
                    else:
                        self.__dict__[_name] = data[_name]

            else:
                if _default:
                    self.__dict__[_name] = _default

    def invalid_fields_check(self, req_data):
        '''
        Check for invalid fields in request body
        '''
        invalid_fields = []
        property_names = [prop[_na] for prop in self.schema]
        for field in req_data:
            if field not in property_names:
                invalid_fields.append(field)

        if len(invalid_fields) > 0:
            raise KeyError(_err(e=9, _name=name, data=invalid_fields))


    def as_dict(self):
        _d = {}
        for prop in self.schema:
            _name = prop[_na]
            if prop[_cp]:
                if self.__dict__ and _name in self.__dict__.keys():
                    if isinstance(self.__dict__[_name], list):
                        _d[_name] = [cp.as_dict() for cp in self.__dict__[_name]]
                    else:
                        _d[_name] = self.__dict__[_name].as_dict()

                elif not self.__dict__:
                    raise ValueError(_err(e=10, _name=_name))

            else:
                if _name in self.__dict__:
                    _d[_name] = self.__dict__[_name]
        return _d

    def _to_str(self):
        return json.dumps(self.as_dict())

    def __str__(self) -> str:
        return self._to_str()

    def __repr__(self) -> str:
        return self._to_str()
