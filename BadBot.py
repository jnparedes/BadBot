import os
from DatasetCSV import DatasetCSV
from CFPublicationM import CFPublicationM
from CFPublicationNM import CFPublicationNM
from CFPublicationBM import CFPublicationBM
from AFPublication import AFPublication
from CFPublicationNBM import CFPublicationNBM
import json
import csv
import random
import subprocess

class BadBot:

	def __init__(self, config_path):
		with open(config_path) as config_json:
			config_data = json.load(config_json)
		self._new_graph = config_data["new_graph"]
		self._t_sim = config_data["t_sim"]
		dataset_conf = config_data["dataset_csv"]
		if os.path.dirname(__file__) == '':
			loc = dataset_conf["location"] 
		else:
			loc = os.path.dirname(__file__) + '/' + dataset_conf["location"] 	
		
		id_ds = dataset_conf["id"]
		content = dataset_conf["content"]
		category = dataset_conf["category"]
		gt = dataset_conf["gt"]
		positive_labels = dataset_conf["positive_labels"]
		negative_labels = dataset_conf["negative_labels"]
		delimiter = dataset_conf["delimiter"]
		self._dataset = DatasetCSV(loc, id_ds, content, category, gt, positive_labels, negative_labels, delimiter)
		self._num_nodes = config_data["num_nodes"]
		self._num_edges = config_data["num_edges"]
		self._graph = None
		self._init_new_graph(self._num_nodes, self._num_edges)
		self._num_botnet = config_data["num_botnet"]
		self._prop_mal = config_data["prop_mal"]
		prob_b_post = float(config_data["prob_b_post"])
		prob_b_mal = float(config_data["prob_b_mal"])
		prob_b_share = float(config_data["prob_b_share"])
		self._social_botnets = []
		for x in range(self._num_botnet):
			self._social_botnets.append(None)
		
		cant_mal_nodes = int(len(self._graph.keys()) * self._prop_mal)
		cant_bot_memb = 0

		index = 0
		prob_memb = float(config_data["prob_memb"])
		prob_m_post = float(config_data["prob_m_post"])
		prob_m_mal = float(config_data["prob_m_mal"])
		prob_m_share = float(config_data["prob_m_share"])

		prob_nm_post = float(config_data["prob_nm_post"])
		prob_nm_mal = float(config_data["prob_nm_mal"])
		prob_nm_share = float(config_data["prob_nm_share"])
		
		self._af_publications = []
		for node in self._graph.keys():
			neighbours = self._graph[node]["neigh"]
			af_publication = None
			if index < cant_mal_nodes:

				if random.random() < prob_memb:
					sb_index = random.randint(0, len(self._social_botnets) - 1)
					if (self._social_botnets[sb_index] is None):
						af_publication = CFPublicationM(node, neighbours, self._dataset, self, prob_m_post, prob_m_mal, prob_m_share)
					else:
						af_publication = CFPublicationBM(node, neighbours, self._dataset, self, self._social_botnets[sb_index], prob_b_post, prob_b_mal, prob_b_share)
					self._social_botnets[sb_index] = af_publication
					self._graph[node]["type"] = "bot"
					cant_bot_memb += 1
				else:
					af_publication = CFPublicationM(node, neighbours, self._dataset, self, prob_m_post, prob_m_mal, prob_m_share)
					self._graph[node]["type"] = "mal"
			else:
				af_publication = CFPublicationNM(node, neighbours, self._dataset, self, prob_nm_post, prob_nm_mal, prob_nm_share)
				self._graph[node]["type"] = "non-mal"
			self._af_publications.append(af_publication)
			index += 1

	def _init_new_graph(self, num_nodes, num_edges):
		csv_graph_location = os.path.dirname(__file__) + "/graph_structure/graph(n="+ str(num_nodes) +", e="+ str(num_edges) + ").csv"
		executable_location = os.path.dirname(__file__) + '/executable/PaRMAT.exe'
		subprocess.call([executable_location, "-nEdges", str(num_edges), "-nVertices", str(num_nodes), "-noEdgeToSelf", "-noDuplicateEdges", "-output", csv_graph_location])
		graph = {}
		if self._graph is None:
			self._graph = {}
		for n in range(num_nodes):
			if not (str(n) in self._graph.keys()):
				self._graph[str(n)] = {}
			self._graph[str(n)]["neigh"] = []

		with open(csv_graph_location, newline = '', encoding = 'utf-8') as csvfile:
			spamreader = csv.reader(csvfile, delimiter = '\t')
			for row in spamreader:
				self._graph[row[0]]["neigh"].append(row[1])

	def get_trace(self):
		trace = {}
		post_data = []

		for time in range(0, self._t_sim):
			for af_publication in self._af_publications:
				post = af_publication.get_publication(time)
				if not post is None:
					data = {}
					node = af_publication.get_node()
					category = af_publication.get_dominant_category(time)
					data["id_post"] = post
					data["id_node"] = node
					data["dom_category"] = category
					data["time"] = time
					post_data.append(data)

		trace["graph"] = self._graph
		trace["post_data"] = post_data

		if (self._new_graph):
			self._init_new_graph(self._num_nodes, self._num_edges)

		return trace

	def _get_af_publication(self, node):
		result = None
		for af_publication in self._af_publications:
			if af_publication.get_node() == node:
				result = af_publication
				break

		return result

	def get_dominant_category(self, node, time):
		result = None
		af_publication = self._get_af_publication(node)
		if not af_publication is None:
			result = af_publication.get_dominant_category(time)

		return result

	def get_old_publication(self, node, category, time):
		result = None
		af_publication = self._get_af_publication(node)
		result = af_publication.get_old_publication(category, time)

		return result