import random
import copy
from CFPublicationNBM import CFPublicationNBM
from NewPublicationFactory import NewPublicationFactory

class CFPublicationNM(CFPublicationNBM):

	def __init__(self, node, neighbors, dataset, af_post_database, prob_post = 1, prob_mal = 0, prob_share = 0):
		super().__init__(node, neighbors, dataset, af_post_database, prob_post, prob_mal, prob_share)
		categories_order = copy.deepcopy(dataset.get_categories())
		random.shuffle(categories_order)
		self._new_pub_factory = NewPublicationFactory(self._dataset, categories_order, self._prob_categories)

	
	
