# import constants
# from collections import deque
# import random

# class Maze:
#     def __init__(self, n, m, width, height):
#         self.n = n
#         self.m = m
#         self.matrix = [
#             [constants.WALL_CODE for _ in range(self.m)] for _ in range(self.n)
#         ]
#         self.start = None
#         self.end = None

#         self.width = width
#         self.height = height

#     def generate_maze_dfs(self):
#         (start_x, start_y, end_x, end_y) = self.create_random_entrances()
#         self.start = (start_x, start_y)
#         self.end = (end_x, end_y)
#         self.matrix[start_x][start_y] = constants.EMPTY_CODE
#         self.matrix[end_x][end_y] = constants.EMPTY_CODE
#         # mid_point = (self.n // 2, self.m // 2)
#         stack = [(start_x, start_y)]
#         visited = set((start_x, start_y))
#         while stack:
#             (cx, cy) = stack.pop()
#             if (cx, cy) == (end_x, end_y):
#                 break
#             directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#             random.shuffle(directions)
#             for (dx, dy) in directions:
#                 nx = cx + 2*dx
#                 ny = cy + 2*dy
#                 if 0<= nx < self.n and 0 <= ny < self.m and self.matrix[nx][ny] == constants.WALL_CODE and (nx, ny) not in visited: 
#                     visited.add((nx, ny))
#                     stack.append((nx, ny))
#                     self.matrix[nx][ny] = constants.EMPTY_CODE
#                     self.matrix[cx + dx][cy + dy] = constants.EMPTY_CODE
#             self.ensure_exit_accessible()
        
#     # failed attempt at prims algorithm
#     def is_legal(self, x,y):
#         return 0 < x < self.n - 1 and 0 < y < self.m - 1 

#     def frontier(self, x, y):
#         return [(nx, ny) for nx, ny in [(x-2,y), (x+2, y), (x, y-2), (x, y+2)] if self.is_legal(nx, ny) and self.matrix[nx][ny] == constants.WALL_CODE]

#     def neighbor(self, x, y):
#         return [(nx, ny) for nx, ny in [(x-2,y), (x+2, y), (x, y-2), (x, y+2)] if self.is_legal(nx, ny) and self.matrix[nx][ny] == constants.EMPTY_CODE]
        
#     def between(self, x, y, nx, ny):
#         dx = (nx - x)
#         dy = (ny - y)
#         return (x + dx // 2, y + dy // 2)
    
#     def generate_maze_prims(self):
#         def connect_random_neighbor(x,y):
#             neighbors = self.neighbor(x, y)
#             if neighbors:
#                 xn, yn = random.choice(neighbors)
#                 xb, yb = self.between(x, y, xn, yn)
#                 self.matrix[yb][xb] = constants.EMPTY_CODE

#         def extend(front):
#             visited = set()
#             while front:
#                 xf, yf = random.choice(front)
#                 self.matrix[yf][xf] = constants.EMPTY_CODE
#                 connect_random_neighbor(xf, yf)
#                 front.remove((xf, yf))
#                 visited.add((xf, yf))
#                 new_frontier = [cell for cell in self.frontier(xf, yf) if cell not in visited and cell not in front]
#                 front.extend(new_frontier)
    
#         (start_x, start_y, end_x, end_y) = self.create_random_entrances()
#         self.start = (start_x, start_y)
#         self.end = (end_x, end_y)
#         self.matrix[start_x][start_y] = constants.EMPTY_CODE
#         self.matrix[end_x][end_y] = constants.EMPTY_CODE
#         front = self.frontier(start_x, start_y)
#         extend(front)
        
#     # failed attempt ends here        
#     def ensure_exit_accessible(self):
#         directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#         exit_accessible = any(self.matrix[self.end[0] + dx][self.end[1] + dy] == constants.EMPTY_CODE for dx, dy in directions if 0 <= self.end[0] + dx < self.n and 0 <= self.end[1] + dy < self.m)
#         if not exit_accessible:
#             for dx, dy in directions:
#                 nx, ny = self.end[0] + dx, self.end[1] + dy
#                 if 0 <= nx < self.n and 0 <= ny < self.m:
#                     self.matrix[nx][ny] = constants.EMPTY_CODE  
#                     break  

