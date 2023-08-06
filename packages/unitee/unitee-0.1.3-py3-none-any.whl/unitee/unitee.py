from __future__ import annotations

import functools
import csv
from abc import abstractmethod
from collections import namedtuple
import pathlib
import types
from typing import Any, Mapping, Tuple, Iterable, Union, Callable


def _iter_csv_table(file, skiprows=1):
    with open(file, newline='') as fp:
        ireader = csv.reader(fp)
        next(ireader) # skip first row
        for line in ireader:
            yield line
            

Prefix = namedtuple('Prefix', ['symbol', 'name', 'val'])


class _UnitBaseCls:
    """
    Base class for creating Unit types.
    
    Each unit has a type, and unit instances have one attribute - `unit.prefix`.
    
    This class should not be used directly, instead new `Unit` types should be created using `UnitSystem.add_unit`.
    """

    unit_system: UnitSystem = None

    symbol: str = None
    name: str = None
    base: bool = None
    base_unit: _Quantity = None

    def __init__(self, prefix: str=''):
        self.prefix = self.unit_system.prefixes[prefix]

    @property
    def prefix_val(self) -> float:
        return self.prefix.val
        
    def as_quantity(self) -> _Quantity:
        return self.unit_system.Quantity(1, {self: 1})
        
    def with_prefix(self, prefix:str ='') -> _UnitBaseCls:
        """
        Returns new Unit instance with different prefix
        """
        return self.__class__(prefix)
        
    def __str__(self) -> str:
        return f"{self.prefix.symbol}{self.symbol}"
        
    @property
    def long_name(self) -> str:
        """
        string representation without symbols
        """
        return f"{self.prefix.name} {self.name}" if self.prefix.symbol else self.name
        
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} prefix='{self.prefix}'>"
        
    def __hash__(self) -> int:
        return hash((self.prefix, self.symbol))
        
    def __eq__(self, other: Any) -> bool:
        return self.prefix == other.prefix and self.symbol == other.symbol


