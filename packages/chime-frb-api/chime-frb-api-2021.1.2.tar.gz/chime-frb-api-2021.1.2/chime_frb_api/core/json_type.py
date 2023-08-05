#!/usr/bin/env python
from typing import List, Mapping, Union

# Possible JSON Values
_v = Union[str, int, float, bool, None]
_4 = Mapping[str, Union[_v, Mapping[str, _v], List[_v]]]
_3 = Mapping[str, Union[_v, Mapping[str, Union[_v, _4]], List[_4]]]
_2 = Mapping[str, Union[_v, Mapping[str, Union[_v, _3]], List[_3]]]
_1 = Mapping[str, Union[_v, Mapping[str, Union[_v, _2]], List[_2]]]

JSON = Mapping[str, Union[_v, Mapping[str, Union[_v, _1]], List[_1]]]
