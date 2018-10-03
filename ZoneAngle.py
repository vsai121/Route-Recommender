import math

theta = 30

def getAngle(place1,place2,loader):
    dx = loader.coordinates[place2][0] - loader.coordinates[place1][0]
    dy = loader.coordinates[place2][1] - loader.coordinates[place1][1]
    angle = math.degrees(math.atan2(dy,dx))
    return angle

def validPlaces(source, final, destinations, loader):
    angle = getAngle(source,final,loader)
    valid = []
    B=0
    if angle<0:
        angle = 360-angle

    for i in range(len(destinations)):
        if destinations[i] != final:
            A = getAngle(source,destinations[i],loader)
            if A<0:
                A = 360-A
            if A >= angle-theta and A <= angle+theta:
                valid.append(destinations[i])

    valid.append(final)
    return tuple(sorted(valid))


def validate(source,path , loader):
    place1 = source
    place2=path[0]
    illegal=0
    for i in range(1 , len(path)):

        previousAngle=getAngle(place1 , place2 , loader)

        place1=place2
        place2=path[i]

        B=getAngle(place1 , place2 , loader)

        if B<90:
            limit=180-previousAngle+B
        else:
            limit=180-B+previousAngle

        if limit <150:
            illegal=1
            break

    if illegal:
        return 0

    return 1