class UnitSystem:
    """
    Base class for defining unit systems i.e. a set of prefixes, units and constants.
    
    Also parses expressions to create `Quantity` objects.
    """

    linear_fmt: str = '{unit.prefix.symbol}{unit.symbol}'
    exp_fmt: str = '{unit.prefix.symbol}{unit.symbol}^{exp}'
    suffix_sep: str = ' '
    unit_sep: str = '.'

    def __init__(self):
        class Quantity(_Quantity):
            unit_system = self
        
        self.Quantity: _Quantity = Quantity
        
        class UnitBaseCls(_UnitBaseCls):
            unit_system = self
            
        self.UnitBaseCls: _UnitBaseCls = UnitBaseCls
        
        self.prefixes: Mapping[str, Prefix] = {}
        self._units: Mapping[str, _UnitBaseCls] = {}
        self.consts: Mapping[str, _Quantity] = {}
        
        self.load_prefixes()
        self.load_base_units()
        self.load_derived_units()
        self.load_consts()
        
    @property
    def units(self) -> MappingProxyType:
        """
        Immutable copy of `self._units`, prevents naughty manual insersion of units!
        """
        return types.MappingProxyType(self._units)
        
    @property
    def config_dir(self) -> pathlib.Path:
        """
        Directory where configuration csvs are loaded from by default
        """
        return pathlib.Path(__file__).parent
        
    def add_unit(self, symbol: str, name: str, base_unit: bool, base: _Quantity=None) -> _UnitBaseCls:
        """
        Add a new unit to this UnitSystem
        """
        Unit = type(f'Unit<{name}({symbol})>', (self.UnitBaseCls,), 
                    {'symbol': symbol, 'name': name, 'base': base, 'base_unit': base_unit})

        if base is None:
            Unit.base = Unit().as_quantity()

        self._units[symbol] = Unit
        return Unit
        
    def parse_expr(self, expr: str) -> _Quantity:
        """
        Parse a unit expression into a Quantity.
        
        expr must be a series of units and exponents, separated by `'.'` with no spaces. Exponents can just be integers, or separated by `'^'` e.g.
        
            >>> SI.parse_expr('kg.m.s-2')
            1.0 kg.m.s^-2
        """    
        
        if not expr:
            return 1.0

        if '/' in expr:
            raise ValueError("Cannot parse expressions using /, please use negative powers")
        expr = expr.replace('^', '')  # no need
        parts = expr.split('.')
        out = 1.0
        
        for part in parts:
            part = list(part)
            symbol = []
            
            while part and part[0].isalpha():
                symbol.append(part.pop(0))
            
            symbol = ''.join(symbol)
            exp = ''.join(part)
            
            if exp:
                exp = int(exp)
            else:
                exp = 1
            
            out *= self.get_unit(symbol) ** exp
        
        return out
    
    def parse_name(self, name: str) -> Tuple[str, str]:
        """
        Splits a name into a prefix and symbol e.g.
        
            >>> SI.parse_name('km')
            ('k', 'm')
        
        Only works with symbols, not names.
        """
        if name in self.units:
            return '', name
        
        try:
            prefix, *symbol = name
        except ValueError:
            raise ValueError(f"Cannot parse name {name}")
        
        symbol = ''.join(symbol)
        
        if prefix in self.prefixes and symbol in self.units:
            return prefix, symbol
        
        raise ValueError(f"Cannot parse name {name}")
        
    def get_unit(self, name: str) -> _Quantity:
        """
        Gets a `Quantity` representing a unit (including prefix) from its name.
        """
        prefix, symbol = self.parse_name(name)
        
        if symbol not in self.units:
            raise ValueError(f"Cannot find unit matching symbol {symbol}")
        
        Unit = self.units[symbol]
        return Unit(prefix).as_quantity()
        
    def order_units(self, units: Mapping[str, _UnitBaseCls]) -> Iterable[_UnitBaseCls, int]:
        """
        Used to order units before rendering.
        """
        return sorted(((unit, exp) for unit, exp in units.items()), key=lambda v: (-v[-1], v[-2].symbol))
        
    def format_suffix(self, ordered_units: Iterable[_UnitBaseCls, int]) -> str:
        """
        Create a suffix string for a given iterable of units. This is added to the float representation of a `Quantity`.
        """
        return self.suffix_sep + self.unit_sep.join(self.linear_fmt.format(unit=unit) if exp == 1 else
                                                    self.exp_fmt.format(unit=unit, exp=exp) for unit, exp in ordered_units)

    def __getitem__(self, name: str) -> _Quantity:
        """
        Get a constant by its symbol
        """
        return self.consts[name]

    def __call__(self, expr: str) -> _Quantity:
        """
        Parse a string representation of a Quantity, i.e. a scalar and its units.
        
        units and scalar are separated by a `' '`.
        
        units are parsed with `self.parse_expr`.
        """
        try:
            val, units = expr.split(' ')
        except ValueError:
            val = 1.0
            units = expr
        return float(val) * self.parse_expr(units)
        
    def __getattr__(self, name: str) -> Any:
        try:
            return self.__call__(name)
        except ValueError:
            raise AttributeError(name)
        
    @abstractmethod
    def load_prefixes(self) -> None:
        """
        Method called to fill `self.prefixes`. Automatically called during creation of a `UnitSystem` instance. Called first.
        """
        pass

    @abstractmethod
    def load_base_units(self) -> None:
        """
        Method called to fill `self._units` with base units. Automatically called during creation of a `UnitSystem` instance. Called second.
        """
        pass
        
    @abstractmethod
    def load_derived_units(self) -> None:
        """
        Method called to fill `self._units` with derived_units units. Automatically called during creation of a `UnitSystem` instance. Called third.
        """
        pass
        
    @abstractmethod
    def load_consts(self) -> None:
        """
        Method called to fill `self.consts`. Automatically called during creation of a `UnitSystem` instance. Called forth.
        """
        pass


