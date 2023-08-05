import numpy as np

from hyperopt import hp

from hpogrid.search_space.base_space import BaseSpace

class HyperOptSpace(BaseSpace):
	def __init__(self, search_space = None):
		self.library = 'hyperopt'
		super().__init__(search_space)	
		

	def reset_space(self):
		self.search_space = {}
		
	def append(self, space_value):
		self.search_space[space_value[0]] = space_value[1]

	def categorical(self, label, categories, grid_search = False):
		if grid_search != False:
			raise ValueError('{} does not allow grid search'.format(self.library))
		return (label, hp.choice(label, categories))

	def uniformint(self, label, low, high):
		return (label, hp.uniformint(label, low, high))

	def uniform(self, label, low, high):
		return (label, hp.uniform(label, low, high))

	def quniform(self, label, low, high, q):
		return (label, hp.uniform(label, low, high, q))

	def loguniform(self, label, low, high, base = np.e):
		if base != np.e:
			raise ValueError('{} search space only allows base e for loguniform sampling'.format(self.library))
		return (label, hp.loguniform(label, np.log(low), np.log(high)))

	def qloguniform(self, label, low, high, q, base = np.e):
		if base != np.e:
			raise ValueError('{} search space only allows base e for qloguniform sampling'.format(self.library))
		return (label, hp.qloguniform(label, np.log(low), np.log(high)), q)

	def normal(self, label, mu, sigma):
		return (label, hp.normal(label, mu, sigma))

	def qnormal(self, label, mu, sigma, q):
		return (label, hp.normal(label, mu, sigma, q))

	def lognormal(self, label, mu, sigma, base):
		if base != np.e:
			raise ValueError('{} search_space only allows base e for lognormal sampling'.format(self.library))
		return (label, hp.lognormal(label, mu, sigma))

	def qlognormal(self, label, mu, sigma, q, base = np.e):
		if base != np.e:
			raise ValueError('{} search_space only allows base e for qlognormal sampling'.format(self.library))
		return (label, hp.qlognormal(label, mu, sigma, q))

	def fixed(self, value):
		return (label, value)
