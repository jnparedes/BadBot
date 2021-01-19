from abc import ABC,abstractmethod

class Dataset(ABC):

	def __init__(self, location):
		self._location = location
		self._load_data()

	@abstractmethod
	def _load_data(self):
		pass
	
	@abstractmethod
	def get_data(self):
		pass

	@abstractmethod
	def get_ground_truth(self):
		pass
	
	@abstractmethod
	def get_categories(self):
		pass

	@abstractmethod
	def get_category(self, id_post):
		pass