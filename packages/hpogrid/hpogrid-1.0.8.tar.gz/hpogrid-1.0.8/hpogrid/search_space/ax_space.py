import ax

from hpogrid.search_space.base_space import BaseSpace

class AxSpace(BaseSpace):

	def __init__(self, search_space = None):
		self.library = 'ax'
		super().__init__(search_space)	
		

	def reset_space(self):
		self.search_space = []

	def append(self, space_value):
		self.search_space.append(space_value)
	
	def _range(self, name, bounds, value_type = "bounds", log_scale = False):
		space_value = {
			"name": name,
			"type": "range",
			"bounds": bounds,
			"value_type": value_type,
			"log_scale": log_scale
		}
		return space_value


	def categorical(self, label, categories, grid_search = False):
		space_value = {
			"name": label,
			"type": "choice",
			"values": categories
		}
		return space_value

	def uniform(self, label, low, high):
		return self._range(label, [low, high], "float")

	def uniformint(self, label, low, high):
		return self._range(label, [low, high], "int")

	def loguniform(self, label, low, high, base = 10):
		if base != 10:
			raise ValueError('{} search space only allows base 10 for loguniform sampling'.format(self.library))
		return self._range(label, [low, high], "float", log_scale=True)

	def qloguniform(self, label, low, high, q = 1):
		if q != 1:
			raise ValueError('{} search space only allows q = 1 for qloguniform sampling'.format(self.library))
		return self._range(label, [low, high], "int", log_scale=True)


	def fixed(name, label, value):
		space_value = {
			"name": label,
			"value": value
		}
		return space_value