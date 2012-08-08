# generic value container
class Value:
	def __init__(self):
		pass

	def __str__(self):
		return "{GenericValue}";

	def Convert(self, otherValue):
		if not issubclass(otherValue, Value):
			raise ValueError("Cannot convert to non-value.");
		if otherValue == type(self):
			return self;
		else:
			raise ValueError("Cannot convert to that value.");

# null class - no value
class Nothing (Value):
	def __init__(self):
		Value.__init__(self);

	def __str__(self):
		return "{Nothing}";

# boolean - either true or false
class Boolean (Value):
	def __init__(self, value):
		Value.__init__(self);

		if type(value) == Boolean:
			self.value = value.value;
		elif issubclass(type(value), Value):
			self.value = value.Convert(Boolean).value;
		else:
			value = int(value);
			if value == 0 or value == False:
				self.value = False;
			else:
				self.value = True;

	def Convert(self, otherValue):
		if not issubclass(otherValue, Value):
			raise ValueError("Cannot convert to non-value.");

		if otherValue == Boolean:
			return self;
		elif otherValue == Integer:
			return Integer(self.value);
		else:
			raise ValueError("Cannot convert to that value.");

	def __str__(self):
		return "{Boolean value: " + str(self.value) + "}";

# integer - any whole number
class Integer (Value):
	def __init__(self, value):
		Value.__init__(self);

		if type(value) == Integer:
			self.value = value.value;
		elif issubclass(type(value), Value):
			self.value = value.Convert(Integer).value;
		else:
			self.value = int(value);

	# convert to another Value
	def Convert(self, otherValue):
		if not issubclass(otherValue, Value):
			raise ValueError("Cannot convert to non-value.");

		if otherValue == Integer:
			return self;
		elif otherValue == Boolean:
			return Boolean(self.value);
		elif otherValue == Fraction:
			return Fraction(self.value, 1);
		else:
			raise ValueError("Cannot convert to that value.");

	def __str__(self):
		return "{Integer value: " + str(self.value) + "}";

# fraction - any two integers divided
class Fraction (Value):
	def __init__(self, top, bottom):
		Value.__init__(self);
		
		# copy the top and bottom arguments, the Integers will sort it out
		self.top = Integer(top);
		self.bottom = Integer(bottom);

	def Convert(self, otherValue):
		if not issubclass(otherValue, Value):
			raise ValueError("Cannot convert to non-value.");
		if otherValue == Fraction:
			return self;

		# Integer conversion is one step
		elif otherValue == Integer:
			return Integer(self.top / self.bottom);

		# Boolean conversion goes via Integer
		elif otherValue == Boolean:
			return self.Convert(Integer).convert(Boolean);
		else:
			raise ValueError("Cannot convert to that value.");

	def Simplify(self):
		if fun_equals(self.top, Integer(0)).value:
			return Integer(0);
		if fun_equals(self.bottom, Integer(1)).value:
			return Integer(self.top);
		if fun_equals(self.top, self.bottom).value:
			return Integer(1);
		gcd = fun_gcd(self.top, self.bottom);
		if fun_greater(gcd, Integer(1)):
			return Fraction(self.top.value / gcd.value, self.bottom.value / gcd.value);
		return self;

	def __str__(self):
		return "{Fraction top: " + str(self.top) + " bottom: " + str(self.bottom) + "}";

from Functions import *