#     def create_random_entrances(self):
#         (start_x, start_y) = (0,0)
#         (end_x, end_y) = (0,0)
#         while True:
#             start_x = random.randint(0, self.n - 1)
#             start_y = random.randint(0, self.m - 1)
#             end_x = random.randint(0, self.n - 1)
#             end_y = random.randint(0, self.m - 1)
#             if abs(start_x - end_x) + abs(start_y - end_y) > self.n * 2 / 3:
#                 break
#         return (start_x, start_y, end_x, end_y)

#     def dfs_solve(self, canvas):
#         start = self.start
#         (start_x, start_y) = start
#         stack = [(start_x, start_y)]
#         visited = set()
#         parent = {start: None}
#         while stack:
#             (x,y) = stack.pop()
#             visited.add((x,y))
#             if (x,y) == self.end:
#                 path = self.reconstruct_path(parent)
#                 for (i, j) in path:
#                     if (i, j) != self.end:
#                         self.paint_cell(canvas, i, j, constants.TRAVELLED_COLOR, constants.TRAVELLED_COLOR)
#                         yield
#                 return
#             passable_cells = self.get_empty_neighbors(x,y)
#             for (i, j) in passable_cells:
#                 if (i ,j) not in visited and (i, j):
#                     stack.append((i,j))
#                     parent[(i,j)] = (x,y)
    
#     def bfs_solve(self, canvas):
#         start = self.start
#         (start_x, start_y) = start
#         deq = deque([(start_x, start_y)])
#         visited = set()
#         parent = {start: None}
#         while deq:
#             (x,y) = deq.popleft()
#             visited.add((x,y))
#             if (x,y) == self.end:
#                 path = self.reconstruct_path(parent)
#                 for (i, j) in path:
#                     if (i, j) != self.end:
#                         self.paint_cell(canvas, i, j, constants.TRAVELLED_COLOR, constants.TRAVELLED_COLOR)
#                         yield
#                 return
#             passable_cells = self.get_empty_neighbors(x,y)
#             for (i, j) in passable_cells:
#                 if (i ,j) not in visited and (i, j):
#                     deq.append((i,j))
#                     parent[(i,j)] = (x,y)
        

         
#     def reconstruct_path(self, path):
#         reverse_path = []
#         current = self.end
#         while current:
#             reverse_path.append(current)
#             current = path[current]
#         return reverse_path[::-1]

#     def get_empty_neighbors(self, x,y):
#         neighbors = []
#         for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#             nx = x + dx
#             ny = y + dy
#             if 0<= nx < self.n and 0 <= ny < self.m and self.matrix[nx][ny] == constants.EMPTY_CODE:
#                 neighbors.append((nx, ny))
#         return neighbors

#     def paint_cell(self, canvas, i, j, color, outline):
#         cell_width = self.width / self.m
#         cell_height = self.height / self.n
#         x0 = j * cell_width
#         y0 = i * cell_height
#         x1 = (j + 1) * cell_width
#         y1 = (i + 1) * cell_height
#         canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=outline)

#     def animate_iterator(self, canvas, iterator):
#         try:
#             next(iterator)
#             canvas.after(1, self.animate_iterator, canvas, iterator)
#         except StopIteration:
#             pass

#     def draw_grid(self, canvas):
#         for i in range(self.n):
#             for j in range(self.m):
#                 color = None
#                 outline = None 
#                 if (i, j) == self.start:
#                     color = constants.START_COLOR
#                     outline = color
#                 elif (i,j) == self.end:
#                     color = constants.END_COLOR
#                     outline = color
#                 else:
#                     color = constants.EMPTY_COLOR if self.matrix[i][j] == constants.EMPTY_CODE else constants.WALL_COLOR
#                     outline = "black" if self.matrix[i][j] != constants.EMPTY_CODE else "white"
#                 self.paint_cell(canvas, i, j, color, outline)


