import numpy as np

import ConfigSpace as CS
import ConfigSpace.hyperparameters as CSH


from hpogrid.search_space.base_space import BaseSpace

class BOHBSpace(BaseSpace):

	def __init__(self, search_space = None):
		self.library = 'bohb'
		super().__init__(search_space)	
		

	def reset_space(self):
		self.search_space = CS.ConfigurationSpace(seed=1)	

	def append(self, space_value):
		self.search_space.add_hyperparameter(space_value)

	def categorical(self, label, categories, grid_search = False):
		if grid_search != False:
			raise ValueError('{} does not allow grid search'.format(self.library))
		return CSH.CategoricalHyperparameter(name=label, choices=categories)

	def uniformint(self, label, low, high):
		return CSH.UniformIntegerHyperparameter(name=label, lower=low, upper=high)

	def uniform(self, label, low, high):
		return CSH.UniformFloatHyperparameter(name=label, lower=low, upper=high)

	def quniform(self, label, low, high, q):
		return CSH.UniformFloatHyperparameter(name=label, lower=low, upper=high, q=q)

	def qloguniform(self, label, low, high, q, base=np.e):
		if base != np.e:
			raise ValueError('{} only allows base e for qloguniform'.format(self.library))
		return CSH.UniformFloatHyperparameter(name=label, lower=low, upper=high, q=q, log=True)

	def loguniform(self, label, low, high, base=np.e):
		if base != np.e:
			raise ValueError('{} only allows base e for loguniform'.format(self.library))
		return CSH.UniformFloatHyperparameter(name=label, lower=low, upper=high, log=True)


	def normal(self, label, mu, sigma):
		return CSH.NormalFloatHyperparameter(name=label, mu=mu, sigma=sigma)

	def qnormal(self, label, mu, sigma, q):
		return CSH.NormalFloatHyperparameter(name=label, mu=mu, sigma=sigma, q=q)

	def qlognormal(self, label, mu, sigma, q, base=np.e):
		if base != np.e:
			raise ValueError('{} only allows base e for qlognormal'.format(self.library))
		return CSH.NormalFloatHyperparameter(name=label, mu=mu, sigma=sigma, q=q, log=True)

	def fixed(self, label, value):
		return self.CategoricalHyperparameter(name=label, choices=[value])
