import sys, re;

from Value import *;
from Functions import *;

class Token:
	def __init__(self, type, data):
		self.type = type;
		self.data = data;

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

		# parentheses are important!
		if self.string[:1] == '(':
			self.string = self.string[1:];
			return Token("leftparen", None);
		if self.string[:1] == ')':
			self.string = self.string[1:];
			return Token("rightparen", None);

		# infix functions
		if self.string[:2] == '=>':
			self.string = self.string[2:];
			return Token("infix", fun_convert);
		if self.string[:1] == '+':
			self.string = self.string[1:];
			return Token("infix", fun_add);
		if self.string[:1] == '-':
			self.string = self.string[1:];
			return Token("infix", fun_sub);
		if self.string[:1] == '*':
			self.string = self.string[1:];
			return Token("infix", fun_mult);
		if self.string[:1] == '/':
			self.string = self.string[1:];
			return Token("infix", fun_div);
		if self.string[:1] == '^':
			self.string = self.string[1:];
			return Token("infix", fun_pow);
		if self.string[:1] == '&':
			self.string = self.string[1:];
			return Token("infix", fun_and);
		if self.string[:1] == '|':
			self.string = self.string[1:];
			return Token("infix", fun_or);
		if self.string[:1] == '=':
			self.string = self.string[1:];
			return Token("infix", fun_equals);
		if self.string[:1] == '>':
			self.string = self.string[1:];
			return Token("infix", fun_greater);

		raise SyntaxError("Unknown token, starting at: '" + self.string + "'");

	def next(self):
		if len(self.buffer) > 0:
			return self.buffer.pop();
		return self.tokenFromString();

def parseInfixPart(tokenSrc, val):
	try:
		next = tokenSrc.next();
	except StopIteration:
		return val;

	if next.type == "infix":
		val2 = parseExpression(tokenSrc);
		return next.data(val, val2);
	else:
		tokenSrc.put(next);
		return val;

def parseExpression(tokenSrc):
	try:
		token = tokenSrc.next();
	except StopIteration:
		raise SyntaxError("Expected expression, received end of line.");

	if token.type == "value" or token.type == "type":
		return parseInfixPart(tokenSrc, token.data);

	if token.type == "leftparen":
		exp = parseExpression(tokenSrc);
		next = tokenSrc.next();
		if next.type != "rightparen":
			raise SyntaxError("Expected right parenthesis, received " + str(next));
		else:
			# check if it's not part of another (infix) expression
			return parseInfixPart(tokenSrc, exp);
	
	raise SyntaxError("Expected expression, received: " + str(token));

# the first step in evaluating a command, sets up things so that they can get parsed
def evaluate(command):
	tokens = TokenIterator(command);
	return  parseExpression(tokens);

# startup screen, do loading before this
print("OctopusCalc loaded");

# main loop
while 1:
	# read a statement
	command = input("> ");

	# exit if the command is empty
	if command == "exit" or command == "":
		break;

	# try to evaluate the command
	try:
		result = evaluate(command);
	#except (SyntaxError, NameError):
	#	print ("Error: invalid command:", command);
	#except ValueError:
	#	print ("Error: invalid number:", command);
	except:
	#	print ("Error: unknown error of type:", sys.exc_info()[0]);
		raise
	else:
		print (result);

# offload everything after this
print ("Exiting...");