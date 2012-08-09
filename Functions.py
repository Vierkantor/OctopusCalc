import math

from Value import Value, Nothing, Boolean, Integer, Fraction, Decimal

def fun_convert(a, b):
	if issubclass(type(a), Value) and issubclass(b, Value):
		return a.Convert(b);
	else:
		raise ValueError("Cannot convert that way.");

# since apparently Python doesn't feel the need to support overloading, we'll have to redefine most of the basic operations
def fun_and (a, b):
	a = a.Convert(Boolean);
	b = b.Convert(Boolean);
	return Boolean(a.value and b.value);

def fun_or (a, b):
	a = a.Convert(Boolean);
	b = b.Convert(Boolean);
	return Boolean(a.value or b.value);

def fun_equals (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		a.Truncate(b.sigFigs());
		b.Truncate(a.sigFigs());
		return fun_and(fun_equals(a.value, b.value), fun_equals(a.power, b.power));
	elif type(a) == Fraction or type(b) == Fraction:
		# a/b == c/d <=> ad == bc (so no simplification needed)
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return fun_equals(fun_mult(a.top, b.bottom), fun_mult(a.bottom, b.top));
	elif type(a) == Integer or type(b) == Integer:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Boolean(a.value == b.value);
	else:
		a = a.Convert(Boolean);
		b = b.Convert(Boolean);
		return Boolean(a.value == b.value);

def fun_greater (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		a = a.Truncate(b.sigFigs());
		b = b.Truncate(a.sigFigs());
		return fun_or(fun_greater(a.power, b.power), fun_and(fun_equals(a.power, b.power), fun_greater(a.value, b.value)));
	elif type(a) == Fraction or type(b) == Fraction:
		# a/b > c/d <=> ad/bd > bc/bd <=> ad > bc
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return fun_greater(fun_mult(a.top, b.bottom), fun_mult(b.top, a.bottom));
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Boolean(a.value > b.value);

def fun_add (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		if (a.power.value < b.power.value):
			a, b = b, a;
		return Decimal((a.value.value * 10 ** (a.power.value - b.power.value) + b.value.value) // 10 ** (a.power.value - b.power.value), a.power);
	elif type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_add(fun_mult(a.top, b.bottom), fun_mult(a.bottom, b.top)), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value + b.value);

def fun_sub (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		if (a.power.value < b.power.value):
			a, b = b, a;
			return Decimal(int((-a.value.value * 10 ** (a.power.value - b.power.value)) + b.value.value) // 10 ** (a.power.value - b.power.value), a.power);
		else:
			return Decimal(int((a.value.value * 10 ** (a.power.value - b.power.value)) - b.value.value) // 10 ** (a.power.value - b.power.value), a.power);
	elif type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_sub(fun_mult(a.top, b.bottom), fun_mult(a.bottom, b.top)), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value - b.value);

def fun_mult (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		return Decimal(fun_mult(a.value, b.value), fun_add(a.power, b.power)).Truncate(min(a.sigFigs(), b.sigFigs()));
	elif type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_mult(a.top, b.top), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value * b.value);

def fun_div (a, b):
	if type(a) == Decimal or type(b) == Decimal:
		a = a.Convert(Decimal);
		b = b.Convert(Decimal);
		c = fun_div(a.value, b.value).Convert(Decimal);	# preserves precision
		c.power = fun_add(c.power, fun_sub(a.power, b.power));
		return c.Truncate(min(a.sigFigs(), b.sigFigs()));
	elif type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_mult(a.top, b.bottom), fun_mult(b.top, a.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Fraction(a.value, b.value).Simplify();

def fun_pow (a, b):
	# TODO: (fraction, fraction) requires higher power roots and that is something not ready yet
	if type(a) == Fraction and type(b) == Integer:
		return Fraction(fun_pow(a.top, b), fun_pow(a.bottom, b)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value ** b.value);

def fun_mod (a, b):
	a = a.Convert(Integer);
	b = b.Convert(Integer);
	return Integer(a.value % b.value);

# not very basic but handy for fraction arithmetic
def fun_gcd (a, b):
	a = a.Convert(Integer);
	b = b.Convert(Integer);
	if fun_greater(b, a).value:
		a, b = b, a
	if fun_equals(b, Integer(0)).value:
		return a;
	else:
		return fun_gcd(b, fun_mod(a, b));