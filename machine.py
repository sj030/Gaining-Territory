import random
from itertools import combinations
from shapely.geometry import LineString, Point

class MACHINE():
    """
        [ MACHINE ]
        MinMax Algorithm을 통해 수를 선택하는 객체.
        - 모든 Machine Turn마다 변수들이 업데이트 됨

        ** To Do **
        MinMax Algorithm을 이용하여 최적의 수를 찾는 알고리즘 생성
           - class 내에 함수를 추가할 수 있음
           - 최종 결과는 find_best_selection을 통해 Line 형태로 도출
               * Line: [(x1, y1), (x2, y2)] -> MACHINE class에서는 x값이 작은 점이 항상 왼쪽에 위치할 필요는 없음 (System이 organize 함)
    """
    def __init__(self, score=[0, 0], drawn_lines=[], whole_lines=[], whole_points=[], location=[]):
        self.id = "MACHINE"
        self.score = [0, 0] # USER, MACHINE
        self.drawn_lines = [] # Drawn Lines
        self.board_size = 7 # 7 x 7 Matrix
        self.num_dots = 0
        self.whole_points = []
        self.location = []
        self.triangles = [] # [(a, b), (c, d), (e, f)]

        # for convex Hull
        self.isFirst = True
        self.HullLines = []
        self.HullPoints = []
        self.ansTriNum = 0
        self.ansLineNum = 0
        # Q. num dots와 whole_points의 차이?

    def find_best_selection(self):
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2], self.drawn_lines)]

        # convex hull 구하는 과정 -> 처음 한 번만 실행
        if self.isFirst:
            self.getConvexHull(self.whole_points)
            self.isFirst = False

        availConv = []
        for i in self.HullLines:
            if self.check_availability(i, self.drawn_lines):
                availConv.append(i)
        if len(availConv) == 0:
            return random.choice(available)
        else:
            return random.choice(availConv)

    def ccw(self, p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    def getConvexHull(self, points):
        points = sorted(points)
        lower = []
        for p in points:
            while len(lower) >= 2 and self.ccw(lower[-2], lower[-1], p) < 0:
                lower.pop()
            lower.append(p)
        upper = []
        for p in reversed(points):
            while len(upper) >= 2 and self.ccw(upper[-2], upper[-1], p) < 0:
                upper.pop()
            upper.append(p)
        self.HullPoints = lower[:-1] + upper[:-1]
        for idx in range(len(self.HullPoints) - 1):
            self.HullLines.append([self.HullPoints[idx], self.HullPoints[idx + 1]])
        self.ansTriNum = (2 * len(self.whole_points)) - len(self.HullPoints) + 2
        self.ansLineNum = (3 * len(self.whole_points)) - len(self.HullPoints) + 3
        print(" Hull point is " + str(self.HullPoints))
        print(" Hull Line is " + str(self.HullLines))
        print(" ANS TRI is " + str(self.ansTriNum))
        print(" ANS LINE is " + str(self.ansLineNum))


    def check_availability(self, line, drawn):
        line_string = LineString(line)

        # Must be one of the whole points
        condition1 = (line[0] in self.whole_points) and (line[1] in self.whole_points)
        
        # Must not skip a dot
        condition2 = True
        for point in self.whole_points:
            if point==line[0] or point==line[1]:
                continue
            else:
                if bool(line_string.intersection(Point(point))):
                    condition2 = False

        # Must not cross another line
        condition3 = True
        for l in drawn:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in drawn)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