class SISystem(UnitSystem):
    """
    SI unit system. As defined https://simple.wikipedia.org/wiki/International_System_of_Units
    """
    
    def load_prefixes(self):        
        for name, symbol, value in _iter_csv_table(self.config_dir / 'prefixes.csv'):
            self.prefixes[symbol] = Prefix(name=name, symbol=symbol, val=float(value))

    def load_base_units(self):
        for name, symbol in _iter_csv_table(self.config_dir / 'base_units.csv'):
            self.add_unit(symbol, name, True, None)

    def load_derived_units(self):
        for name, symbol, val, expr in _iter_csv_table(self.config_dir / 'derived_units.csv'):
            if expr: 
                val = float(val)
                base = self.parse_expr(expr)
                self.add_unit(symbol, name, False, val * base)
            else:
                self.add_unit(symbol, name, False, None)
                    
    def load_consts(self):
        for name, val, units in _iter_csv_table(self.config_dir / 'consts.csv'):
            self.consts[name] = float(val) * self.parse_expr(units)


class _Quantity(float):

    unit_system: UnitSystem = None
    
    def __new__(cls, val: float, units: Mapping[_UnitBaseCls, int]=None):
        obj = super().__new__(cls, val)
        
        if units is None:
            units = {}
            
        obj._units: Mapping[_UnitBaseCls, int] = units
        obj._is_base: bool = all(unit.base_unit for unit in units)

        return obj
        
    @property
    def units(self) -> _Quantity:
        """
        Quantity representation of units
        """
        out = 1.0
        for unit, exp in self._units.items():
            out *= unit.as_quantity() ** exp
        return out
    
    @property
    def scalar(self) -> float:
        """
        Scalar value of self (ignores prefixes)
        """
        return float(self)
        
    @property
    def is_base(self):
        return self._is_base
        
    def _reciprocate_units(self):
        return {unit: -exp for unit, exp in self._units.items()}
    
    def _combine_unit_dict(self, first, second):        
        new = first.copy()
        for unit, exp in second.items():
            if unit in new:
                new[unit] += exp
            else:
                new[unit] = exp
        return new
        
    def _change_unit(self, current: _Quantity, to: _Quantity, safe: bool=True) -> _Quantity:
        current_factor = current.to_base()
        to_factor = to.to_base()
        
        if safe and not current_factor.comparable(to_factor):
            raise ValueError(f"Trying to swap non-equivalent units: {current} and {to}")
        
        return self * (current_factor / to_factor) * to / current

    def combinable(self, other: Any) -> bool:
        """
        Does `other` share the same units to `self`?
        """
        return isinstance(other, self.unit_system.Quantity) and self._units == other._units
        
    def comparable(self, other: Any) -> bool:
        """
        Are `other`'s units equivalent to `self`?
        """
        return isinstance(other, self.unit_system.Quantity) and self.to_base()._units == other.to_base()._units
        
    def no_prefix(self) -> _Quantity:
        """
        New `Quantity` with all prefixes removed - maintains equivalent value
        """
        factor = 1
        for unit, exp in self._units.items():
            factor *= unit.prefix_val ** exp
        return self.__class__(self * factor, {unit.with_prefix(''): exp for unit, exp in self._units.items()})

    def to_base(self) -> _Quantity:        
        """
        Create new `Quantity` from `self`, but with all units converted to `base` units. (Also removes prefixes).
        """
        out = self.no_prefix()
        
        for unit, exp in out._units.items():
            out *= (unit.base ** exp) / (unit.as_quantity() ** exp)
        return out
        
    def swap(self, current: Union[str, _Quantity], to: Union[str, _Quantity], safe: bool=True) -> _Quantity:
        """
        Create new `Quantity`, but with `current` unit substituted for `to`. 
        
        If `safe=True`, will check if `current` and `to` are equivalent, and raise an exception if not.
        
        Accepts `str` or `Quantity`s as `current` or `to`.
        """
        if isinstance(current, str):
            current = self.unit_system.parse_expr(current)
        if isinstance(to, str):
            to = self.unit_system.parse_expr(to)
        
        return self._change_unit(current, to, safe=safe)
    
    def to(self, to: Union[str, _Quantity]) -> _Quantity:
        """
        Shorthand for `self.change_unit(self.units, to, True)` i.e. create a new `Quantity` where all of `self`'s units have been replaced by `to`.
        """
        if isinstance(to, str):
            to = self.unit_system.parse_expr(to)
        return self._change_unit(self.units, to, True)
        
    def _uniterize(method: Callable[[Any], Mapping[_UnitBaseCls, int]]) -> Callable[[Any], _Quantity]:
        """
        Convert a float to one that returns a Quantity.
        
        The wrapped method must return the appropriate units after that operation (not perform the operation itself!)
        """
        @functools.wraps(method)
        def wrapped(self, other):
            result = self.__class__(getattr(super(), method.__name__)(other))
            return self.unit_system.Quantity(result, {k: v for k, v in method(self, other).items() if v != 0})
        return wrapped
        
    def _require_combinable(method: Callable[[Any], _Quantity]) -> Callable[[Any], _Quantity]:
        """
        Wraps a method in a combinability check.
        """
        @functools.wraps(method)
        def wrapped(self, other):
            if not self.combinable(other):
                raise ValueError(f"Tried to {method.__name__} with quantities without matching units: {self} and {other}")
            return method(self, other)
        return wrapped
        
    def _try_make_comparable(method: Callable[[Any], _Quantity]) -> Callable[[Any], _Quantity]:
        """
        Try to convert self and other to make comparable
        """
        @functools.wraps(method)
        def wrapped(self, other):
            if not self.combinable(other) and not self.comparable(other):
                raise ValueError(f"Tried to {method.__name__} with inequivalent units: {self} and {other}")
            elif not self.is_base or not other.is_base:
                return getattr(self.to_base(), method.__name__)(other.to_base())
            
            return method(self, other)
        return wrapped
            
    @_uniterize
    @_require_combinable
    def __add__(self, other):
        return self._units
            
    @_uniterize
    @_require_combinable
    def __radd__(self, other):
        return self._units
            
    @_uniterize
    @_require_combinable
    def __sub__(self, other):
        return self._units
            
    @_uniterize
    @_require_combinable
    def __rsub__(self, other):
        return self._units
    
    @_uniterize
    def __pow__(self, other):
        if isinstance(other, self.unit_system.Quantity):
            raise ValueError("Cannot raise to the power of other units")
        return {unit: exp * other for unit, exp in self._units.items()}

    @_uniterize
    def __mul__(self, other):
        if isinstance(other, self.unit_system.Quantity):
            return self._combine_unit_dict(self._units, other._units)
        return self._units

    @_uniterize
    def __rmul__(self, other):
        if isinstance(other, self.unit_system.Quantity):
            return self._combine_unit_dict(self._units, other._units)
        return self._units

    @_uniterize
    def __truediv__(self, other):
        if isinstance(other, self.unit_system.Quantity):
            return self._combine_unit_dict(self._units, other._reciprocate_units())
        return self._units

    @_uniterize
    def __rtruediv__(self, other):
        if isinstance(other, self.unit_system.Quantity):
            return self._combine_unit_dict(self._reciprocate_units(), other._units)
        return self._units
    
    @_try_make_comparable
    def __eq__(self, other):
        return super().__eq__(other)
    
    @_try_make_comparable
    def __ne__(self, other):
        return super().__ne__(other)
       
    @_try_make_comparable
    def __lt__(self, other):
        return super().__lt__(other)

    @_try_make_comparable
    def __le__(self, other):
        return super().__le__(other)
        
    @_try_make_comparable
    def __gt__(self, other):
        return super().__gt__(other)
        
    @_try_make_comparable
    def __ge__(self, other):
        return super().__ge__(other)
        
    def __iter__(self):
        return iter(self._units.items())

    def __repr__(self):
        return super().__repr__() + self.unit_system.format_suffix(self.unit_system.order_units(self._units))
    
    def __str__(self):
        return self.__repr__()
            
    def __format__(self, spec):
        suffix = self.unit_system.format_suffix(self.unit_system.order_units(self._units))
        return super().__format__(spec) + suffix if spec else super().__str__() + suffix


SI = SISystem()
