#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype object utility unit tests.**

This submodule unit tests the public API of the private
:mod:`beartype._util.utilobject` submodule.
'''

# ....................{ IMPORTS                           }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# ....................{ TESTS                             }....................
def test_is_object_hashable() -> None:
    '''
    Test the :func:`beartype._util.utilobject.is_object_hashable` function.
    '''

    # Defer heavyweight imports.
    from beartype._util.utilobject import is_object_hashable
    from beartype_test.a00_unit.data.hint.data_hint import (
        NOT_HINTS_HASHABLE, NOT_HINTS_UNHASHABLE,)

    # Assert this tester accepts unhashable objects.
    for object_hashable in NOT_HINTS_HASHABLE:
        assert is_object_hashable(object_hashable) is True

    # Assert this tester rejects unhashable objects.
    for object_unhashable in NOT_HINTS_UNHASHABLE:
        assert is_object_hashable(object_unhashable) is False
