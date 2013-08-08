
def circle(radius):
    arr = [[0 for _ in range(2*radius+1)] for _ in range(2*radius+1)]
    
    x0 = radius
    y0 = radius
    f = 1 - radius
    ddf_x = 1
    ddf_y = -2 * radius
    x = 0
    y = radius
    arr[x0][y0 + radius] =  1
    arr[x0][ y0 - radius] = 1    
    arr[x0 + radius][y0] = 1     
    arr[x0 - radius][y0] = 1    
 
    while x < y:
        if f >= 0: 
            y -= 1
            ddf_y += 2
            f += ddf_y
        x += 1
        ddf_x += 2
        f += ddf_x    
        arr[x0 + x][ y0 + y] = 1
        '''arr[x0 - x, y0 + y, colour)
        arr[x0 + x, y0 - y, colour)
        arr[x0 - x, y0 - y, colour)
        arr[x0 + y, y0 + x, colour)
        arr[x0 - y, y0 + x, colour)
        arr[x0 + y, y0 - x, colour)
        arr[x0 - y, y0 - x, colour)'''
    return arr

c = circle(7)

for l in c:
    s=""
    for n in l:
        s+=str(n)
    print s
