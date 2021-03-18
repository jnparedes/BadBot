from abc import ABC, abstractmethod
import random
import copy
from NewPublicationFactory import NewPublicationFactory

class AFPublication(ABC):

	def __init__(self, node, neighbors, dataset, af_post_database = None, prob_post = 1, prob_mal = 0, prob_share = 0):
		self._dataset = dataset
		self._node = node
		self._neighbors = neighbors
		self._time = -1
		self._prob_post = prob_post
		self._prob_mal = prob_mal
		self._prob_share = prob_share
		self._history_publications = []
		self._af_post_database = af_post_database
		categories_order = copy.deepcopy(dataset.get_categories())
		max_weight = len(categories_order)
		total_weight = 0
		for w in range(1, max_weight + 1):
			total_weight += w

		self._prob_categories = {True: [], False: []}
		index = 0
		for category in categories_order:
			self._prob_categories[True].append((max_weight - index) / total_weight)
			self._prob_categories[False].append((max_weight - index) / total_weight)
			index += 1
		self._new_pub_factory = NewPublicationFactory(self._dataset, categories_order, self._prob_categories)
		


	@abstractmethod
	def get_new_publication(self):
		pass
	
	def get_publication(self, time):
		post_index = None
		if (self._time < time):
			while (self._time < time):
				self._time += 1
				random_value = random.random()
				if random_value < self._prob_post:
					post_index = self.get_new_publication()
				elif((random_value <= (self._prob_post + self._prob_share)) and (len(self._neighbors) > 0)):
					post_index = self.get_publication_neigh(self._time)

				self._history_publications.append(post_index)
		else:
			post_index = self._history_publications[time]

		return post_index

	def get_node(self):
		return self._node

	def get_neighbors(self):
		return self._neighbors

	
	def get_dominant_category(self, time):
		result = None
		category_kinds = self._dataset.get_categories()
		counter = [0] * len(category_kinds)
		for t in range(time + 1):
			if t < len(self._history_publications):
				id_post = self._history_publications[t]
				if not (id_post is None):
					for x in range(len(category_kinds)):
						if self._dataset.get_category(id_post) == category_kinds[x]:
							counter[x] += 1
							break
			else:
				break	
		max_counter = max(counter)
		if max_counter > 0:
			result = category_kinds[counter.index(max_counter)]
		
		return result
	

	def get_old_publication(self, category, time):
		result = None
		if (time < len(self._history_publications)):
			id_post = self._history_publications[time]
			if not (id_post is None):
				if (self._dataset.get_category(id_post) == category):
					result = id_post
		return result

	def get_dominant_category_neigh(self, time):
		result = None
		category_kinds = self._dataset.get_categories()
		counter = [0] * len(category_kinds)
		for neigh in self._neighbors:
			#category = self._af_post_database.get_dominant_category(neigh, self._time)
			category = self._af_post_database.get_dominant_category(neigh, time)
			if not category is None:
				for x in range(len(category_kinds)):
					if category == category_kinds[x]:
						counter[x] += 1
						break

		max_counter = max(counter)
		if max_counter > 0:
			result = category_kinds[counter.index(max_counter)]

		return result


	def get_publication_neigh(self, time):
		result = None
		category = self.get_dominant_category_neigh(time)
		#times = list(range(self._time + 1))
		times = list(range(time))
		random.shuffle(times)
		random.shuffle(self._neighbors)
		if not category is None:
			for t in times:
				for neigh in self._neighbors:
					result = self._af_post_database.get_old_publication(neigh, category, t)
					if not result is None:
						break

		return result