from Pathfinder.greedypick import greedyorder
from Pathfinder.greedypick import pathGenerator
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces , validate
import matplotlib.pyplot as plt
import networkx as nx
from createMap import makeMap
from recommender import recommend

def powerset(s):
	power=[]
	x = len(s)
	for i in range(1 << x):
		t=[s[j] for j in range(x) if (i & (1 << j))]
		
		if len(t)>0:
			power.append(t)
	if len(power) == 0:
		power = [[]]
	power = sorted(power,key=len,reverse=True)
	return power

def subtractList(l1,l2):
	retList = []
	for i in l1:
		if i not in l2:
			retList.append(i)
	return retList

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
loader.loadEdges()
pos = dict(enumerate(loader.coordinates))
nx.draw(loader.Graph, pos, with_labels=True)
labels = nx.get_edge_attributes(loader.Graph,'weight')
nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
plt.show()

start = input("Enter source:")
startPoint=start
start=loader.places.index(start+'\n')
tovisit = input("Enter your desired destinations:").split()
for i in range(len(tovisit)):
	tovisit[i] = loader.places.index(tovisit[i]+"\n")
allValid = []
orderedLocations = {}

"""
recommendedVisits = [start]

for x in tovisit:
	recommendedVisits.append(x)

recommendedVisits = recommend(recommendedVisits)

"""


#Generate valid paths
for i in tovisit:
	valid = validPlaces(start, i,tovisit,loader)
	allValid.append(valid)

	path = greedyorder(start, valid, loader)
	orderedLocations[i] = list(path)



print("orderedLocations", orderedLocations,"AllValid", allValid)
lastRoutes=[]


#main
allPaths= pathGenerator(start,orderedLocations,loader)
# for x in orderedLocations:
# 	x=orderedLocations[x]
# 	final = x[-1]
# 	allPaths[final]=[]
# 	for i in powerset(x[0:-1]):
# 		i.append(final)
# 		finalPath=[]
# 		s=start
# 		alreadyConsidered=False
# 		if validate(start,i,loader):
# 			# for j in i:
# 			# 	for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight'):
# 			# 		if k not in finalPath:
# 			# 			finalPath.append(k)

# 			# 	s=j

# 			for route in allPaths[x[-1]]:
# 				if set(i).issubset(set(route)):
# 					alreadyConsidered=True
# 					break

# 			if alreadyConsidered==False:					
# 				allPaths[x[-1]].append(i)


'''2.0'''
print(allPaths)

returnLocations = {}
returnPaths = {}
journeys = []
for dest in allPaths:
	for p in allPaths[dest]:
		returnLocations[str(p)] = list(reversed(subtractList(orderedLocations[dest],p)))
		returnLocations[str(p)].append(start)
		returnPaths[str(p)] = pathGenerator(dest,returnLocations,loader)
		for x in returnPaths[str(p)][start]:
			p.extend(i for i in x)
		journeys.append(list(p))
		#journeys.append(returnPaths[str(p)])

print("Return Locations = ", returnLocations)
print("Return Paths = ", returnPaths)
print("journeys=",journeys)
print("Tovisit=",tovisit)
#implementing bit buckets for easy searching of subsets
journeyBits={}
for route in journeys:
	key=0
	for destination in route[:-1]:
		key+=2**(tovisit.index(destination))
	journeyBits[key]=route
print(journeyBits)
keys=list(journeyBits.keys())
keys=sorted(keys,reverse=True)
print(keys)


for i in range(1,len(keys)):
	for j in range(0,i):
		subset=keys[i]&keys[j]
		print(keys[i],'&',keys[j],keys[i]&keys[j])
		if subset==keys[i] or subset==keys[j]:
			del journeyBits[subset]
			break
print(journeyBits)
journeys=[]
for key in journeyBits:
	journeys.append(journeyBits[key])
print(journeys)
fullJourneys=[]
for journey in journeys:
	fullJourney=[start]
	s=start
	for j in journey:
		for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight')[1:]:
			fullJourney.append(k)

		s=j
	fullJourneys.append(fullJourney)
print("WHOLE JOURNEY=",fullJourneys)

# returnRoutes=[]
# bestPaths={}
# for lastRoute in lastRoutes:
# 	currentRoute=(lastRoute)
# 	#legal = validate(start,currentRoute , loader)
# 	includedDestinations=[loader.places[x] for x in currentRoute if x in tovisit]
# 	bestPaths["".join(includedDestinations)]=currentRoute
# 	print("Final path is:",currentRoute," includes destinations:",includedDestinations)
# 	print("*"*50)


# 	destinations=lastRoute
# 	#Retreive return routes
# 	source=destinations[-1]
# 	destinations=[x for x in destinations if x in tovisit]
# 	returnPlaces=list(set(tovisit)-set(destinations)-set([start])) #Stores places that need to be included on the way back
# 	print('Return places',returnPlaces,'for destinations',destinations,'source',source)
# 	returnPlaces.append(start) #Make sure you can get to journey start point from current destination
# 	validReturns=validPlaces(source, start,returnPlaces,loader)
# 	print('ValidReturns=',validReturns)

# 	allValid=[]
# 	allPaths=[]

# 	#Apply same algorithm used to find onward route

# 	for i in validReturns:
# 		valid = validPlaces(source, i,validReturns,loader)
# 		print("i" , i , "Valid" , valid);

# 		if valid not in allValid:
# 			allValid.append(valid)
# 			path = greedyorder(source, valid, loader)
# 			if path[-1]==start:
# 				allPaths.append(path)


# 	for x in allPaths:
# 		for i in powerset(x):
# 			finalPath=[]
# 			s=source
# 			if validate(source,i,loader):
# 				for j in i:
# 					for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight'):
# 						if k not in finalPath:
# 							finalPath.append(k)

# 					s=j
# 				#if finalPath not in lastRoutes:
# 				returnRoutes.append(finalPath)
# 	print('Destinations',destinations,'returnRoutes',returnRoutes)







# a=bestPaths
# remainingPlaces=tovisit
# bestPaths={}
# numberOfPlaces=lambda s:s.count("\n")
# sortedKeys=sorted(a,key=numberOfPlaces,reverse=True)
# for key in sortedKeys:
# 	bestPaths[key]=a.get(key)
# print(bestPaths)

# #Checking for path subsets
# for key in bestPaths:
# 	placesVisited=key.split("\n")
# 	placesRemoved=0
# 	for place in placesVisited:
# 		if place!='' and loader.places.index(place+'\n') in remainingPlaces:
# 			remainingPlaces.remove(loader.places.index(place+"\n"))
# 			placesRemoved+=1
# 	if placesRemoved:
# 		print(remainingPlaces)
# 		#recommend(bestPaths,key,startPoint) incomplete
# 		currentRoute=bestPaths[key]
# 		makeMap(currentRoute)
# 	if len(remainingPlaces)==0:
# 		break

