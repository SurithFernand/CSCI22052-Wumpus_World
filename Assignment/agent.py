# class LogicAgent:
#     def __init__(self, environment):
#         self.env = environment
#         self.visited = set()
#         self.safe = set()
#         self.frontier = [(0, 0)]
#         self.path = [(0, 0)]
#         self.directions = ["up", "right", "down", "left"]
#         self.came_from = {}  # child -> parent
#
#     def perceive_and_update(self):
#         percepts = self.env.percepts
#         x, y = self.env.agent_pos
#         self.visited.add((x, y))
#         self.safe.add((x, y))
#
#         # If no danger, mark all adjacent cells as safe
#         if not percepts['breeze'] and not percepts['stench']:
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
#                     self.safe.add((nx, ny))
#                     if (nx, ny) not in self.visited:
#                         self.frontier.append((nx, ny))
#
#
#     def make_move(self):
#         self.perceive_and_update()
#
#         x, y = self.env.agent_pos
#         candidates = [cell for cell in self.frontier if cell not in self.visited]
#
#         # If no safe unvisited moves, take a risk
#         target = None
#         for cell in candidates:
#             if cell in self.safe:
#                 target = cell
#                 break
#         if not target and candidates:
#             target = candidates[0]  # Risky move
#
#         if target:
#             self.try_move_to(target)
#         else:
#             # Try adjacent unexplored cells
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
#                     if (nx, ny) not in self.visited:
#                         self.try_move_to((nx, ny))
#                         return
#
#     def backtrack_to_start(self):
#         current = self.env.agent_pos
#         path_back = []
#
#         # Follow the path back to (0, 0)
#         while current != (0, 0):
#             prev = self.came_from.get(current)
#             if not prev:
#                 print("No path to start found!")
#                 return
#             path_back.append(prev)
#             current = prev
#
#         path_back.reverse()  # To go from current position → (0,0)
#
#         for cell in path_back:
#             self.try_move_to(cell)
#
#     # def try_move_to(self, target):
#     #     current_x, current_y = self.env.agent_pos
#     #     target_x, target_y = target
#     #
#     #     if current_x != target_x:
#     #         direction = "down" if target_x > current_x else "up"
#     #     else:
#     #         direction = "right" if target_y > current_y else "left"
#     #
#     #     self.face_direction(direction)
#     #     moved = self.env.move_forward()
#     #     if moved:
#     #         self.path.append(self.env.agent_pos)
#     #
#     #         # Grab gold if available
#     #         if self.env.percepts["glitter"]:
#     #             self.env.grab_gold()
#     def try_move_to(self, target):
#         current_x, current_y = self.env.agent_pos
#         target_x, target_y = target
#
#         if current_x != target_x:
#             direction = "down" if target_x > current_x else "up"
#         else:
#             direction = "right" if target_y > current_y else "left"
#
#         self.face_direction(direction)
#         moved = self.env.move_forward()
#         if moved:
#             self.path.append(self.env.agent_pos)
#             self.came_from[self.env.agent_pos] = (current_x, current_y)
#
#             # Grab gold if available
#             if self.env.percepts["glitter"]:
#                 self.env.grab_gold()
#                 print("Gold grabbed!")
#                 self.backtrack_to_start()
#
#     def face_direction(self, desired_direction):
#         # Rotate right until facing the correct direction
#         while self.env.agent_dir != desired_direction:
#             self.env.turn_right()







