import networkx as nx
from Pathfinder.greedypick import greedyorder
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
loader.loadEdges()
places=[]
allValid = []
with open('Loader/places.txt', 'r') as f:
    reader = f.readlines()
    for place in reader:
        places.append(place)

def recommend(bestPaths,key,start):
	print("path is ", bestPaths[key],"\n")
	destinations=key.split("\n")
	for i in range(len(destinations)):
		print(destinations)
		if destinations[i]!='':
			for road in nx.all_simple_paths(loader.Graph, source=places.index(start+"\n"), target=places.index(destinations[i]+"\n"), cutoff=3):
				print("ALTERNATES FROM ",start,loader.places.index(start+"\n")," TO ",loader.places.index(destinations[i]+"\n")," ROAD ",road)
			start=destinations[i]
	return allValid

	