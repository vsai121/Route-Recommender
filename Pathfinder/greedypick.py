import networkx as nx
import numpy as np
from Pathfinder.ZoneAngle import validPlaces , validate
import math
from scipy.spatial import distance
loader = None
start = None

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
    
def findEuclideanDistance(place1,place2,loader):
    x1=loader.coordinates[place1][0]
    x2=loader.coordinates[place2][0]
    y1=loader.coordinates[place1][1]
    y2=loader.coordinates[place2][1]
    point1=[x1,y1]
    point2=[x2,y2]
    return distance.euclidean(point1,point2)


def cmpdist(i):
    global start
    disti = nx.shortest_path_length(loader.Graph, source=start,target=i,weight='weight')
    #distj = nx.shortest_path_length(loader.Graph, source=start, target=j, weight='weight')
    return disti#-distj


def greedyorder(s, destinations, l): #this
    global start
    global loader
    start = s
    loader = l

    left2visit = list(tuple(destinations))
    path = []
    tovisit = list(tuple(left2visit))
    # try:
    #     tovisit = sorted(tovisit, key=cmpdist)
    # except TypeError:
    #     print("caught")

    current = start
    for i in range(len(tovisit)):
        spaths = [math.inf] * len(left2visit)
        #eucledianDist = [math.inf] * len(left2visit)
        for j in range(0,len(left2visit)):
            #spaths[j] = nx.shortest_path_length(loader.Graph, source=current, target=left2visit[j], weight='weight')
            spaths[j] = findEuclideanDistance(current ,  left2visit[j] , l)
            #print("Place1" , loader.places[i] , "Place2" , loader.places[j] , "Distance" , spaths[j])
        minind = spaths.index(min(spaths))
        path.append(left2visit[minind])
        current = left2visit[minind]
        del (left2visit[minind])

    return path

def pathGenerator(start, orderedLocations, loader):
    allPaths = {}
    for x in orderedLocations:
        x=orderedLocations[x]
        final = x[-1]
        allPaths[final]=[]
        for i in powerset(x[0:-1]):
            i.append(final)
            finalPath=[]
            s=start
            alreadyConsidered=False
            if validate(start,i,loader):
                # for j in i:
                #   for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight'):
                #       if k not in finalPath:
                #           finalPath.append(k)

                #   s=j

                for route in allPaths[x[-1]]:
                    if set(i).issubset(set(route)):
                        alreadyConsidered=True
                        break

                if alreadyConsidered==False:                    
                    allPaths[x[-1]].append(i)
    return allPaths
        