# from collections import deque
#
#
# class LogicAgent:
#     def __init__(self, environment):
#         self.env = environment
#         self.visited = set()
#         self.safe = set()
#         self.frontier = [(0, 0)]
#         self.path = [(0, 0)]  # current path to allow backtracking
#         self.returning = False
#         self.return_path = []
#         self.dead_ends = set()  # tracks known dead-end cells
#         # # trick to move first
#         # self.safe.add((0, 1))
#         # self.safe.add((1, 0))
#         # self.frontier += [(0, 1), (1, 0)]
#
#     def find_shortest_safe_path(self, start, goal):
#         queue = deque([[start]])
#         visited = set()
#
#         while queue:
#             path = queue.popleft()
#             current = path[-1]
#             if current == goal:
#                 return path
#             if current in visited:
#                 continue
#             visited.add(current)
#
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 nx, ny = current[0] + dx, current[1] + dy
#                 neighbor = (nx, ny)
#                 if (0 <= nx < self.env.grid_size and
#                         0 <= ny < self.env.grid_size and
#                         neighbor in self.safe):
#                     queue.append(path + [neighbor])
#         return []
#
#     def perceive_and_update(self):
#         percepts = self.env.percepts
#         x, y = self.env.agent_pos
#         self.visited.add((x, y))
#         self.safe.add((x, y))
#         self.frontier = [cell for cell in self.frontier if cell not in self.visited and cell not in self.dead_ends]
#
#         if not percepts['breeze'] and not percepts['stench']:
#             for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
#                     if (nx, ny) not in self.visited:
#                         self.safe.add((nx, ny))
#                         self.frontier.append((nx, ny))
#
#     def perceive_and_update(self):
#         percepts = self.env.percepts
#         x, y = self.env.agent_pos
#         self.visited.add((x, y))
#         self.safe.add((x, y))
#
#         unexplored_neighbors = 0
#
#         if not percepts['breeze'] and not percepts['stench']:
#             for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#                 nx, ny = x + dx, y + dy
#                 if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
#                     neighbor = (nx, ny)
#                     if neighbor not in self.visited:
#                         unexplored_neighbors += 1
#                         self.safe.add(neighbor)
#                         self.frontier.append(neighbor)
#
#         # If no unexplored neighbors from this cell, mark it as a dead end
#         if unexplored_neighbors == 0:
#             self.dead_ends.add((x, y))
#
#         # Clean frontier
#         self.frontier = [cell for cell in self.frontier if cell not in self.visited and cell not in self.dead_ends]
#
#
#     def make_move(self):
#         self.perceive_and_update()
#         x, y = self.env.agent_pos
#
#         #  Grab gold if here
#         if self.env.percepts.get("glitter"):
#             self.env.grab_gold()
#             self.env.percepts = self.env.get_percepts()
#             print("Gold grabbed at", self.env.agent_pos)
#             self.returning = True
#
#         #  If returning, backtrack to (0,0)
#         if self.returning:
#             if (x, y) == (0, 0):
#                 print("Returned to start with gold!")
#                 return
#
#             if not hasattr(self, 'return_path') or not self.return_path:
#                 # Find shortest safe path home
#                 self.return_path = self.find_shortest_safe_path(self.env.agent_pos, (0, 0))[1:]  # skip current
#
#             if self.return_path:
#                 next_step = self.return_path.pop(0)
#                 self.move_to(next_step)
#             return
#
#         #  Explore safe adjacent unvisited cell
#         # for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#         #     nx, ny = x + dx, y + dy
#         #     if (nx, ny) in self.safe and (nx, ny) not in self.visited:
#         #         self.move_to((nx, ny))
#         #         return
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             nx, ny = x + dx, y + dy
#             if (nx, ny) in self.safe and (nx, ny) not in self.visited and (nx, ny) not in self.dead_ends:
#                 self.move_to((nx, ny))
#                 return
#
#         #  Backtrack (safe)
#         # if len(self.path) > 1:
#         #     self.path.pop()
#         #     back = self.path[-1]
#         #     self.move_to(back)
#         #     return
#         if len(self.path) > 1:
#             self.dead_ends.add(self.env.agent_pos)  # Mark current as dead-end
#             self.path.pop()
#             back = self.path[-1]
#             self.move_to(back)
#             return
#
#         #  Take a risk if truly stuck
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             nx, ny = x + dx, y + dy
#             if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
#                 if (nx, ny) not in self.visited:
#                     print("No safe options, taking a risk:", (nx, ny))
#                     self.move_to((nx, ny))
#                     return
#
#     def move_to(self, target):
#         tx, ty = target
#         ax, ay = self.env.agent_pos
#
#         if tx < ax:
#             self.env.agent_dir = "up"
#         elif tx > ax:
#             self.env.agent_dir = "down"
#         elif ty < ay:
#             self.env.agent_dir = "left"
#         elif ty > ay:
#             self.env.agent_dir = "right"
#
#         moved = self.env.move_forward()
#         if moved and not self.returning:
#             self.path.append(self.env.agent_pos)
#         self.env.percepts = self.env.get_percepts()






from collections import deque
import random

