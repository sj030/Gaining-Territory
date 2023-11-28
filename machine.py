import random
from itertools import combinations
from itertools import product, chain, combinations
from shapely.geometry import LineString, Point, Polygon

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
        
        self.FirstTriangle = 0
        self.MaxScore_depth3 = 0
        self.MinScore_depth2 = 0
        self.MaxScore_depth1 = 0

        self.Alpha = float('-inf')
        self.Beta = float('inf')

    def find_best_selection(self):

        
        #***가장 첫 번째 로직: 삼각형을 만들 수 있으면 만들기***
        max_eval = float('-inf')
        best_move = None

        for move in self.generate_moves():
            self.make_move(move, True, depth=-1)
            eval = self.FirstTriangle
            self.FirstTriangle = 0

            self.undo_move(move)

            if eval > max_eval:
                max_eval = eval
                best_move = move

        return best_move
        
        """
        #한 번 이상 사용된 점들을 찾아 저장한다.
        used_points = set(point for line in self.drawn_lines for point in line)
    
        # 두 번 이상 사용된 점들을 찾아 Double_selected_points에 저장한다.
        double_selected_points = [point for point in used_points if self.degree_of_point(point) >= 2]
        available = []

        # 두 번 이상 사용된 점들 중 기준이 되는 점을 선택한다.
        for double_point in double_selected_points:
            connected_lines = [line for line in self.drawn_lines if double_point in line]
            connected_points = set(point for line in connected_lines for point in line if point != double_point)
            
            # 기준이 되는 점과 연결된 다른 점들 중에서 삼각형이 가능한 선을 찾고, available에 추가한다.
            for connected_point_pair in combinations(connected_points, 2):
                potential_line = list(connected_point_pair)
            
                if self.check_availability(potential_line):
                    available.append(potential_line)
        # 삼각형이 가능한 모든 선을 찾았으면 그 선들 중 하나를 랜덤으로 선택한다.
        if available:  
            print(available)
            selected_pair = random.choice(available)
            print("1")
            return selected_pair
        """
        #***첫 번째 로직 끝***
        
        #***두 번째 로직: 한 번도 선택되지 않은 점 두 개를 찾아서 잇도록 시키기 (Degree가 0인 두 점 찾아서 잇기)***
        
        # 이미 선택된 선에 사용된 모든 점을 추출
        used_points = {point for line in self.drawn_lines for point in line}

        # 아직 선택되지 않은 점들 중에서 2개를 무작위로 선택하여 선을 만듦, 하지만 두 점을 잇지 못하는 경우는 제외시킴
        available = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2))
                     if point1 not in used_points and point2 not in used_points and self.check_availability([point1, point2])]

        if available: #Degree가 0인 두 점이 있고 이을 수 있는 경우
            selected_pair = random.choice(available)
            print("2")
            return selected_pair
        else: #Degree가 0인 두 점이 있지만 이을 수 없을 경우 OR Degree가 0인 두 점이 없는 경우
            self.MaxScore_depth1 = 0
            self.MinScore_depth2 = 0
            self.MaxScore_depth3 = 0

            self.Alpha = float('-inf')
            self.Beta = float('inf')

            print("3")
            best_value, best_move = self.minimax(3, True)  # 최대 깊이는 3으로 설정 (조절 가능)
            print(best_move)
            return best_move
            """
            print("2")
            selected_pair = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
            return random.choice(selected_pair)
            """
        #***두 번째 로직 끝***
        
        """
        self.MaxScore_depth1 = 0
        self.MinScore_depth2 = 0
        self.MaxScore_depth3 = 0

        self.Alpha = float('-inf')
        self.Beta = float('inf')

        #print("before minmax")
        best_value, best_move = self.minimax(3, True)  # 최대 깊이는 3으로 설정 (조절 가능)
        print(best_move)
        return best_move
        """

    def minimax(self, depth, maximizing_player):
        if depth == 0 or self.is_game_over() or not self.generate_moves():
            #print("여기요")
            return self.evaluate_board(), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for move in self.generate_moves():
                self.make_move(move, maximizing_player, depth)
                eval = self.minimax(depth - 1, False)[0]
                #print(eval)
                if(depth == 1): 
                    self.MaxScore_depth1 = 0
                    #알파값 갱신
                    if(eval > self.Alpha):
                        self.Alpha = eval
                elif(depth == 3):
                    self.MaxScore_depth3 = 0

                self.undo_move(move)

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                if(depth == 1): #depth가 1일 때만
                    #결과가 베타값보다 크거나 같으면 가지치기
                    if(eval >= self.Beta):
                        break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None

            for move in self.generate_moves():
                self.make_move(move, maximizing_player, depth)
                eval = self.minimax(depth - 1, True)[0]
                #print(eval)
                if(depth == 2):
                    self.MinScore_depth2 = 0
                    #베타값 갱신
                    if(eval < self.Beta):
                        self.Beta = eval
                self.undo_move(move)

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                #결과가 알파값보다 작거나 같으면 가지치기
                if(eval <= self.Alpha):
                    break

            return min_eval, best_move

    def evaluate_board(self):
        
        return self.MaxScore_depth1 - self.MinScore_depth2 + self.MaxScore_depth3

    def check_endgame(self):
        remain_to_draw = [[point1, point2] for (point1, point2) in list(combinations(self.whole_points, 2)) if self.check_availability([point1, point2])]
        return False if remain_to_draw else True

    def is_game_over(self):
        self.check_endgame()    

    def generate_moves(self):
        # 가능한 모든 선분을 moves에 추가
        moves = []
        for point1, point2 in combinations(self.whole_points, 2):
            line = [point1, point2]
            if self.check_availability(line):
                moves.append(line)
        return moves

    def make_move(self, move, turn, depth):
        # 움직임을 수행하는 로직을 추가하세요.
        if(turn):
            #move = self.organize_points(move)
            if self.check_availability(move):
                self.drawn_lines.append(move)
                self.check_triangle_Max(move, depth)
            pass
        else:
            #move = self.organize_points(move)
            if self.check_availability(move):
                self.drawn_lines.append(move)
                self.check_triangle_Min(move, depth)
            pass


    def undo_move(self, move):
        # 움직임을 취소하는 로직
        if move in self.drawn_lines:
            self.drawn_lines.remove(move)
            if(self.triangles):
                recent_triangle = self.triangles[-1]
                self.triangles.remove(recent_triangle)
        
            
    def degree_of_point(self, point):
        return sum(1 for line in self.drawn_lines if point in line)


    def check_availability(self, line):
        if line is None:
            return False

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

    def check_triangle_Max(self, line, depth):
        self.get_score = False

        point1 = line[0]
        point2 = line[1]

        point1_connected = []
        point2_connected = []

        for l in self.drawn_lines:
            if l==line: # 자기 자신 제외
                continue
            if point1 in l:
                point1_connected.append(l)
            if point2 in l:
                point2_connected.append(l)

        if point1_connected and point2_connected: # 최소한 2점 모두 다른 선분과 연결되어 있어야 함
            for line1, line2 in product(point1_connected, point2_connected):
                
                # Check if it is a triangle & Skip the triangle has occupied
                triangle = self.organize_points(list(set(chain(*[line, line1, line2]))))
                if len(triangle) != 3 or triangle in self.triangles:
                    continue

                empty = True
                for point in self.whole_points:
                    if point in triangle:
                        continue
                    if bool(Polygon(triangle).intersection(Point(point))):
                        empty = False

                if empty:
                    self.triangles.append(triangle)
                    if(depth == -1):
                        self.FirstTriangle += 1
                    if(depth == 1):
                        self.MaxScore_depth1 += 1
                    elif(depth == 3):
                        self.MaxScore_depth3 += 1

                        
                    
    def check_triangle_Min(self, line, depth):
        self.get_score = False

        point1 = line[0]
        point2 = line[1]

        point1_connected = []
        point2_connected = []

        for l in self.drawn_lines:
            if l==line: # 자기 자신 제외
                continue
            if point1 in l:
                point1_connected.append(l)
            if point2 in l:
                point2_connected.append(l)

        if point1_connected and point2_connected: # 최소한 2점 모두 다른 선분과 연결되어 있어야 함
            for line1, line2 in product(point1_connected, point2_connected):
                
                # Check if it is a triangle & Skip the triangle has occupied
                triangle = self.organize_points(list(set(chain(*[line, line1, line2]))))
                if len(triangle) != 3 or triangle in self.triangles:
                    continue

                empty = True
                for point in self.whole_points:
                    if point in triangle:
                        continue
                    if bool(Polygon(triangle).intersection(Point(point))):
                        empty = False

                if empty:
                    if(depth == 2):
                        self.MinScore_depth2 += 1
                

    def organize_points(self, point_list):
        if point_list is None:
            return None
        point_list.sort(key=lambda x: (x[0], x[1]))
        return point_list
    
