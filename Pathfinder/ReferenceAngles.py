import math
theta = 30
def getAngle(place1,place2,loader):
    dx = loader.coordinates[place2][0] - loader.coordinates[place1][0]
    dy = loader.coordinates[place2][1] - loader.coordinates[place1][1]
    angle = math.degrees(math.atan2(dy,dx))
    return angle


def validPlaces(source, final, destinations, loader  , flag=0):
    print("destinations",destinations)
    previousAngle=0
    B=0
    illegal=0
    angle = getAngle(source,final,loader)
    valid = []
    if angle<0:
        angle = 360-angle

    for i in range(len(destinations)):
        if destinations[i] != final:
            A = getAngle(source,destinations[i],loader)
            if i>0:
                B = getAngle(destinations[i-1],destinations[i],loader)
                
            if A<0 or B<0:
                A = 180+A
                B = 180+B
        

            if A >= angle-theta and A <= angle+theta:
                if B<90:
                    limit=180-previousAngle+B
                else:
                    limit=180-B+previousAngle
                if limit>120 or flag==0:
                    if(i>0):
                        print("previousAngle=",previousAngle,"B=",B,"oldPlace=",destinations[i-1],"nextPlace",destinations[i],"limit",limit)
                    valid.append(destinations[i])
                else:
                    print(destinations[i-1]," is too divergent from ", destinations[i])
                    illegal=1
                    break
            if i>0:
                 previousAngle=B

    
    valid.append(final)
    return tuple(sorted(valid))
