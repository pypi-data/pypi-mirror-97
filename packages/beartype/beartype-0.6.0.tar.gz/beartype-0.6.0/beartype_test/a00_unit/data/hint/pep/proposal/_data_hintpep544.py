#!/usr/bin/env python3
# --------------------( LICENSE                           )--------------------
# Copyright (c) 2014-2021 Beartype authors.
# See "LICENSE" for further details.

'''
**Beartype** `PEP 544`_**-compliant type hint test data.**

.. _PEP 544:
    https://www.python.org/dev/peps/pep-0544
'''

# ....................{ TODO                              }....................
#FIXME: Test user-defined multiple-inherited protocols (i.e., user-defined
#classes directly subclassing the "typing.Protocol" ABC and one or more other
#superclasses) once @beartype supports these protocols as well.

# ....................{ IMPORTS                           }....................
import pathlib
from abc import abstractmethod
from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_8
from beartype_test.a00_unit.data.hint.data_hintmeta import (
    PepHintMetadata,
    PepHintPithSatisfiedMetadata,
    PepHintPithUnsatisfiedMetadata,
)

# ....................{ CONSTANTS                         }....................
_DATA_HINTPEP544_FILENAME = __file__
'''
Absolute filename of this data submodule, to be subsequently opened for
cross-platform IO testing purposes by the :func:`add_data` function.
'''

