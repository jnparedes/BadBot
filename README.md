# **BadBot**

**BadBot** is a testbed designed to generate full traces of actions occurring on complex networks (such as those involved in social platforms) at different times, according to a set of parameters that characterize a desired setting. The main purpose of BadBot is to address the lack of generally-available adequate data sets with ground truth about malicious behaviour on social media. This testbed combines real-world malicious and non-malicious content (such as fake and real news) datasets with synthetically-generated networks of users and fully-detailed traces of their behavior throughout a series of time points.

##### Badbot's settings can be adjusted through the following parameters (defined in config.json):
- num_traces: number of traces that will be generated.
- output_path_base: path base where the result of every trace will be saved. For example: "results/trace" specifies that every trace will be saved in the directory "results" and the files will have the base name "trace" followed by a sequence number.
- dataset_csv: allows us to define the setting of the malicious and non-malicious content dataset (only CSV format is admitted). The following sub-parameters must be set:
    - location: location of the dataset.
    - id: columm name of the tuple id.
    - content: columm name of the malicious and non-malicious content.
    - category: columm name of the category for the content.
    - gt: columm name of the ground truth for the content (malicious or non-malicious).
    - delimiter: specifies the character to delimit columns.
    - positive_labels: specifies a list of values that can be considered positive ground truth.
    - negative_labels: specifies a list of values that can be considered negative ground truth.
- num_nodes: number of nodes in graph G. 
- num_edges: number of edges in graph G.
- t_sim: number of time points in the generated traces.
- prop_mal: proportion of malicious nodes in G.
- num_botnet: number of botnets to be generated.
- prob_memb: probability that a malicious node is a botnet member.
- prob_nm_post: probability that a non-malicious node posts an article (malicious or not) at each time point.
- prob_m_post: probability that a malicious node posts an article (malicious or not) at each time point.
- prob_b_post: probability that a botnet (i.e., all members) posts an article (malicious or not) at each time point.
- prob_nm_mal: probability of choosing a malicious post when a non-malicious node creates a new post.
- prob_m_mal: probability of choosing a malicious post when a malicious node creates a new post.
- prob_b_mal: probability of choosing a malicious post when a botnet creates a new post.
- prob_nm_share: probability that a non-malicious node shares a post from its neighbors.
- prob_m_share: probability that a malicious node shares a post from its neighbors.
- prob_b_share: probability that a botnet shares a post from its neighbors.


##### The output of every trace is in json format with the following structure:
- graph: an object that contains the structure of the graph where every node id is key and the value is an object with the following structure:
    - neigh: array with the node ids that are neighbors of the corresponding node id.
    - type: has as value one the following strings: 'non-mal' (non-malicious node), 'mal' (malicious node), or 'bot' (botnet member node).
- post-data: an array of objects with the post information on the network defined by the following structure:
    - id_post: is the id of some post in the dataset.
    - id_node: is the node id of the node that posted.
    - time: is the time for the post activity.
    - dom_category: is the most frequent category in the posts of id_node at the corresponding time.

The structure of the graph is obtained using the [PaRMAT](https://github.com/farkhor/PaRMAT) implementation. As the implementation is based on C++, we create an executable (see executable directory); for now, this was done only for the Windows platform.

The file "config.json" contains the setting for create two trace examples based on the fake news dataset located in "example/datasets/fake_news/fake-news-detection/data.csv".

##### Dependencies:
- [python](https://www.python.org/downloads/)
- [cygwin](https://www.cygwin.com/)