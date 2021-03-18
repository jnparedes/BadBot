from AFPublication import AFPublication
from NewPublicationFactory import NewPublicationFactory
import random
import copy

class CFPublicationBM(AFPublication):

	def __init__(self, node, neighbors, dataset, af_post_database, af_publication, prob_post = 1, prob_mal = 0, prob_share = 0):
		super().__init__(node, neighbors, dataset, af_post_database, prob_post, prob_mal, prob_share)

		self._mate = af_publication
		self._neighbors = self._neighbors + self._mate.get_neighbors()
	
	
	def get_new_publication(self):
		pass

	def get_publication(self, time):
		result = self._mate.get_publication(time)
		return result		

		