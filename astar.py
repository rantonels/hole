end = None

NLUT = [ (1,0) , (0,1) , (-1,0) , (0,-1) ]

class Tile:
    def __init__(self,x,y,g=0,parent=None):
        self.x = x
        self.y = y
        self.g = g
        self.parent = parent
        global end
        self.h = ((abs(self.x-end[0]) + abs(self.y-end[1])))

    def __eq__(self,other):
        if other == None:
            return False
        return ( (self.x == other.x) and (self.y == other.y))
    def __ne__(self,other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash((self.x,self.y))

    def __str__(self):
        if self.parent == None:
            sss = ""
        else:
            sss = " <- "+str(self.parent.coords())
        return "<"+str(self.x)+"."+str(self.y)+"g"+str(self.g)+">"+sss
    def __repr__(self):
        return "<"+str(self.x)+"."+str(self.y)+">"

    def coords(self):
        return (self.x,self.y)

    def f(self):
        return self.g + self.h
 
    def nbd(self):
        global NLUT
        return [ Tile(self.x + n[0], self.y + n[1], self.g + 1, self) for n in NLUT]



def pathfind(mapfunction,start,endp):

    global end
    end = endp
    DEBUG = False
#   DEBUG = True


    def log(st):
        if DEBUG:
            print(st)

    startile = Tile(start[0],start[1],0)
    endtile = Tile(end[0],end[1])

    path = []

    # init openSet with the starting tile
    openSet = set([startile])
    closedSet = set()
    
    stepcount = 0

    #the loop, as long as openSet is not empty:
    while len(openSet)>0:

        log(str(stepcount)+"-"+str(openSet))
        stepcount += 1
        fcur = float("inf")
        #find lowest f-count tile in the open set
        for o in openSet:
            if o.f() < fcur:
                fcur = o.f()
                current = o

        log("current: "+str(current))

        #move the current tile to the closed set
        openSet.remove(current)
        closedSet.add(current)

        #find the von neumann neighbourhood
        nbd = current.nbd()
        log("nbd: "+str(nbd))
        #work on the neighbours
        for n in nbd:

            log("processing "+str(n))

            
            if mapfunction(n.x,n.y) != 0: #if it's blocked, ignore
                log("it was blocked.")
                continue
            elif n in closedSet: #if it's in the closed set, ignore
                log("it was in the closed set.")
                continue
            elif n in openSet: #if it's in the open set...
                log("it's in the open set...")
                for e in openSet: 
                    if n==e:            #find the old copy of n in the open set
                        if n.g < e.g:   #if it's a better path, substitute
                            log("SUBSTITUTION")
                            openSet.remove(e)
                            openSet.add(n)
                        else:
                            log("old path was better.")

                        break           #no need to go on...
            else: #if it's not in the open set, add it
                log("not in the open set, adding...")
                openSet.add(n)
        

        if endtile in closedSet:          #if we're done
            #find copy of endtile in closedSet
            for e in closedSet:
                if e == endtile:
                    rec = e
            while (not rec == None) and rec != startile:  #reconstruct the path
                path.append(rec.coords())
                rec = rec.parent
            path.append(startile.coords())
            return path  
    #if openset is empty, no path was found. :(        
    return -1
        




