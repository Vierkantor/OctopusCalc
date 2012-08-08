from Value import Value, Nothing, Boolean, Integer, Fraction

# since apparently Python doesn't feel the need to support overloading, we'll have to redefine most of the basic operations
def fun_and (a, b):
	a = a.Convert(Boolean);
	b = b.Convert(Boolean);
	return Boolean(a.value and b.value);

def fun_equals (a, b):
	if type(a) == Fraction or type(b) == Fraction:
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
	if type(a) == Fraction or type(b) == Fraction:
		# a/b > c/d <=> ad/bd > bc/bd <=> ad > bc
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return fun_greater(fun_mult(a.top, b.bottom), fun_mult(b.top, a.bottom));
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Boolean(a.value > b.value);

def fun_add (a, b):
	if type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_add(fun_mult(a.top, b.bottom), fun_mult(a.bottom, b.top)), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value + b.value);

def fun_sub (a, b):
	if type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_sub(fun_mult(a.top, b.bottom), fun_mult(a.bottom, b.top)), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value - b.value);

def fun_mult (a, b):
	if type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_mult(a.top, b.top), fun_mult(a.bottom, b.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Integer(a.value * b.value);

def fun_div (a, b):
	if type(a) == Fraction or type(b) == Fraction:
		a = a.Convert(Fraction);
		b = b.Convert(Fraction);
		return Fraction(fun_mult(a.top, b.bottom), fun_mult(b.top, a.bottom)).Simplify();
	else:
		a = a.Convert(Integer);
		b = b.Convert(Integer);
		return Fraction(a.value, b.value).Simplify();

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