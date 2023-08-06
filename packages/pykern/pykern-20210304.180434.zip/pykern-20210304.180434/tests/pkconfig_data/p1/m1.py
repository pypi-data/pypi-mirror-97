# -*- coding: utf-8 -*-
u"""test `pykern.pkconfig`

:copyright: Copyright (c) 2015 RadiaSoft LLC.  All Rights Reserved.
:license: http://www.apache.org/licenses/LICENSE-2.0.html
"""
from __future__ import absolute_import, division, print_function
from pykern import pkconfig
from pykern.pkdebug import pkdc, pkdp
import os

def _custom_p6(v):
    import dateutil.parser
    return dateutil.parser.parse(v)

@pkconfig.parse_none
def _some_key(v):
    if v is None:
        return 999
    return int(v)

cfg = pkconfig.init(
    dict1=({
        'd1': 'default1',
        'd2': 'default2',
    }, dict, 'first param is dict'),
    list2=(['second1'], list, 'second param is list'),
    p3=(1313, int, 'third param is int'),
    p4=(None, int, 'fourth param is 10x p3'),
    p6=(None, _custom_p6, 'sixth param is a custom parser'),
    list7=(['default7'], list, 'seventh param is a list '),
    req8=pkconfig.Required(int, 'an eighth required parameter'),
    sub_params9=dict(
        sub9_1=(None, int, 'sub param is first of ninth group'),
        sub9_2=dict(
            sub9_2_1=(44, int, 'sub 9.2.1')
        ),
    ),
    req10=pkconfig.RequiredUnlessDev(('dev-host',), tuple, 'a dev default-only param'),
    dynamic_default10=(None, _some_key, 'sub dynamic default by parsing None'),
    bool1=(False, bool, 'a False boolean'),
    bool2=(True, bool, 'a True boolean'),
    bool3=(True, bool, 'a True boolean will be overriden'),
    bool4=(False, bool, 'a False boolean will be overriden'),
    tuple1=((), tuple, 'an empty tuple'),
    tuple2=((1,), tuple, 'a single value tuple'),
    tuple3=((2,), tuple, '(2,) will be overrriden'),
    tuple4=((3,), tuple, '(3,) will be overriden'),
    set1=(set(), set, 'an empty set'),
    # sets should have only one value of a type
    set2=((1, 1), set, 'a single value set'),
    set3=(set([2,]), frozenset, '(2,) will be overrriden'),
    set4=((3,), set, '(3,) will be overriden'),
)
if cfg.p4 is None:
    cfg.p4 = cfg.p3 * 10
