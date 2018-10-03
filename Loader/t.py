import requests
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

places=[]
scale=100
results=[]
coordinates=[]
key1="AIzaSyBPixfCdBcIm0ro9AXK0zT1HnesX5R7Wh8"
key2="AIzaSyCoXBaC8uyQmSJonX93wMfcPccYifyJbBQ"
gpskey1="AIzaSyCTnzAuLCDjYydqRwHjz1tkuRgQlaqZ1jI"
gpskey2="AIzaSyCuNEeLc1QTlEO81CSCuor9Xz_vW8T9xog"
geocode_keys=[]
distance_keys=[]


with open('places.txt', 'r') as f:
	reader = f.readlines()
	for place in reader:
		if len(place)>2:
			place = " ".join(place.split())
			places.append(place)

with open('coordinates.txt') as results:  
	for result in (results.readlines()):
		if(len(json.loads(result)['results'])>=1):
			coordinate = (json.loads(result)['results'][0]['geometry']['location']['lng'] * scale,json.loads(result)['results'][0]['geometry']['location']['lat'] * scale)
			coordinates.append(coordinate)
		else:
			coordinates.append((-1,-1))

def loadDistances(place1, place2):
	failed=[]
	try:
		result = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + place1 + ',India&destinations=' + place2+'Madhya Pradesh,India&key='+key1)
		result = result.content.decode('utf-8')
		print(result)
	except:
		result = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + place1+ ',India&destinations=' + place2+ 'Madhya Pradesh,India&key='+key2)
		result = result.content.decode('utf-8')
		print(result)
	try:
		distance = (json.loads(result)['rows'][0]['elements'][0]['distance']['text'])
		distance=distance.split('km')[0]
		distance="".join(distance.split(','))
		distance = float(distance)
		return distance
	except Exception as e:
		failed.append([place1,place2])
	
t = Delaunay(coordinates)
nodes = list(range(len(coordinates)))
map = np.zeros((len(coordinates), len(coordinates)))
edges = []
m = dict(enumerate(nodes))  # mapping from vertices to nodes
Graph = nx.Graph()
for i in range(t.nsimplex):
	edges.append((m[t.vertices[i, 0]], m[t.vertices[i, 1]]))
	edges.append((m[t.vertices[i, 1]], m[t.vertices[i, 2]]))
	edges.append((m[t.vertices[i, 2]], m[t.vertices[i, 0]]))

for edge in edges:
	i = edge[0]
	j = edge[1]
	place1 = places[edge[0]]
	place2 = places[edge[1]]
	if "Bhopal" in place2:
		map[i, j] = loadDistances(place1, place2)
		map[j, i] = map[i, j]
		print(map[j,i])
		Graph.add_edge(i,j, weight=map[i,j])

with open('distances2.txt','w') as file:
	for i in map:
		for j in i:
			file.write(str(j))
			file.write(' ')
		file.write('\n')