# ....................{ ADDERS                            }....................
def add_data(data_module: 'ModuleType') -> None:
    '''
    Add `PEP 544`_**-compliant type hint test data to various global containers
    declared by the passed module.

    Parameters
    ----------
    data_module : ModuleType
        Module to be added to.

    .. _PEP 544:
        https://www.python.org/dev/peps/pep-0544
    '''

    # If the active Python interpreter targets less than Python < 3.8, this
    # interpreter fails to support PEP 544. In this case, reduce to a noop.
    if not IS_PYTHON_AT_LEAST_3_8:
        return
    # Else, the active Python interpreter targets at least Python >= 3.8 and
    # thus supports PEP 544.

    # ..................{ IMPORTS                           }..................
    # Defer Python >= 3.8-specific imports.
    from typing import (
        BinaryIO,
        Generic,
        IO,
        Protocol,
        SupportsAbs,
        SupportsBytes,
        SupportsFloat,
        SupportsIndex,
        SupportsInt,
        SupportsRound,
        TextIO,
        TypeVar,
        runtime_checkable,
    )

    # Type variables.
    S = TypeVar('S')
    T = TypeVar('T')

    # ..................{ PROTOCOLS                         }..................
    # User-defined protocol parametrized by *NO* type variables declaring
    # arbitrary concrete and abstract methods.
    @runtime_checkable
    class ProtocolCustomUntypevared(Protocol):
        def alpha(self) -> str:
            return 'Of a Spicily sated'

        @abstractmethod
        def omega(self) -> str: pass

    # User-defined protocol parametrized by a type variable declaring arbitrary
    # concrete and abstract methods.
    @runtime_checkable
    class ProtocolCustomTypevared(Protocol[T]):
        def alpha(self) -> str:
            return 'Gainfully ungiving criticisms, schismatizing Ŧheo‐'

        @abstractmethod
        def omega(self) -> str: pass

    # User-defined class structurally (i.e., implicitly) satisfying *WITHOUT*
    # explicitly subclassing this user-defined protocol.
    class ProtocolCustomStructural(object):
        def alpha(self) -> str:
            return "Sufferance's humus excursion, humility’s endurance, an"

        def omega(self) -> str:
            return 'Surfeit need'

    # Instance of this class.
    protocol_custom_structural = ProtocolCustomStructural()

    # User-defined protocol structurally (i.e., implicitly) satisfying
    # *WITHOUT* explicitly subclassing the predefined "typing.SupportsInt"
    # abstract base class (ABC).
    #
    # Note that the implementations of this and *ALL* other predefined "typing"
    # protocols (e.g., "typing.SupportsFloat") bundled with older Python
    # versions < 3.8 are *NOT* safely type-checkable at runtime. For safety
    # , tests against *ALL* protocols including these previously predefined
    # protocols *MUST* be isolated to this submodule.
    class ProtocolSupportsInt(object):
        def __int__(self) -> int:
            return 42

    # ..................{ SETS                              }..................
    # Add PEP 544-specific deeply ignorable test type hints to that set global.
    data_module.HINTS_PEP_IGNORABLE_DEEP.update((
        # Parametrizations of the "typing.Protocol" abstract base class (ABC).
        Protocol[S, T],
    ))

    # ..................{ TUPLES                            }..................
    # Add PEP 544-specific test type hints to this dictionary global.
    data_module.HINTS_PEP_META.extend((
        # ................{ GENERICS ~ io                     }................
        # Unsubscripted "IO" abstract base class (ABC).
        PepHintMetadata(
            hint=IO,
            pep_sign=Generic,
            generic_type=IO,
            is_typevared=True,
            piths_satisfied_meta=(
                # Open read-only file handle to this submodule.
                PepHintPithSatisfiedMetadata(
                    pith=lambda: open(_DATA_HINTPEP544_FILENAME, 'r'),
                    is_pith_factory=True,
                ),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'To piously magistrate, dis‐empower, and'),
            ),
        ),

        # Unsubscripted "BinaryIO" abstract base class (ABC).
        PepHintMetadata(
            hint=BinaryIO,
            pep_sign=Generic,
            generic_type=BinaryIO,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Open read-only binary file handle to this submodule.
                PepHintPithSatisfiedMetadata(
                    pith=lambda: open(_DATA_HINTPEP544_FILENAME, 'rb'),
                    is_pith_factory=True,
                ),
            ),
            piths_unsatisfied_meta=(
                # Bytestring constant.
                PepHintPithUnsatisfiedMetadata(
                    b"Of a thieved imagination's reveries"),
            ),
        ),

        # Unsubscripted "TextIO" abstract base class (ABC).
        PepHintMetadata(
            hint=TextIO,
            pep_sign=Generic,
            generic_type=TextIO,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Open read-only text file handle to this submodule.
                PepHintPithSatisfiedMetadata(
                    pith=lambda: open(_DATA_HINTPEP544_FILENAME, 'r'),
                    is_pith_factory=True,
                ),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'Statistician’s anthemed meme athame'),
            ),
        ),

        # ................{ PROTOCOLS ~ supports              }................
        # Unsubscripted "SupportsAbs" abstract base class (ABC).
        PepHintMetadata(
            hint=SupportsAbs,
            pep_sign=Generic,
            generic_type=SupportsAbs,
            # Oddly, some but *NOT* all "typing.Supports*" ABCs are
            # parametrized by type variables. *shrug*
            is_typevared=True,
            piths_satisfied_meta=(
                # Integer constant.
                PepHintPithSatisfiedMetadata(73),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('Scour Our flowering'),
            ),
        ),

        # Unsubscripted "SupportsBytes" abstract base class (ABC).
        PepHintMetadata(
            hint=SupportsBytes,
            pep_sign=Generic,
            generic_type=SupportsBytes,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Platform-agnostic filesystem path object constant.
                #
                # Note that exceedingly few stdlib types actually define the
                # __bytes__() dunder method. Among the few include classes
                # defined by the "pathlib" module, which is why we instantiate
                # such an atypical class here. See also:
                #     https://stackoverflow.com/questions/45522536/where-can-the-bytes-method-be-found
                PepHintPithSatisfiedMetadata(
                    pith=lambda: pathlib.Path('/'),
                    is_context_manager=True,
                    is_pith_factory=True,
                ),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'Fond suburb’s gibbet‐ribbed castrati'),
            ),
        ),

        #FIXME: Uncomment after we determine whether or not any stdlib classes
        #actually define the __complex__() dunder method. There don't appear to
        #be any, suggesting that the only means of testing this would be to
        #define a new custom "ProtocolSupportsComplex" class as we do above for
        #the "ProtocolSupportsInt" class. *shrug*
        # # Unsubscripted "SupportsComplex" abstract base class (ABC).
        # SupportsComplex: PepHintMetadata(
        #     pep_sign=Generic,
        #     piths_satisfied_meta=(
        #         # Integer constant.
        #         108,
        #     ),
        #     piths_unsatisfied_meta=(
        #         # String constant.
        #         PepHintPithUnsatisfiedMetadata('Fondled ΘuroƂorus-'),
        #     ),
        # ),

        # Unsubscripted "SupportsFloat" abstract base class (ABC).
        PepHintMetadata(
            hint=SupportsFloat,
            pep_sign=Generic,
            generic_type=SupportsFloat,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Integer constant.
                PepHintPithSatisfiedMetadata(92),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('Be’yond a'),
            ),
        ),

        # Unsubscripted "SupportsIndex" abstract base class (ABC) first
        # introduced by Python 3.8.0.
        PepHintMetadata(
            hint=SupportsIndex,
            pep_sign=Generic,
            generic_type=SupportsIndex,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Integer constant.
                PepHintPithSatisfiedMetadata(29),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('Self-ishly'),
            ),
        ),

        # Unsubscripted "SupportsInt" abstract base class (ABC).
        PepHintMetadata(
            hint=SupportsInt,
            pep_sign=Generic,
            generic_type=SupportsInt,
            is_subscripted=False,
            piths_satisfied_meta=(
                # Floating-point number constant.
                PepHintPithSatisfiedMetadata(25.78),
                # Structurally subtyped instance.
                PepHintPithSatisfiedMetadata(ProtocolSupportsInt()),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'Ungentlemanly self‐righteously, and'),
            ),
        ),

        # Unsubscripted "SupportsRound" abstract base class (ABC).
        PepHintMetadata(
            hint=SupportsRound,
            pep_sign=Generic,
            generic_type=SupportsRound,
            # Oddly, some but *NOT* all "typing.Supports*" ABCs are
            # parametrized by type variables. *shrug*
            is_typevared=True,
            piths_satisfied_meta=(
                # Floating-point number constant.
                PepHintPithSatisfiedMetadata(87.52),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'Our Fathers vowed, indulgently,'),
            ),
        ),

        # ................{ PROTOCOLS ~ user                  }................
        # Despite appearances, protocols implicitly subclass "typing.Generic"
        # and thus do *NOT* transparently reduce to standard types.
        #
        # Note that the "data_hintpep484" submodule already exercises
        # predefined "typing" protocols (e.g., "typing.SupportsInt"), which
        # were technically introduced with PEP 484 and thus available since
        # Python >= 3.4 or so.

        # User-defined protocol parametrized by *NO* type variables.
        PepHintMetadata(
            hint=ProtocolCustomUntypevared,
            pep_sign=Generic,
            generic_type=ProtocolCustomUntypevared,
            is_subscripted=False,
            is_type_typing=False,
            piths_satisfied_meta=(
                PepHintPithSatisfiedMetadata(protocol_custom_structural),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('For durance needs.'),
            ),
        ),

        # User-defined protocol parametrized by a type variable.
        PepHintMetadata(
            hint=ProtocolCustomTypevared,
            pep_sign=Generic,
            generic_type=ProtocolCustomTypevared,
            is_typevared=True,
            is_type_typing=False,
            piths_satisfied_meta=(
                PepHintPithSatisfiedMetadata(protocol_custom_structural),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata('Machist-'),
            ),
        ),

        # User-defined protocol parametrized by a type variable, itself
        # parametrized by the same type variables in the same order.
        PepHintMetadata(
            hint=ProtocolCustomTypevared[T],
            pep_sign=Generic,
            generic_type=ProtocolCustomTypevared,
            is_typevared=True,
            is_typing=False,
            piths_satisfied_meta=(
                PepHintPithSatisfiedMetadata(protocol_custom_structural),
            ),
            piths_unsatisfied_meta=(
                # String constant.
                PepHintPithUnsatisfiedMetadata(
                    'Black and white‐bit, bilinear linaements'),
            ),
        ),
    ))