class LogicAgent:
    def __init__(self, environment):
        self.env = environment
        self.visited = set()
        self.safe = set()
        self.frontier = [(0, 0)]
        self.path = [(0, 0)]  # Current path for backtracking
        self.returning = False
        self.return_path = []
        self.dead_ends = set()  # Tracks dead-end cells
        self.backtrack_count = {}  # Tracks backtracking frequency
        self.wumpus_killed = False  # Tracks if Wumpus is killed
        self.recent_positions = []  # Tracks recent positions for loop detection

    def find_shortest_safe_path(self, start, goal):
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            current = path[-1]
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if (0 <= nx < self.env.grid_size and
                        0 <= ny < self.env.grid_size and
                        neighbor in self.safe):
                    queue.append(path + [neighbor])
        return []

    def find_path_ignore_safety(self, start, goal):
        """Find path ignoring safety when no safe path exists"""
        queue = deque([[start]])
        visited = set()

        while queue:
            path = queue.popleft()
            current = path[-1]
            if current == goal:
                return path
            if current in visited:
                continue
            visited.add(current)

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = current[0] + dx, current[1] + dy
                neighbor = (nx, ny)
                if (0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size):
                    queue.append(path + [neighbor])
        return []

    def perceive_and_update(self):
        percepts = self.env.percepts
        x, y = self.env.agent_pos
        self.visited.add((x, y))
        self.safe.add((x, y))

        # Special handling for starting position
        if (x, y) == (0, 0):
            # Always consider at least one adjacent cell as safe to prevent deadlock
            if len(self.visited) == 1:  # Only at the very first move
                self.safe.update([(0, 1), (1, 0)])
                self.frontier.extend([(0, 1), (1, 0)])

        unexplored_neighbors = 0

        if not percepts['breeze'] and not percepts['stench']:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size:
                    neighbor = (nx, ny)
                    if neighbor not in self.visited:
                        unexplored_neighbors += 1
                        self.safe.add(neighbor)
                        self.frontier.append(neighbor)

        # If no unexplored neighbors from this cell, mark it as a dead end
        if unexplored_neighbors == 0 and (x, y) != (0, 0):
            self.dead_ends.add((x, y))

        # Clean frontier
        self.frontier = [cell for cell in self.frontier if cell not in self.visited and cell not in self.dead_ends]

    def reset_stench_cells(self):
        for i in range(self.env.grid_size):
            for j in range(self.env.grid_size):
                if (i, j) in self.visited and self.env.world[i][j]['wumpus']:
                    self.visited.remove((i, j))
                    if (i, j) not in self.frontier:
                        self.frontier.append((i, j))

    def make_move(self):
        # If stuck at start with no safe moves, take a calculated risk
        if self.env.agent_pos == (0, 0) and not any(cell in self.safe for cell in [(0, 1), (1, 0)]):
            print("Forced to take risk from start position")
            self.move_to((0, 1))  # Prefer moving right first
            return

        self.perceive_and_update()
        x, y = self.env.agent_pos

        # Grab gold if here
        if self.env.percepts.get("glitter"):
            self.env.grab_gold()
            self.env.percepts = self.env.get_percepts()
            print("Gold grabbed at", self.env.agent_pos)
            self.returning = True

        # If returning, backtrack to (0,0)
        if self.returning:
            if (x, y) == (0, 0):
                print("Returned to start with gold!")
                return

            if not hasattr(self, 'return_path') or not self.return_path:
                # Find shortest safe path home
                self.return_path = self.find_shortest_safe_path(self.env.agent_pos, (0, 0))
                if not self.return_path:  # If no safe path found
                    print("No safe path home, taking risks")
                    # Try to find any path home, even through unsafe cells
                    self.return_path = self.find_path_ignore_safety(self.env.agent_pos, (0, 0))[1:]
                else:
                    self.return_path = self.return_path[1:]  # skip current

            if self.return_path:
                next_step = self.return_path.pop(0)
                self.move_to(next_step)
            return

        # Explore safe adjacent unvisited cell
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size and
                    (nx, ny) in self.safe and (nx, ny) not in self.visited and
                    (nx, ny) not in self.dead_ends):
                self.move_to((nx, ny))
                return

        # Backtrack (safe)
        if len(self.path) > 1:
            self.dead_ends.add(self.env.agent_pos)  # Mark current as dead-end
            self.path.pop()
            back = self.path[-1]
            if back in self.safe:  # Only backtrack to safe cells
                self.move_to(back)
                return

        # Take a risk if truly stuck (only to unvisited cells)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < self.env.grid_size and 0 <= ny < self.env.grid_size and
                    (nx, ny) not in self.visited):
                print("No safe options, taking a risk:", (nx, ny))
                self.move_to((nx, ny))
                return

    def move_to(self, target):
        tx, ty = target
        ax, ay = self.env.agent_pos

        if tx < ax:
            self.env.agent_dir = "up"
        elif tx > ax:
            self.env.agent_dir = "down"
        elif ty < ay:
            self.env.agent_dir = "left"
        elif ty > ay:
            self.env.agent_dir = "right"

        moved = self.env.move_forward()
        if moved and not self.returning:
            self.path.append(self.env.agent_pos)
        self.env.percepts = self.env.get_percepts()