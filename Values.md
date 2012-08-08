Value System
============

The basic OctopusCalc can handle a number of value types, the simplest being Nothing.
> null -> {Nothing}

There is also the Boolean, either being true or false.
> true  -> {Boolean value: true}
> false -> {Boolean value: false}

Numbers come in a few different flavours, the most basic being the Integer.
> 4 -> {Integer value: 4}
Integers can be as large as you want and as negative as you want.

Fractions are whole number fractions, consisting of a numerator and a denominator.
> 4/5 -> {Fraction top: {Integer value: 4} bottom: {Integer value: 5}}

Decimals are base 10 floating point numbers, and are essentially the same as scientific notation.
> 4.5 -> {Decimal value: {Integer value: 45} power: {Integer value: 0} sigfigs: {Integer value: 2}}
> 5.34e10 -> {Decimal value: {Integer value: 534} power: {Integer value: 10} sigfigs: {Integer value: 3}}

Irrationals are any real number that doesn't have one of these representations. They have no calculated value unless that value is required.
> pi -> {Irrational value: 'pi'}

Quantities are Values with a Unit added.
> 3.0 km -> {Quantity value: {Decimal value: {Integer value: 30} power: {Integer value:0} sigfigs: {Integer value: 2}} unit: {Unit name: 'km'}}
> pi rad -> {Quantity value: {Irrational value: 'pi'} unit: {Unit name: 'rad'}}

A Text is a series of characters:
> "Hello, world!" -> {Text value:'Hello, world!'}

Objects are generally defined in datafiles and store a number of values:
> cat -> {Object name: {Text value:'cat'} isAnimal: {Boolean value:'true'}}

Using values
------------

Values can be used by invoking functions on them, such as '+':
> 2 + 2    -> {Integer value: 4}

This also works with different types of values, as long as it makes sense:
> 12 + 2.3 -> {Decimal value: {Integer value: 14} power: {Integer value: 1} sigfigs: {Integer value: 2}}
> 4.00 m + 50 cm -> {Quantity value: {Decimal value: {Integer value: 450} power: {Integer value:0} sigfigs: {Integer value: 3}} unit: {Unit name: 'm'}}

Functions can also (need to) be put in front:
> sqrt 4 -> {Integer value: 2}
> add 4, 5, 10 -> {Integer value: 19}

Objects' properties are accessed in this way:
> [cat isAnimal] -> {Boolean: true}
You can also do this with other values than objects:
> [4.5 sigfigs] -> {Integer: 2}

Conversion is a special type of function:
> 3000 m => km -> {Quantity value: {Integer value: 3} unit: {Unit name: km}}