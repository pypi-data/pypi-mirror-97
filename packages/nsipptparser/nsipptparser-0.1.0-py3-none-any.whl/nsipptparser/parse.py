from enum import Enum, auto

class LineType(Enum):
	OPEN  = auto() # Opening line that has children tags
	CLOSE = auto() # Closing line indicating the end of a parent
	LEAF  = auto() # Leaf line with data in the same line

class Data:
	def __init__(self, key, value, line_type):
		self.key = key
		self.value = value
		self.line_type = line_type

def insert_pair(dictionary, key, value):
	"""Allows insertion to dictionary even if key is already present
	If key is already present, updates dictionary's key to point to a list 
	of all the values for that key in the order in which they were added
	"""
	if key not in dictionary:
		dictionary[key] = value
	else:
		if isinstance(dictionary[key], list):
			dictionary[key].append(value)
		else:
			dictionary[key] = [dictionary[key], value]

def get_last_pair(dictionary, key):
	"""Throws exception if key not in dictionary"""
	if isinstance(dictionary[key], list):
		return dictionary[key][-1]
	return dictionary[key]

def parse_line(line):
	a, b = line.find('<'), line.find('>')
	if line[a+1] == '/':
		return Data(None, None, LineType.CLOSE)
	key = line[a+1:b]
	value = line[b+1:]
	if value == "":
		return Data(key, value, LineType.OPEN)
	else:
		return Data(key, value, LineType.LEAF)

def parse(file):
	"""Based on the algorithm by dchhetri
	https://codereview.stackexchange.com/a/58103
	"""
	parsed_json = {}
	parent_stack = [parsed_json]
	for line in file:
		line = line.rstrip('\n')
		data = parse_line(line)

		if data.line_type == LineType.LEAF:
			current_parent = parent_stack[-1]
			insert_pair(dictionary=current_parent, key=data.key, value=data.value)

		elif data.line_type == LineType.OPEN:
			current_parent = parent_stack[-1]
			insert_pair(current_parent, data.key, {})
			new_parent = get_last_pair(current_parent, data.key)
			parent_stack.append(new_parent)

		else: # LineType.CLOSE 
			parent_stack.pop(-1)

	return parsed_json
