import random
class NewPublicationFactory:

	def __init__(self, dataset = None, categories_order = None, prob_categories = None):
		self._dataset = dataset
		self._categories_order = categories_order
		self._prob_categories = prob_categories
		self._history = []

	def set_dataset(self, dataset):
		self._dataset = dataset

	def get_index_new_publ(self, label):
		acum_prob = 0
		category = None
		random_value = random.random()

		if (not label is None):
			probabilities = self._prob_categories[label]
			for index in range(len(probabilities)):
				acum_prob += probabilities[index]
				if random_value <= acum_prob:
					category = self._categories_order[index]
					break
		
			data_id = self._dataset.get_id_data(label, category)

		self._history.append(data_id)

		return data_id

	def set_categories_order(self, categories_order):
		self._categories_order = categories_order

	def set_prob_categories(self, prob_categories):
		self._prob_categories = prob_categories
