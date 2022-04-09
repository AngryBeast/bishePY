class LocationStruct:
    def __init__(self,name,x,y,z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    
    def printSelfData(self):
        print('name:%s, X:%d, Y:%d, Z:%d' %(self.name,self.x, self.y ,self.z))


L = LocationStruct('car',0,1,2)
L.printSelfData()