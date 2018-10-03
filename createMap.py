from Loader.mapLoader import mapLoader
import networkx as nx
import matplotlib.pyplot as plt

places=[]

with open('Loader/places.txt', 'r') as f:
    i=0
    reader = f.readlines()
    for place in reader:
        if place!='\n':
            i+=1
            places.append(place)

def loadDistances(place1, place2):
    distanceMatrix=[]
    with open('Loader/distances.txt') as results:
        for result in (results.readlines()):    
            t=[]            
            for i in result.split(' '):                    
                if i!='\n':
                    if i!='nan':
                        x=float(i)
                        t.append(x)
                    else:
                        t.append(19999)
            distanceMatrix.append(t)

    return distanceMatrix[places.index(place1)][places.index(place2)]
def makeMap(path):
	loader = mapLoader(100)
	loader.loadPlaces()
	loader.loadCoordinates()
	loader.loadGraph()
	for i in range(0,len(path)-1):
		place1 = loader.places[path[i]]
		place2 = loader.places[path[i+1]]
		w=loadDistances(place1, place2)
		if(w>0 and w<1000):
			loader.Graph.add_edge(places.index(place1),places.index(place2), weight=w)
	pos = dict(enumerate(loader.coordinates))
	nx.draw(loader.Graph, pos, with_labels=True)
	labels = nx.get_edge_attributes(loader.Graph,'weight')
	nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
	plt.show()
