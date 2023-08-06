# Unitee

Unitee is an attempt to add physical units to Python in the neatest way possible.

The approach Unitee takes is to extend the `float` minimally, adding a units attribute and tweaking its methods.

Unitee is somewhat of a proof of concept as I wanted to see how easily and powerfully this functionality can be added to Python.

In practice as a hobby project, I would thoroughly recommend those looking for a serious route to support units make use of [Pint](https://github.com/hgrecco/pint) this library is more complete, tested and is actually quite similarly structured (coincidence?).

## Usage

The core of Unitee is the `UnitSystem` object, this stores information about the unit system you want to use and provide tools to make use of it. You can define your own `UnitSystem`, or simply make use of the ready made `unitee.SI` system, which includes the units and constants of the [International System of Units](https://simple.wikipedia.org/wiki/International_System_of_Units), I would expect this is sufficient for the majority of users. 

To get started

    >>> from unitee import SI
    >>> SI
    <unitee.SISystem object at 0x000002A1A819A5F8>

Scalars alongside units are known as Quantities, there are a number of ways to easily create the `Quantity` objects you want:

    >>> L = SI('10 nm')  # SI can be treated like a constructor. scalar and units are separated by a space
    >>> L
    10.0 nm
    >>> nanometer = SI('nm')  # omitting the scalar, it's assumed to be 1
    >>> nanometer
    1.0 nm
    >>> L = 10 * SI('nm')  # hence, this works
    >>> L
    10.0 nm
    >>> L = 10 * SI.nm  # __getattr__ calls are redirected to SI.__call__, so units that work as attribute names can be accessed this way (cheeky!)
    >>> L
    10.0 nm
    >>> F = SI('25 kg.m.s-2')  # complex units work too, these are separated with '.', exponents follow the unit.
    >>> F
    25.0 kg.m.s^-2

Operatations work as I hope you'd expect:

    >>> distance = 15 * SI.km
    >>> time = 1.5 * SI.h
    >>> speed = distance / time  # division works as expected
    >>> speed
    10.0 km.h^-1  # negative powers are used rather than /
    >>> throw = SI('10 m.s-1')
    >>> net = speed + throw  # adding or subtracting quantities without matching units is forbidden, because the way to cast units is ambigous
    ValueError: Tried to __add__ with quantities without matching units: 10.0 m.s^-1 and 10.0 mi.h^-1
    >>> net = speed + throw.to('km.h-1')  # but matching units is fine
    >>> net 
    46.0 km.h^-1
    >>> net > throw  # but comparisons between equivalent units are allowed
    True
    >>> distance > throw  # comparisons between non-equivalent units is not!
    ValueError: Tried to __gt__ with inequivalent units: 15.0 km and 10.0 m.s^-1

Two methods exist for unit conversion, `Quantity.to`:

    >>> speed = SI('10 km.h-1')
    >>> speed.to('m.s-1')  # tries to replace all the units with the new unit
    2.7777777777777777 m.s^-1
    >>> speed.to('J')  # will complain if the new unit isn't equivalent
    ValueError: Trying to swap non-equivalent units: 1.0 km.h^-1 and 1.0 J
    
and `Quantity.swap`:

    >>> speed = SI('10 km.h-1')    
    >>> speed.swap('m', 'km') # tries to swap one unit for another equivalent unit
    10000.0 m.h^-1
    >>> F = SI('15 kg.m.s-2') 
    >>> F.swap('kg.m.s-2', 'N')  # can do complex swapping!
    15.0 N 
    >>> F.swap('kg.m.s-2', 'J', safe=False)  # for dangerous swapping, use safe=False
    15.0 J.m^-1  # your answer will still follow the laws of physics!

`unitee` can tell when units are equivalent because it understands how units break up into the fundamental base units e.g.

    >>> F = SI('300 kN')
    >>> F.to_base()
    300000.0 kg.m.s^-2
    >>> charge = 15 * SI.C
    >>> charge.to_base()
    15.0 A.s

The base units are defined relative to fundamental constants, which can also be accessed:
    
    >>> electron_charge = SI['e']
    >>> e
    1.602176634e-19 C
    >>> list(SI.consts.keys())
    ['dV_Cs', 'c', 'h', 'e', 'B_k', 'N_A']
    
Because `Quantity` objects are instances of `float`, they play ok with other libaries:

    >>> import numpy as np
    >>> angle = np.pi / 2 * SI('rad')
    >>> angle
    1.5707963267948966 rad
    >>> np.sin(angle)
    1.0
    >>> import math
    >>> math.sin(angle)
    1.0

But be cautious, because other libaries don't know about `unitee` and will just use the scalar value of your `Quantity`:

    >>> math.sin(angle.to('deg'))
    0.8939966636005579
    >>> np.sin(angle.to('deg'))
    0.8939966636005579
    
[Pint](https://github.com/hgrecco/pint) has been written to make units work with numpy, this is probably your best option if you are doing lots of calculations and wanting to involve units. I see `unitee` being used for little sums and maybe on the in and out end of things.    

All `Quantity` objects are immutable hence all operations result in a new `Quantity` being created.

## Customising

Depending on how much you want to customise `unitee`'s behaviour, you can do a few things.

You can add new units on the fly to the `SISystem`, using `SI.add_unit`:

    >>> SI.add_unit('in', 'inches', False, SI('2.54 cm'))
    
Or you can subclass `UnitSystem` and create your own. You can overwrite the `load_prefixes`, `load_base_units`, `load_derived_units` and `load_consts` methods. These should fill in the `self.prefixes`, `self._units` ... `self._units` and `self.consts` attributes. 

By default, `unitee` will look for `csv` files defining a new unit system in `pathlib.Path.home() / '.unitee' / self.__class__.__name__`. 

The rendering of `Quantities` can be customised via the `linear_fmt`, `exp_fmt`, `suffix_sep` and `unit_sep` `UnitSystem` class attributes, or by overwriding the whole `UnitSystem.format_suffix` method.

The ordering of units can be customised by overwriding the `UnitSystem.order_units` method. 