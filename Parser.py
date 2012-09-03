import re;

from Functions import *;
from Value import *;

## {{{ http://code.activestate.com/recipes/52549/ (r3)
class curry:
    def __init__(self, fun, *args, **kwargs):
        self.fun = fun
        self.pending = args[:]
        self.kwargs = kwargs.copy()

    def __call__(self, *args, **kwargs):
        if kwargs and self.kwargs:
            kw = self.kwargs.copy()
            kw.update(kwargs)
        else:
            kw = kwargs or self.kwargs

        return self.fun(*(self.pending + args), **kw)
## end of http://code.activestate.com/recipes/52549/ }}}

class Token:
	def __init__(self, type, data):
		self.type = type;
		self.data = data;
		
	def __repr__(self):
		return self.__str__();

	def __str__(self):
		return "{Token type: " + str(self.type) + " data: " + str(self.data) + "}"

class TokenIterator:
	def __init__(self, string):
		self.string = string;
		self.buffer = [];

	def __iter__(self):
		return self;

	def peek(self):
		next = self.tokenFromString();
		self.buffer.append(next);
		return next;

	def put(self, token):
		self.buffer.append(token);

	def empty(self):
		if len(self.buffer) > 0:
			return false;
		# skip over whitespace
		match = re.match("^(\s*)(.*)$", self.string);
		self.string = match.group(2);
		return len(self.string) == 0;

	def tokenFromString(self):
		# skip over whitespace
		match = re.match("^(\s*)(.*)$", self.string);
		self.string = match.group(2);
		if len(self.string) == 0:
			raise StopIteration;

		# Typenames are very important
		if self.string[:7] == "Boolean":
			self.string = self.string[7:];
			return Token("type", Boolean);
		if self.string[:7] == "Integer":
			self.string = self.string[7:];
			return Token("type", Integer);
		if self.string[:8] == "Fraction":
			self.string = self.string[8:];
			return Token("type", Fraction);
		if self.string[:7] == "Decimal":
			self.string = self.string[7:];
			return Token("type", Decimal);
		if self.string[:4] == "Text":
			self.string = self.string[4:];
			return Token("type", Text);
		if self.string[:6] == "Object":
			self.string = self.string[6:];
			return Token("type", Object);
		if self.string[:4] == "Unit":
			self.string = self.string[4:];
			return Token("type", Unit);
		if self.string[:8] == "Quantity":
			self.string = self.string[8:];
			return Token("type", Quantity);
			
		# literal characters
		if self.string[:1] == '(':
			self.string = self.string[1:];
			return Token("leftparen", None);
		if self.string[:1] == ')':
			self.string = self.string[1:];
			return Token("rightparen", None);
		if self.string[:1] == ',':
			self.string = self.string[1:];
			return Token("comma", None);
		if self.string[:1] == '[':
			self.string = self.string[1:];
			return Token("leftbracket", None);
		if self.string[:1] == ']':
			self.string = self.string[1:];
			return Token("rightbracket", None);
		
		# infix functions
		if self.string[:2] == '=>':
			self.string = self.string[2:];
			return Token("infix", (fun_convert, 6));
		if self.string[:1] == '^':
			self.string = self.string[1:];
			return Token("infix", (fun_pow, 5));
		if self.string[:1] == '*':
			self.string = self.string[1:];
			return Token("infix", (fun_mult, 4));
		if self.string[:1] == '/':
			self.string = self.string[1:];
			return Token("infix", (fun_div, 4));
		if self.string[:1] == '%':
			self.string = self.string[1:];
			return Token("infix", (fun_mod, 4));
		if self.string[:1] == '+':
			self.string = self.string[1:];
			return Token("infix", (fun_add, 3));
		if self.string[:1] == '-':
			self.string = self.string[1:];
			return Token("infix", (fun_sub, 3));
		if self.string[:1] == '&':
			self.string = self.string[1:];
			return Token("infix", (fun_and, 2));
		if self.string[:1] == '|':
			self.string = self.string[1:];
			return Token("infix", (fun_or, 2));
		if self.string[:1] == '=':
			self.string = self.string[1:];
			return Token("infix", (fun_equals, 1));
		if self.string[:1] == '>':
			self.string = self.string[1:];
			return Token("infix", (fun_greater, 1));
		if self.string[:1] == 'and':
			self.string = self.string[1:];
			return Token("infix", (fun_and, 0));
		if self.string[:1] == 'or':
			self.string = self.string[1:];
			return Token("infix", (fun_or, 0));

		# predefined functions
		if self.string[:3] == 'gcd':
			self.string = self.string[3:];
			return Token("function", fun_gcd);
				
		# Text
		match = re.match("^\"(.*?)\"(.*)$", self.string);
		if match != None:
			self.string = match.group(2);
			return Text(match.group(1));
		
		match = re.match("^'(.*?)'(.*)$", self.string);
		if match != None:
			self.string = match.group(2);
			return Text(match.group(1));

		# Boolean: either 'false' or 'true'
		if re.match("^(false)", self.string, re.I) != None:
			self.string = self.string[5:];
			return Token("value", Boolean(False));
		if re.match("^(true)", self.string, re.I) != None:
			self.string = self.string[4:];
			return Token("value", Boolean(True));

		# Decimal: either a'.'b , a'e'c or a'.'b'e'c where a, b and c are a series of digits
		match = re.match("^(\d+)\.(\d+)e(\d+)", self.string, re.I);
		if match != None:
			self.string = self.string[match.end(3):];
			value = int(match.group(1) + match.group(2));
			power = int(match.group(3)) - len(match.group(2));
			return Token("value", Decimal(value, power));
		match = re.match("^(\d+)e(\d+)", self.string, re.I);
		if match != None:
			self.string = self.string[match.end(2):];
			value = int(match.group(1));
			power = int(match.group(2));
			return Token("value", Decimal(value, power));
		match = re.match("^(\d+)\.(\d+)", self.string);
		if match != None:
			self.string = self.string[match.end(2):];
			value = int(match.group(1) + match.group(2));
			power = -len(match.group(2));
			return Token("value", Decimal(value, power));

		# Fractions are handled as an expression

		# Integer: a series of digits
		match = re.match("^(\d+)", self.string);
		if match != None:
			self.string = self.string[match.end(1):];
			return Token("value", Integer(match.group(1)));
		
		# try to make every alpha-numeric character into an Object or Unit
		match = re.match("^(\w+)", self.string);
		if match != None:
			self.string = self.string[match.end(1):];
			
			value = match.group(1);
			if value in objects:
				return Token("value", objects[value]);
			if value in units:
				return Token("value", units[value]);
			
			return Token("name", value);
		
		raise SyntaxError("Unknown token, starting at: '" + self.string + "'");

	def next(self):
		if len(self.buffer) > 0:
			return self.buffer.pop();
		return self.tokenFromString();

