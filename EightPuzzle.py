
import sys, heapq, copy

# returns the formatted input from the input file
def extract_input():
    with open(sys.argv[2], 'r') as file:
      current = 0
      state = [[]]
      for i, num in enumerate(file.read().split()):
        state[current].append(num)
        if (i+1) % 3 == 0 and i != 8:
          state.append([])
          current += 1
      return state

# prints a single state
def print_state(state):
    if state == None:
      print('ERROR: Not found with preset depth of 10.')
      return 0
    for row in state:
      print(f'{row[0]}  {row[1]}  {row[2]}')
    print()

# prints a collection of states with the number of moves and states enqueued
def print_states(path, states_enqueued):
  for state in path:
    print_state(state)
  print(f'Number of moves = {len(path)-1}\nNumber of states enqueued = {states_enqueued}')

# gets the coordiates of a specific value on a board
def get_coords(value, board):
  for i in range(3):
    for j in range(3):
      if board[i][j] == value:
        return i, j

# tile comparison function
def tile_compare(state, goal):
  different = 0
  for i in range(3):
    for j in range(3):
      if state[i][j] != goal[i][j]:
        different += 1
  return different

# euclidean distance heuristic function
def euclidean(state, goal):
  distance = 0
  for i in range(3):
    for j in range(3):
      if state[i][j] != '*':
        x, y = get_coords(state[i][j], goal)
        distance += ((i - x)**2 + (j - y)**2)
  return distance

# solves the puzzle given the algorithm type and starting state
def solvePuzzle(algorithm, starting_state):

    goal_state = [['7', '8', '1'], ['6', '*', '2'], ['5', '4', '3']]
    states_enqueued = [0]
    path = []

    # depth-first search solution to the puzzle
    def dfs(board, depth):
      
      # increment states visited
      states_enqueued[0] += 1
      
      # base cases
      if board == goal_state:
        path.append(copy.deepcopy(board))
        return board
      elif depth == 0:
        return None
  
      # finds the coordinates of the space  
      x, y = get_coords('*', board)

      # recursively calls dfs on each of the positions: left, up, right, down
      for i, j in [[0, -1], [-1, 0], [0, 1], [1, 0]]:
        if 0 <= x + i < 3 and 0 <= y + j < 3:
          board[x][y], board[x+i][y+j] = board[x+i][y+j], board[x][y]
          result = dfs(board, depth - 1)
          board[x][y], board[x+i][y+j] = board[x+i][y+j], board[x][y]
          if result is not None:
            path.append(copy.deepcopy(result))
            return result
      return None

    # iterative deepening search solution to the puzzle
    def ids(board):
      for depth in range(11):
        result = dfs(board, depth)
        if result is not None:
          return result
      return None

    # A* search solution to the puzzle
    def astar(board, heuristic):
      
      # cant use set because lists are mutable and unhashable in python, using list instead
      visited = []
      queue = [(0, board, [copy.deepcopy(board)])]
      states_enqueued = 1
      
      while queue:
        
        # finds cheapest cost from heap
        cost, board, path = heapq.heappop(queue)
        
        # base cases
        if board == goal_state:
          return path, states_enqueued
        if board in visited:
          continue
        
        # adds the current state to the visited
        visited.append(board)

        # finds the coordinates of the spacec
        x, y = get_coords('*', board)
    
        # calculates cost of each continuation and enqueues
        for i, j in [[0, -1], [-1, 0], [0, 1], [1, 0]]:
          if 0 <= x + i < 3 and 0 <= y + j < 3:
            next_board = copy.deepcopy(board)
            next_board[x][y], next_board[x+i][y+j] = next_board[x+i][y+j], next_board[x][y]
            new_cost = cost + 1
            heuristic_cost = new_cost + heuristic(next_board, goal_state)
            if len(path) < 10:
              heapq.heappush(queue, (heuristic_cost, next_board, path + [next_board]))
            states_enqueued += 1
      return [], states_enqueued

    # solves the puzzle using the dfs solution
    if algorithm == 'dfs':
      result = dfs(starting_state, 10)
      if result == None:
        print('ERROR: Not found with preset depth of 10.')
      path.reverse()
      print_states(path, states_enqueued[0])

    # solves the puzzle using the ids solution
    elif algorithm == 'ids':
      result = ids(starting_state)
      if result == None:
        print('ERROR: Not found with preset depth of 10.')
      path.reverse()
      print_states(path, states_enqueued[0])

    # solves the puzzle using the astar solution with a tile comparison hueristic
    elif algorithm == 'astar1':
      path, states_enqueued = astar(starting_state, tile_compare)
      if path == []:
        print('ERROR: Not found with preset depth of 10.')
      print_states(path, states_enqueued)

    # solves the puzzle using the astar solution with a euclidean distance hueristic
    elif algorithm == 'astar2':
      path, states_enqueued = astar(starting_state, euclidean)
      print_states(path, states_enqueued)

    # returns an error if they try to use any other algorithm
    else:
      print('ERROR: That is not a valid algorithm!')


# main thread of execution
if __name__ == '__main__':
    
    start_state = extract_input()
    solvePuzzle(sys.argv[1], start_state)
