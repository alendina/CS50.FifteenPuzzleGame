#import fifteen_puzzle_interface
from copy import deepcopy

START_BOARD = [
    [1, 2, 3, 4],
    [5, 0, 6, 11],
    [9, 15, 8, 7],
    [13, 10, 14,12]
]

FINISH_BOARD = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

class Node():
    def __init__(self, state_board, parent_board, action_from_parent):
        self.state = state_board
        self.parent = parent_board
        self.action = action_from_parent

    def get_height(self):
        return len(self.state)
    
    def get_width(self):
        return len(self.state[0])

    def get_empty_cell(self):   
        for i in range(self.get_height()):
            for j in range(self.get_width()):
                if self.state[i][j] == 0:
                    return (i,j)
        raise Exception("Empty cell not found")   

    def get_neighbors(self):
        neighbors = []
        empty_cell = self.get_empty_cell()
        i = empty_cell[0]
        j = empty_cell[1]

        # Check cell Down
        if i-1 >= 0:
            new_state = deepcopy(self.state)
            new_state[i][j] = new_state[i-1][j]
            new_state[i-1][j] = 0
            new_node = Node(state_board=new_state, parent_board=self, action_from_parent="Down")
            neighbors.append(new_node)
        
        # Check cell Up   
        if i+1 < self.get_height():
            new_state = deepcopy(self.state)
            new_state[i][j] = new_state[i+1][j]
            new_state[i+1][j] = 0
            new_node = Node(state_board=new_state, parent_board=self, action_from_parent="Up")
            neighbors.append(new_node)

        # Check cell Right
        if j-1 >= 0:
            new_state = deepcopy(self.state)
            new_state[i][j] = new_state[i][j-1]
            new_state[i][j-1] = 0
            new_node = Node(state_board=new_state, parent_board=self, action_from_parent="Right")
            neighbors.append(new_node)

        # Check cell Left
        if j+1 < self.get_width():
            new_state = deepcopy(self.state)
            new_state[i][j] = new_state[i][j+1]
            new_state[i][j+1] = 0
            new_node = Node(state_board=new_state, parent_board=self, action_from_parent="Left")
            neighbors.append(new_node)

        '''
        print("Neighbors:")
        for i in neighbors:
              print(i.action)
              print(*i.state, sep="\n")
        '''
              
        return neighbors
   
class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class SortQueueFrontier(QueueFrontier):

    def add(self, node):
        self.frontier.append(node)
        self.frontier.sort(key=lambda x: x.cost)


class Board():
    def __init__(self):
        self.width = 3
        self.height = 2
        self.start = START_BOARD
        self.state = START_BOARD
        self.finish = FINISH_BOARD
        self.empty_cell = self.get_empty_cell()
        self.explored = []
        self.way = []
        self.method = "BFS"

    def get_empty_cell(self):   
        for i in range(self.height):
            for j in range(self.width):
                if self.state[i][j] == 0:
                    return (i,j)
        raise Exception("Empty cell not found")   
    
    def contains_in_explored(self, state):
        return any(node.state == state for node in self.explored)

    def move(self, action):
        i = self.empty_cell[0]
        j = self.empty_cell[1]
        if action == "Up":
            self.state[i][j] = self.state[i-1][j]
            self.state[i-1][j] = 0
            self.empty_cell = (i-1, j)
        elif action == "Down":
            self.state[i][j] = self.state[i+1][j]
            self.state[i+1][j] = 0
            self.empty_cell = (i+1, j)
        elif action == "Left":
            self.state[i][j] = self.state[i][j-1]
            self.state[i][j-1] = 0
            self.empty_cell = (i, j-1)
        elif action == "Right":
            self.state[i][j] = self.state[i][j+1]
            self.state[i][j+1] = 0
            self.empty_cell = (i, j+1)
        else:
            raise Exception("Invalid action")
        return self.state        
    
    def terminal(self):
        return self.state == self.finish

    def search(self):
        start_node = Node(state_board=self.state, parent_board=None, action_from_parent=None)
        #frontier = StackFrontier() # Deep first search
        frontier = QueueFrontier() # Breadth first search
        frontier.add(start_node)
        
        while True:
            if frontier.empty():
                print(f"\nSOLUTION ({self.method}): No solution")
                print(f"Explored: {len(self.explored)}")
                return "No solution"
            
            print("\nLen of Frontier:" , len(frontier.frontier))
            node = frontier.remove()
            #print("Node:")
            #print(*node.state, sep="\n")
            #print()
            
            if node.state == self.finish:
                actions = []
                states = []
                while node.parent is not None:
                    actions.append(node.action)
                    states.append(node.state)
                    node = node.parent
                    
                actions.reverse()
                states.reverse()
                self.way = states

                
                print(f"\nSOLUTION ({self.method}):")
                print(f"Way: {len(actions)}")
                print(f"Explored: {len(self.explored)}")
                print(f"Actions: {actions}")
                print("\nWay:")
                print(*self.start, sep="\n")
                for i in range(len(actions)):
                    print(actions[i])
                    print()
                    print(*states[i], sep="\n")
                    print()
                

                return actions, states

            self.explored.append(node)
            
            for node in node.get_neighbors():
                if (frontier.contains_state(node.state) == False) and (self.contains_in_explored(node.state) == False):
                    frontier.add(node)
            

            #print(f"Frontier: {[node_f.state for node_f in frontier.frontier]}")
            #print(f"Explored: {self.explored}")
        


def main():
    board = Board()
    print()
    print(*board.state, sep="\n")
    print()
    board.search()
    
    
if __name__ == "__main__": 
    main()