def parseFunction(tokenList, func):
	# go up to first comma (since other functions should have been stripped out by now)
	for location, value in enumerate(tokenList):
		if type(value) == Token and value.type == "comma":
			arg = parseExpressionList(tokenList[:location]);
			return parseFunction(tokenList[location + 1:], curry(func, arg));
	
	# if there are no commas, the rest of the expression must be our arguments
	arg = parseExpressionList(tokenList);
	return func(arg);
	
def getValue(token):
	if issubclass(type(token), Value):
		return token;
	else:
		if type(token) != Token or (token.type != "value" and token.type != "type"):
			raise SyntaxError("Unexpected " + str(token));
		else:
			return token.data;
			
def parseExpressionList(tokenList):
	#for value in tokenList:
		#print(str(value));

	# if the list is only one value, return that
	if len(tokenList) <= 0:
		return None;
	if len(tokenList) == 1:
		return getValue(tokenList[0]);
	
	# reduce parentheses to their contents' value
	parenLevel = 0
	for location, value in enumerate(tokenList):
		if type(value) == Token and value.type == "leftparen":
			for endPos, token in enumerate(tokenList[location+1:]):
				if type(token) == Token and token.type == "leftparen":
					parenLevel = parenLevel + 1;
				if type(token) == Token and token.type == "rightparen":
					if parenLevel > 0:
						parenLevel = parenLevel - 1;
					else:
						value = parseExpressionList(tokenList[location + 1 : location + endPos + 1]);
						# replace the value into tokenList
						tokenList[location : location + endPos + 2] = [value];
						# parse the resulting list
						return parseExpressionList(tokenList);

			raise SyntaxError("Unmatched parentheses, you are missing a ')' somewhere.");
	
	# reduce quantities to their values
	for location, value in enumerate(tokenList):
		if location > 0:
			if type(value) == Unit:
				try:
					value = Quantity(getValue(tokenList[location - 1]), value);
					tokenList[location - 1:location + 1] = [value];
					return parseExpressionList(tokenList);
				except SyntaxError:
					pass;
			elif type(value) == Token and value.type == "value" and type(value.data) == Unit:
				try:
					value = Quantity(getValue(tokenList[location - 1]), value.data);
					tokenList[location - 1:location + 1] = [value];
					return parseExpressionList(tokenList);
				except SyntaxError:
					pass;

	# reduce functions to their values
	for location, value in enumerate(tokenList):
		if type(value) == Token and value.type == "function":
			# since functions go up to the end of the expression, we should've reached the end,
			# therefore we can safely ignore everything after this function
			value = parseFunction(tokenList[location + 1:], value.data);
			# replace into tokenList
			tokenList[location:] = [value];
			return parseExpressionList(tokenList);
	
	# reduce objects to their properties
	parenLevel = 0
	for location, value in enumerate(tokenList):
		if type(value) == Token and value.type == "leftbracket":
			object = tokenList[location + 1];
			property = tokenList[location + 2];
			if type(tokenList[location + 3]) != Token or tokenList[location + 3].type != "rightbracket":
				raise SyntaxError("Unmatched brackets, you are missing a ']' somewhere.");
			if type(object) == Token:
				if object.type == "name" and object.data in objects:
					object = objects[object.data];
				if object.type == "value":
					object = object.data;

			if type(property) == Token:
				if property.type == "name":
					property = property.data;
			
			value = object.getAttr(property);
			# replace the value into tokenList
			tokenList[location : location + 4] = [value];
			return parseExpressionList(tokenList);
			
	# reduce infix operators to their values
	maxPrecedence = -1;
	opPos = 0;
	opFunc = (lambda x, y: x);
	for location, value in enumerate(tokenList):
		if type(value) == Token and value.type == "infix":
			if value.data[1] > maxPrecedence:
				maxPrecedence = value.data[1];
				opPos = location;
				opFunc = value.data[0];
	if maxPrecedence > -1:
		left = parseExpressionList([tokenList[opPos - 1]]);
		right = parseExpressionList([tokenList[opPos + 1]])
		value = opFunc(left, right);
		# replace the value into tokenList
		tokenList[opPos - 1 : opPos + 2] = [value];
		return parseExpressionList(tokenList);
	
	raise SyntaxError("No idea what to do with these values: " + str(tokenList));

def parseExpression(tokenSrc, canBeNull = False):
	valueList = [];
	
	# when multiple statements are in, parse up to the end of this statement:
	while not tokenSrc.empty():
		try:
			valueList.append(tokenSrc.next());
		except StopIteration:
			raise ValueError("Tokens expected but none received.");
			
	if len(valueList) <= 0:
		return None;
	else:
		return parseExpressionList(valueList);
	
