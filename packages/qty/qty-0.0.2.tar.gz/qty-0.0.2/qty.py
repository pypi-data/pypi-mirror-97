#!/usr/bin/env python3
"""A Python library for dealing with physical quantities"""

__version__ = '0.0.2'

import keyword

import numpy as np
import scipy.constants as const


PREFIXES = {
    'Y': const.yotta,
    'Z': const.zetta,
    'E': const.exa,
    'P': const.peta,
    'T': const.tera,
    'G': const.giga,
    'M': const.mega,
    'k': const.kilo,
    'h': const.hecto,
    'da': const.deka,
    'd': const.deci,
    'c': const.centi,
    'm': const.milli,
    'u': const.micro,
    'n': const.nano,
    'p': const.pico,
    'f': const.femto,
    'a': const.atto,
    'z': const.zepto,
}


def _add_prefix(BaseClass: object, prefix: str, multiplier: float) -> None:
    """Create rescaled descriptor."""

    class NewClass(BaseClass):

        def __get__(self, instance, owner):
            return super().__get__(instance, owner) / multiplier

        def __set__(self, instance, value):
            super().__set__(instance, value * multiplier)

    # Add trailing underscore if name conflicts with built-in keywords.
    name = prefix + BaseClass.__name__[1:]
    if name in keyword.kwlist:
        NewClass.__name__ = name + '_'
        NewClass.__qualname__ = name + '_'
    else:
        NewClass.__name__ = name
        NewClass.__qualname__ = name

    return NewClass


class Quantity:

    def __init_subclass__(cls, units):
        for unit in units:
            old_class = getattr(cls, '_' + unit)
            for key, value in PREFIXES.items():
                new_class = _add_prefix(old_class, key, value)
                setattr(cls, new_class.__name__, new_class())

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        args = []
        for i, input_ in enumerate(inputs):
            if isinstance(input_, self.__class__):
                args.append(input_._value)
            else:
                args.append(input_)
        new = self.__class__()
        new._value = getattr(ufunc, method)(*args, **kwargs)
        return new

    def __add__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.add, '__call__', self, other)
        else:
            raise Exception("Incompatible quantities.")

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.equal, '__call__', self, other)
        else:
            raise Exception("Incompatible quantities.")

    def __ne__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.not_equal, '__call__', self, other)
        else:
            raise Exception("Incompatible quantities.")

    def __le__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.less_equal, '__call__', self, other)
        else:
            raise Exception("Incompatible quantities.")

    def __lt__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.less, '__call__', self, other)
        else:
            raise Exception("Incompatible quantities.")

    def __mul__(self, other):
        return self.__array_ufunc__(np.multiply, '__call__', self, other)

    def __neg__(self):
        return self.__array_ufunc__(np.negative, '__call__', self)

    def __pos__(self):
        return self.__array_ufunc__(np.positive, '__call__', self)

    def __radd__(self, other):
        if self.__class__ == other.__class__:
            return self.__array_ufunc__(np.add, '__call__', other, self)
        else:
            raise Exception("Incompatible quantities.")

    def __rmul__(self, other):
        return self.__array_ufunc__(np.multiply, '__call__', other, self)

    def __truediv__(self, other):
        return self.__array_ufunc__(np.true_divide, '__call__', self, other)


