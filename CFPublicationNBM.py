from AFPublication import AFPublication
import random
import copy
from NewPublicationFactory import NewPublicationFactory

class CFPublicationNBM(AFPublication):

	def __init__(self, node, neighbors, dataset, af_post_database, prob_post = 1, prob_mal = 0, prob_share = 0):
		super().__init__(node, neighbors, dataset, af_post_database, prob_post, prob_mal, prob_share)
	
	
	def get_new_publication(self):
		index = None
		random_value = random.random()
		if random_value <= self._prob_mal:
			index = self._new_pub_factory.get_index_new_publ(True)
		else:
			index = self._new_pub_factory.get_index_new_publ(False)
		return index
