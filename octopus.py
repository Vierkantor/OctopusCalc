import sys;

# the first step in evaluating a command
def evaluate(command):
	try:
		return eval(command);
	except:
		raise;

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
	except (SyntaxError, NameError):
		print ("Error: invalid command:", command);
	except ValueError:
		print ("Error: invalid number:", command);
	except:
		print ("Error: unknown error of type:", sys.exc_info()[0]);
	else:
		print (result);

# offload everything after this
print ("Exiting...");