class Energy(Quantity, units=['J', 'eV', 'm', 'K', 'Hz', 's', 'Ha']):
    r"""Energy units.

    Available units:

        * Joule [J]
        * Electronvolt [eV]
        * Meter [m]
        * Kelvin [K]
        * Hertz [Hz]
        * Second [s]
        * Hartree [Ha]

    Units are related by the following equalities:

    .. math::
        E[\text{J}] &= E[\text{eV}] \times e[\text{C}] \times [\text{J} \cdot \text{C}^{-1} \cdot \text{eV}^{-1}]\\
	    E[\text{J}] &= h[\text{J} \cdot \text{s}] \times c[\text{m} \cdot \text{s}^{-1}] \times (\lambda[\text{m}])^{-1}\\
	    E[\text{J}] &= k_B[\text{J} \cdot \text{K}^{-1}] \times T[\text{K}]\\
	    E[\text{J}] &= h[\text{J} \cdot \text{s}] \times ν[\text{Hz}] \times [\text{Hz}^{-1} \cdot \text{s}^{-1}]\\
	    E[\text{J}] &= h[\text{J} \cdot \text{s}] \times (ν^{-1}[\text{s}])^{-1}\\
	    E[\text{J}] &= E[\text{Ha}] \times m_e[\text{kg}] \times (c[\text{m} \cdot \text{s}^{-1}])^2 \times \alpha^2 \times [\text{Ha}^{-1}] \\

    .. note::
        Due to a conflict with the built-in Python keyword `as`, use `as_`
        for attoseconds.
    """

    class _J:

        def __get__(self, instance, owner):
            return getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', value)

    class _eV:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / const.eV

        def __set__(self, instance, value):
            setattr(instance, '_value', value * const.eV)

    class _m:

        def __get__(self, instance, owner):
            return const.h * const.c / getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', const.h * const.c / value)

    class _K:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / const.k

        def __set__(self, instance, value):
            setattr(instance, '_value', value * const.k)

    class _Hz:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / const.h

        def __set__(self, instance, value):
            setattr(instance, '_value', value * const.h)

    class _s:

        def __get__(self, instance, owner):
            return const.h / getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', const.h / value)

    class _Ha:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / (const.m_e * const.c**2 * const.alpha**2)

        def __set__(self, instance, value):
            setattr(instance, '_value', value * const.m_e * const.c**2 * const.alpha**2)

    J = _J()
    eV = _eV()
    m = _m()
    K = _K()
    Hz = _Hz()
    s = _s()
    Ha = _Ha()


class Length(Quantity, units=['m', 'A']):
    r"""Length units.

    Available units:

        * Meter [m]
        * Ångström [Å]

    Units are related by the following equality:

    .. math::
        l[\text{m}] = l[\text{Å}] \times 10^{-10}[\text{m} \cdot \text{Å}^{-1}]

    .. note::
        The ångström symbol (Å) has been substituted with a capital A
        in the module for convenience.
    """

    class _m:

        def __get__(self, instance, owner):
            return getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', value)

    class _A:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') * const.angstrom

        def __set__(self, instance, value):
            setattr(instance, '_value', value / const.angstrom)

    m = _m()
    A = _A()


class Temperature(Quantity, units=['K', 'C', 'F']):
    r"""Temperature units.

    Available units:
        * Kelvin [K]
        * Degree Celsius [℃]
        * Degree Farenheit [℉]

    Units are related by the following equalities:

    .. math::
        T[\text{K}] &= 1[\text{K} \cdot \text{℃}^{-1}] \times T[\text{℃}] + 273.15[\text{K}]

        T[℉] &= 1.8[\text{F} \cdot \text{℃}^{-1}] \times T[\text{℃}] + 32[\text{℉}]

    .. note::
        The degree sign from the degree Celsius (℃) and degree Farenheit (℉)
        symbols has been omitted in the module for convenience.
    """

    class _K:

        def __get__(self, instance, owner):
            return getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', value)

    class _C:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') - 273.15

        def __set__(self, instance, value):
            setattr(instance, '_value', value + 273.15)

    class _F:

        def __get__(self, instance, owner):
            return (getattr(instance, '_value') - 273.15) * 1.8 + 32.

        def __set__(self, instance, value):
            setattr(instance, '_value', (value -32.) / 1.8 + 273.15)

    K = _K()
    C = _C()
    F = _F()


class Time(Quantity, units=['s', 'min', 'h']):
    r"""Time units.

    Available units:

        * Second [s]
        * Minutes [min]
        * Hour [h]

    Units are related by the following equalities:

    .. math::
        t[\text{min}] &= 60[\text{s} \cdot \text{min}^{-1}] × t[\text{s}]

        t[\text{h}] &= 60[\text{min} \cdot \text{h}^{-1}] × t[\text{h}]

    .. note::
        Due to a conflict with the built-in Python keyword `as`, use `as_`
        for attoseconds.
    """

    class _s:

        def __get__(self, instance, owner):
            return getattr(instance, '_value')

        def __set__(self, instance, value):
            setattr(instance, '_value', value)

    class _min:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / 60.

        def __set__(self, instance, value):
            setattr(instance, '_value', value * 60.)

    class _h:

        def __get__(self, instance, owner):
            return getattr(instance, '_value') / 3600.

        def __set__(self, instance, value):
            setattr(instance, '_value', value * 3600.)

    s = _s()
    min = _min()
    h = _h()

if __name__ == '__main__':
    pass

