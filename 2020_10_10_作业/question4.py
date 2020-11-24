class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False
def orientation(p, q, r):
    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0
def doIntersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    if ((o1 != o2) and (o3 != o4)):
        return True
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True
    return False


def pair_intersect(a, b):
    a_points = [(i,0) for i in a]
    b_points = [(i,1) for i in b]
    numbers = 0
    for i in range(len(a_points)-1):
        p1 = Point(a_points[i][0],a_points[i][1])
        q1 = Point(b_points[i][0],b_points[i][1])
        for j in range(i+1,len(a_points)):
            p2 = Point(a_points[j][0],a_points[j][1])
            q2 = Point(b_points[j][0],b_points[j][1])
            if doIntersect(p1, q1, p2, q2):
                numbers += 1
    return numbers


a = [1, 2, 3]
b = [2, 1, 3]
print(pair_intersect(a, b))

a = [3, 1, -1, 0]
b = [0, 2, 2, 3]
print(pair_intersect(a, b))