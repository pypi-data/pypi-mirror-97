from typing import Union
import sys, types, inspect
from math import sqrt

# ERRORS:
class VectorError(Exception):
	__module__ = Exception.__module__
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
		self.__class__.__name__ = "VectorError"

class Vector:

	# FUNCTIONS
	def __init__(self, *argv):
		"""Check amount of args and set them"""
		if type(argv[0]) == tuple and len(argv) == 1 and len(argv[0]) > 0 and len(argv[0]) < 5:
			argv = tuple([var for var in argv[0]])

		if len(argv) < 1 or len(argv) > 4 or [True for var in argv if not(type(var) == int or type(var) == float)]:
			raise ValueError('Vector type only supports 1 to 4 integers and floats or tuple')

		self.attrlist = ['x', 'y', 'z', 't']

		for i in range(len(self.attrlist)):
			try:
				exec(f'self.{self.attrlist[i]} = {argv[i]}')
				exec(f'self.type = f"vector{i+1}"')
			except IndexError:
				exec(f'self.{self.attrlist[i]} = None')

	def __str__(self):
		returntuple = []
		if not self.x == None: returntuple.append(self.x)
		if not self.y == None: returntuple.append(self.y)
		if not self.z == None: returntuple.append(self.z)
		if not self.t == None: returntuple.append(self.t)
		return str(tuple(returntuple))

	def __len__(self):
		if self.type == 'vector1': return 1
		if self.type == 'vector2': return 2
		if self.type == 'vector3': return 3
		if self.type == 'vector4': return 4

	def __getitem__(self, index):
		if (index < 0 or index > len(self) - 1):
			raise IndexError(f"'{index}' is an invalid index for type '{self.type}'")
		if (not type(index) == int):
			raise IndexError(f"vector indexing does not support type '{type(index).__name__}'")
		else:
			if index == 0: return self.x
			if index == 1: return self.y
			if index == 2: return self.z
			if index == 3: return self.t

	def __setitem__(self, index, value):
		if (index < 0 or index > len(self) - 1):
			raise IndexError(f"'{index}' is an invalid index for type '{self.type}'")
		if (not type(index) == int):
			raise IndexError(f"vector indexing does not support type '{type(index).__name__}'")
		else:
			if index == 0: self.x = value
			if index == 1: self.y = value
			if index == 2: self.z = value
			if index == 3: self.t = value

	def __repr__(self):
		if len(self) > 0: result = f"Vector({self.x})"
		if len(self) > 1: result = f"Vector({self.x}, {self.y})"
		if len(self) > 2: result = f"Vector({self.x}, {self.y}, {self.z})"
		if len(self) > 3: result = f"Vector({self.x}, {self.y}, {self.z}, {self.t})"
		return result

	def mag(self):
		summ = 0
		for i in range(len(self)):
		    summ = self[i]*self[i] + summ    
		return pow(summ,0.5)
	def magnitude(self):
		return self.mag()
		#

	def normalized(self):
		mag = self.mag()
		if len(self) == 1:
			return Vector(1)
		if len(self) == 2:
			return Vector(self.x/mag, self.y/mag)
		if len(self) == 3:
			return Vector(self.x/mag, self.y/mag, self.z/mag)
		if len(self) == 4:
			return Vector(self.x/mag, self.y/mag, self.z/mag, self.t/mag)
		else:
			raise VectorError(f'an error occured during the normalization of {self.type}')
	def norm(self):
		return self.normalized()
		#		

	def positive(self):
		if len(self) == 1:
			return Vector(sqrt(self.x**2))
		if len(self) == 2:
			return Vector(sqrt(self.x**2), sqrt(self.y**2))
		if len(self) == 3:
			return Vector(sqrt(self.x**2), sqrt(self.y**2), sqrt(self.z**2))
		if len(self) == 4:
			return Vector(sqrt(self.x**2), sqrt(self.y**2), sqrt(self.z**2), sqrt(self.t**2))
		else:
			raise VectorError(f'an error occured during the positive of {self.type}')
			
	# BINARY OPERATORS
	def __add__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x + other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y + other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z + other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t + other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x + other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y + other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z + other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t + other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x + other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y + other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z + other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t + other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x + other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y + other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z + other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t + other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot add type '{type(other).__name__}' to type '{self.type}'")			

	def __sub__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x - other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y - other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z - other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t - other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x - other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y - other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z - other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t - other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x - other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y - other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z - other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t - other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x - other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y - other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z - other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t - other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot subtract type '{type(other).__name__}' from type '{self.type}'")			

	def __mul__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x * other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y * other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z * other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t * other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x * other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y * other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z * other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t * other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x * other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y * other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z * other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t * other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x * other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y * other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z * other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t * other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot multiply type '{self.type}' with type '{type(other).__name__}'")

	def __truediv__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x / other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y / other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z / other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t / other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x / other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y / other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z / other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t / other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x / other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y / other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z / other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t / other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x / other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y / other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z / other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t / other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot divide type '{self.type}' by type '{type(other).__name__}'")

	def __floordiv__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x // other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y // other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z // other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t // other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x // other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y // other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z // other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t // other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x // other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y // other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z // other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t // other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x // other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y // other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z // other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t // other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot divide type '{self.type}' by type '{type(other).__name__}'")

	def __mod__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x % other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y % other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z % other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t % other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x % other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y % other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z % other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t % other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x % other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y % other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z % other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t % other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x % other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y % other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z % other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t % other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot mod type '{self.type}' by type '{type(other).__name__}'")

	def __pow__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				returntuple = []
				if len(self) > 0:
					newx = self.x ** other.x
					returntuple.append(newx)
				if len(self) > 1:
					newy = self.y ** other.y
					returntuple.append(newy)
				if len(self) > 2:
					newz = self.z ** other.z
					returntuple.append(newz)
				if len(self) > 3:
					newt = self.t ** other.t
					returntuple.append(newt)
				return tuple(returntuple)

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			returntuple = []
			if len(self) > 0:
				newx = self.x ** other[0]
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y ** other[1]
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z ** other[2]
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t ** other[3]
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == int:
			returntuple = []
			if len(self) > 0:
				newx = self.x ** other
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y ** other
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z ** other
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t ** other
				returntuple.append(newt)
			return tuple(returntuple)

		elif type(other) == float:
			lenstr = len(str(other).split(".")[1])

			returntuple = []
			if len(self) > 0:
				newx = round(self.x ** other, lenstr)
				returntuple.append(newx)
			if len(self) > 1:
				newy = round(self.y ** other, lenstr)
				returntuple.append(newy)
			if len(self) > 2:
				newz = round(self.z ** other, lenstr)
				returntuple.append(newz)
			if len(self) > 3:
				newt = round(self.t ** other, lenstr)
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot raise type '{self.type}' to type '{type(other).__name__}'")

	# ASSIGNMENT OPERATORS
	def __iadd__(self, other):
		result = self.__add__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __isub__(self, other):
		result = self.__sub__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __imul__(self, other):
		result = self.__mul__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __idiv__(self, other):
		result = self.__truediv__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __ifloordiv__(self, other):
		result = self.__floordiv__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __imod__(self, other):
		result = self.__mod__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	def __ipow__(self, other):
		result = self.__pow__(other)
		
		for i in range(len(result)):
			exec(f"self.{self.attrlist[i]} = {result[i]}")
		return self

	# COMPARISON OPERATORS
	def __lt__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					self_av = self.x
					other_av = other.x
				if len(self) > 1:
					self_av += self.y
					other_av += other.y
				if len(self) > 2:
					self_av += self.z
					other_av += other.z
				if len(self) > 3:
					self_av += self.t
					other_av += other.t

				self_av = self_av / len(self)
				other_av = other_av / len(other)
				return self_av < other_av

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				self_av = self.x
				other_av = other[0]
			if len(self) > 1:
				self_av += self.y
				other_av += other[1]
			if len(self) > 2:
				self_av += self.z
				other_av += other[2]
			if len(self) > 3:
				self_av += self.t
				other_av += other[3]
				
			self_av = self_av / len(self)
			other_av = other_av / len(other)
			return self_av < other_av

		elif type(other) == int:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av < other_av

		elif type(other) == float:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av < other_av

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	def __gt__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					self_av = self.x
					other_av = other.x
				if len(self) > 1:
					self_av += self.y
					other_av += other.y
				if len(self) > 2:
					self_av += self.z
					other_av += other.z
				if len(self) > 3:
					self_av += self.t
					other_av += other.t

				self_av = self_av / len(self)
				other_av = other_av / len(other)
				return self_av > other_av

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				self_av = self.x
				other_av = other[0]
			if len(self) > 1:
				self_av += self.y
				other_av += other[1]
			if len(self) > 2:
				self_av += self.z
				other_av += other[2]
			if len(self) > 3:
				self_av += self.t
				other_av += other[3]
				
			self_av = self_av / len(self)
			other_av = other_av / len(other)
			return self_av > other_av

		elif type(other) == int:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av > other_av

		elif type(other) == float:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av > other_av

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	def __le__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					self_av = self.x
					other_av = other.x
				if len(self) > 1:
					self_av += self.y
					other_av += other.y
				if len(self) > 2:
					self_av += self.z
					other_av += other.z
				if len(self) > 3:
					self_av += self.t
					other_av += other.t

				self_av = self_av / len(self)
				other_av = other_av / len(other)
				return self_av <= other_av

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				self_av = self.x
				other_av = other[0]
			if len(self) > 1:
				self_av += self.y
				other_av += other[1]
			if len(self) > 2:
				self_av += self.z
				other_av += other[2]
			if len(self) > 3:
				self_av += self.t
				other_av += other[3]
				
			self_av = self_av / len(self)
			other_av = other_av / len(other)
			return self_av <= other_av

		elif type(other) == int:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av <= other_av

		elif type(other) == float:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av <= other_av

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	def __ge__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					self_av = self.x
					other_av = other.x
				if len(self) > 1:
					self_av += self.y
					other_av += other.y
				if len(self) > 2:
					self_av += self.z
					other_av += other.z
				if len(self) > 3:
					self_av += self.t
					other_av += other.t

				self_av = self_av / len(self)
				other_av = other_av / len(other)
				return self_av >= other_av

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				self_av = self.x
				other_av = other[0]
			if len(self) > 1:
				self_av += self.y
				other_av += other[1]
			if len(self) > 2:
				self_av += self.z
				other_av += other[2]
			if len(self) > 3:
				self_av += self.t
				other_av += other[3]
				
			self_av = self_av / len(self)
			other_av = other_av / len(other)
			return self_av >= other_av

		elif type(other) == int:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av >= other_av

		elif type(other) == float:
			if len(self) > 0:
				self_av = self.x
				other_av = other
			if len(self) > 1:
				self_av += self.y
				other_av += other
			if len(self) > 2:
				self_av += self.z
				other_av += other
			if len(self) > 3:
				self_av += self.t
				other_av += other
				
			self_av = self_av / len(self)
			other_av = other_av / len(self)
			return self_av >= other_av

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	def __eq__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					if not self.x == other.x:
						return False
				if len(self) > 1:
					if not self.y == other.y:
						return False
				if len(self) > 2:
					if not self.z == other.z:
						return False
				if len(self) > 3:
					if not self.t == other.t:
						return False
				return True

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				if not self.x == other[0]:
					return False
			if len(self) > 1:
				if not self.y == other[1]:
					return False
			if len(self) > 2:
				if not self.z == other[2]:
					return False
			if len(self) > 3:
				if not self.t == other[3]:
					return False
			return True

		elif type(other) == int or type(other) == float:
			if len(self) > 0:
				if not self.x == other:
					return False
			if len(self) > 1:
				if not self.y == other:
					return False
			if len(self) > 2:
				if not self.z == other:
					return False
			if len(self) > 3:
				if not self.t == other:
					return False
			return True

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	def __ne__(self, other):
		if isinstance(other, Vector):
			if not self.type == other.type:
				raise VectorError(f"Vector types '{self.type}' and '{other.type}' do not match")
			else:
				if len(self) > 0:
					if self.x == other.x:
						return False
				if len(self) > 1:
					if self.y == other.y:
						return False
				if len(self) > 2:
					if self.z == other.z:
						return False
				if len(self) > 3:
					if self.t == other.t:
						return False
				return True

		elif (type(other) == tuple or type(other) == list) and len(other) == len(self):
			if len(self) > 0:
				if self.x == other[0]:
					return False
			if len(self) > 1:
				if self.y == other[1]:
					return False
			if len(self) > 2:
				if self.z == other[2]:
					return False
			if len(self) > 3:
				if self.t == other[3]:
					return False
			return True

		elif type(other) == int or type(other) == float:
			if len(self) > 0:
				if self.x == other:
					return False
			if len(self) > 1:
				if self.y == other:
					return False
			if len(self) > 2:
				if self.z == other:
					return False
			if len(self) > 3:
				if self.t == other:
					return False
			return True

		else:
			raise VectorError(f"Cannot compare type '{self.type}' to type '{type(other).__name__}'")

	# UNARY OPERATORS
	def __neg__(self):
		if isinstance(self, Vector):

			returntuple = []
			if len(self) > 0:
				newx = self.x * -1
				returntuple.append(newx)
			if len(self) > 1:
				newy = self.y * -1
				returntuple.append(newy)
			if len(self) > 2:
				newz = self.z * -1
				returntuple.append(newz)
			if len(self) > 3:
				newt = self.t * -1
				returntuple.append(newt)
			return tuple(returntuple)

		else:
			raise VectorError(f"Cannot negate type '{self.type}'")

	def __pos__(self):
		return self
		# does nothing yet

def vtype(given):
	if isinstance(given, Vector):
		return given.type
	else:
		return type(given).__name__
vectortype = vtype

def unvector(self):
	if not isinstance(self, Vector):
		raise VectorError(f"cannot unvector type '{type(self).__name__}'")
	if len(self) > 0: result = (self.x)
	if len(self) > 1: result = (self.x, self.y)
	if len(self) > 2: result = (self.x, self.y, self.z)
	if len(self) > 3: result = (self.x, self.y, self.z, self.t)
	return result
unv = unvector

def magnitude(self):
	if not isinstance(self, Vector):
		raise VectorError(f"cannot find magnitude of type '{type(self).__name__}'")
	return self.mag()
mag = magnitude

def normalized(self):
	if not isinstance(self, Vector):
		raise VectorError(f"cannot normalize type '{type(self).__name__}'")
	return self.normalized()
norm = normalized

def positive(self):
	if not isinstance(self, Vector):
		raise VectorError(f"cannot make type '{type(self).__name__}' positive")
	return self.positive()