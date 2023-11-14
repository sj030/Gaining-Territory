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

    def find_best_selection(self):

        # ***1. 한 번도 선택되지 않은 점 두 개를 찾아서 잇도록 시키기 (Degree가 0인 두 점 찾아서 잇기)***
        # 이미 선택된 선에 사용된 모든 점을 추출
        used_points = {point for line in self.drawn_lines for point in line}

        # 아직 선택되지 않은 점들 중에서 2개를 무작위로 선택하여 선을 만듦, 하지만 두 점을 잇지 못하는 경우는 제외시킴
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2))
                     if point1 not in used_points and point2 not in used_points and self.check_availability([point1, point2])]

        if available: #Degree가 0인 두 점이 있고 이을 수 있는 경우
            selected_pair = random.choice(available)
            print("1")
            return selected_pair
        else: #Degree가 0인 두 점이 있지만 이을 수 없을 경우 OR Degree가 0인 두 점이 없는 경우
            print("2")
            selected_pair = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
            return random.choice(selected_pair)
            
    
    def check_availability(self, line):
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
        for l in self.drawn_lines:
            if len(list(set([line[0], line[1], l[0], l[1]]))) == 3:
                continue
            elif bool(line_string.intersection(LineString(l))):
                condition3 = False

        # Must be a new line
        condition4 = (line not in self.drawn_lines)

        if condition1 and condition2 and condition3 and condition4:
            return True
        else:
            return False    

    
