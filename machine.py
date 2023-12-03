import random
from itertools import combinations
from shapely.geometry import LineString, Point
from scipy.spatial import ConvexHull

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

        # Convex Hull 위의 점들을 무작위로 선택하는 함수
    def random_points_on_convex_hull(self, points):
        hull = ConvexHull(points)
        hull_points = [points[i] for i in hull.vertices]
        return random.choice(hull_points)
    
    def minimax(self, depth, is_maximizing):
        if depth == 0:
            return self.evaluate()

        if is_maximizing:
            best_score = float('-inf')
            available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]

            for move in available:
                self.drawn_lines.append(move)
                score = self.minimax(depth - 1, False)
                self.drawn_lines.remove(move)

                best_score = max(score, best_score)

            return best_score
        else:
            best_score = float('inf')
            available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]

            for move in available:
                self.drawn_lines.append(move)
                score = self.minimax(depth - 1, True)
                self.drawn_lines.remove(move)

                best_score = min(score, best_score)

            return best_score

    # 평가함수 - 휴리스틱 구현 -> 삼각형을 만들 수 있는지에 대한 가중치 적용
    def evaluate(self):
        # Check if triangles can be formed
        can_form_triangle = False
        for triangle in self.triangles:
            line1, line2, line3 = triangle
            if line1 in self.drawn_lines and line2 in self.drawn_lines and line3 in self.drawn_lines:
                can_form_triangle = True
                break

        if can_form_triangle:
            return 1
        else:
            return 0

    def find_best_selection(self):
        # 점이 12개까지 잡혔을 때 -> convex_hull을 통한 랜덤 점 잡기
        if len(self.whole_points) <= 12:
            return self.random_points_on_convex_hull()
        else:
            # 12개 이후 -> min_max를 이용한 점 잡기
            machine_turn = True
            available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
            best_score = float('-inf')
            best_move = None

            for move in available:
                self.drawn_lines.append(move)
                score = self.minimax(1, machine_turn)
                self.drawn_lines.remove(move)

                if score > best_score:
                    best_score = score
                    best_move = move

            return best_move
    
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