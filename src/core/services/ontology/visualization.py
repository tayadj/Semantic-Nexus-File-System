import networkx
import pyvis
import seaborn



# URI = settings.DATA_STORAGE_PREFIX.get_secret_value() + '/.meta/ontology.html'

def ontology_visualization(URI, graph):

	communities_generator = networkx.community.girvan_newman(graph)
	next(communities_generator)
	communities = next(communities_generator)
	communities = sorted(map(sorted, communities))

	palette = seaborn.color_palette('hls', len(communities)).as_hex()
	group = 0

	for community in communities:

		color = palette.pop()
		group += 1

		for node in community:

			graph.nodes[node]['group'] = group
			graph.nodes[node]['color'] = color
			graph.nodes[node]['size'] = graph.degree[node]	

	network = pyvis.network.Network(
		notebook = False,
		cdn_resources = 'remote',
		height = '900px',
		width = '100%',
		select_menu = True,
		filter_menu = False
	)
	network.from_nx(graph)
	network.force_atlas_2based(central_gravity = 0.015, gravity = -31)
	network.show_buttons(filter_ = ["physics"])
	network.show(URI, notebook = False)

