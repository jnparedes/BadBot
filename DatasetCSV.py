import csv
import random
from Dataset import Dataset
from abc import abstractmethod

class DatasetCSV(Dataset):

	def __init__(self, location, id_ds, content, category, ground_truth, positive_labels, negative_labels, delimiter=','):
		self._id_ds = id_ds
		self._content = content
		self._category = category
		self._ground_truth = ground_truth
		self._delimiter = delimiter
		self._positive_labels = positive_labels
		self._negative_labels = negative_labels
		super().__init__(location)

	def _load_data(self):
		data = {}
		total_categories = set()
		with open(self._location, newline='', encoding='utf-8') as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				data[row[self._id_ds]] = {self._content: row[self._content], self._ground_truth: row[self._ground_truth], self._category: row[self._category]}
				total_categories.add(row[self._category])
		self._data = data
		self._total_categories = list(total_categories)

	def get_data(self):
		return self._data

	def get_ids(self):
		return list(self._data.keys())

	def get_ground_truth(self, data_id):
		return self._data[data_id][self._ground_truth]

	def get_category(self, data_id):
		return self._data[data_id][self._category]

	def get_categories(self):
		return self._total_categories

	def _is_positive_label(self, label):
		return label in self._positive_labels

	def _is_negative_label(self, label):
		return label in self._negative_labels

	def get_id_data(self, label, category):
		label_targets = None
		result = None
		if label:
			label_targets = self._positive_labels
		else:
			label_targets = self._negative_labels

		data_ids = self.get_ids()
		index_id = random.randint(0, len(data_ids) - 1)
		data_id = data_ids[index_id]


		while (not self.get_ground_truth(data_id) in label_targets) or (not self.get_category(data_id) == category):
				index_id = random.randint(0, len(data_ids) - 1)
				data_id = data_ids[index_id]

		result = data_id

		return result
