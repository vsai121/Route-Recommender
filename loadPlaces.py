places=[]
with open('places.txt', 'r') as f:
    reader = f.readlines()
    for place in reader:
    	place=place.split()[0]		
    	places.append(place)