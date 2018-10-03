import math

import matplotlib.pyplot as plt
import networkx as nx
from scipy.spatial import distance

theta = 30
maxDeviation = 150

def getAngle(place1,place2,loader):
    dx = loader.coordinates[place2][0] - loader.coordinates[place1][0]
    dy = loader.coordinates[place2][1] - loader.coordinates[place1][1]
    angle = math.degrees(math.atan2((dy),(dx)))
    return angle

def validPlaces(source, final, destinations, loader): #this

    angle1 = getAngle(source,final,loader)
    angle2 = getAngle(final , source , loader)
    valid = []
    B=0
    if angle1<0:
        angle1 = 360+angle1

    if angle2<0:
        angle2 = 360+angle2

    for i in range(len(destinations)):
        if destinations[i] != final:
            A = getAngle(source,destinations[i],loader)
            C = getAngle(final , destinations[i] , loader)
            if A<0:
                A+=360
            if C<0:
                C+=360

            if A >= angle1-theta and A <= angle1+theta  and C >= angle2-theta and C <= angle2+theta:
                valid.append(destinations[i])


    valid.append(final)
    return tuple(valid)

def findEuclideanDistance(place1,place2,loader):
    x1=loader.coordinates[place1][0]
    x2=loader.coordinates[place2][0]
    y1=loader.coordinates[place1][1]
    y2=loader.coordinates[place2][1]
    point1=[x1,y1]
    point2=[x2,y2]
    return distance.euclidean(point1,point2)

def validate(source,path,loader): #this

    #print("In validate\n")
    #print("Path\n" , path)
    if len(path)<=1:
        #print("Less than 2");
        return 1
    place1 = source
    place2=path[0]
    place3=path[1]
    distance12=findEuclideanDistance(place1,place2,loader)
    distance13=findEuclideanDistance(place1,place3,loader)
    distance23=findEuclideanDistance(place2,place3,loader)

    pathDeviation=math.degrees(math.acos((distance12**2+distance23**2-distance13**2)/(2*distance12*distance23)))
    #print("PLACE1=",place1,"PLACE2=",place2,"PLACE3=",place3,"DISTANCE12=",distance12,"DISTANCE13=",distance13,"DISTANCE23=",distance23,"PATH_DEV=",pathDeviation,"\n")
    legal=1
    if pathDeviation<maxDeviation:
        legal=0
    else:
        for i in range(2, len(path)):
            legal=1
            place1=place2
            place2=place3
            place3=path[i]
            distance12=findEuclideanDistance(place1,place2,loader)
            distance13=findEuclideanDistance(place1,place3,loader)
            distance23=findEuclideanDistance(place2,place3,loader)
            pathDeviation=math.degrees(math.acos((distance12**2+distance23**2-distance13**2)/(2*distance12*distance23)))
            #print("PLACE1=",place1,"PLACE2=",place2,"PLACE3=",place3,"DISTANCE12=",distance12,"DISTANCE13=",distance13,"DISTANCE23=",distance23,"PATH_DEV=",pathDeviation,"\n")
            if pathDeviation<maxDeviation:
                legal=0
                break
    return legal
