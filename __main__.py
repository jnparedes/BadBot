import os
import json
from BadBot import BadBot

local_path = os.path.dirname(__file__)

if local_path=='':
	config_path = "config.json"
else:
	config_path = os.path.dirname(__file__) + "/config.json"

with open(config_path) as config_json:
	config_data = json.load(config_json)
num_traces = config_data["num_traces"]
output_path_base = config_data["output_path_base"]
badbot = BadBot(config_path)
if local_path=='':
	results_path = output_path_base
	results_dir = os.path.dirname(output_path_base)
else:
	results_path = os.path.dirname(__file__) + "/" + output_path_base
	results_dir = os.path.dirname(__file__) + "/" + os.path.dirname(output_path_base)

os.makedirs(results_dir, exist_ok=True)
for num in range(num_traces):
	trace = badbot.get_trace()
	with open(results_path + str(num) + '.json', 'w', encoding='utf-8') as json_file:
		json.dump(trace, json_file)