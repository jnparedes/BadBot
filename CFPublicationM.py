import random
import copy
from CFPublicationNBM import CFPublicationNBM
from NewPublicationFactory import NewPublicationFactory

class CFPublicationM(CFPublicationNBM):

	def __init__(self, node, neighbors, dataset, af_post_database, prob_post = 1, prob_mal = 0, prob_share = 0):
		super().__init__(node, neighbors, dataset, af_post_database, prob_post, prob_mal, prob_share)
		aux_categories_order = copy.deepcopy(self._dataset.get_categories())[1:]
		categories_order = copy.deepcopy(self._dataset.get_categories())[:1]
		random.shuffle(aux_categories_order)
		categories_order = categories_order + aux_categories_order
		self._prob_categories[False] = []
		for category in categories_order:
			self._prob_categories[False].append(1 / len(categories_order))

		self._new_pub_factory = NewPublicationFactory(self._dataset, categories_order, self._prob_categories)
	
