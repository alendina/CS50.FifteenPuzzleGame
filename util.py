import os


BASIC_PART_FILENAME = "G"
LABYRINTH_SYMBOLS = {
    "wall"  : "#",
    "tunnel": " ",
    "start" : "A",
    "finish": "B",
    "pass_finish"  : "*",
    "pass_all"     : "."
}
LABYRINTH_HTML_COLOR = {
    "wall"  : "rgb(182, 180, 180)", 
    "tunnel": "White", 
    "start" : "rgb(160, 160, 231)", 
    "finish": "rgb(212, 159, 159)", 
    "pass_finish"  : "rgb(149, 197, 149)",
    "pass_all"     : "rgb(243, 233, 156)"
}


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    def get_neighbors(self, labyrinth):
        neighbors = []
        # Check cell Up
        if self.state[0]-1 >= 0 and labyrinth.labyrinth[self.state[0]-1][self.state[1]] != labyrinth.symbols["wall"]:
            new_node = Node(state=(self.state[0]-1, self.state[1]), parent=self, action="Up")
            neighbors.append(new_node)
        # Check cell Down
        if self.state[0]+1 <= labyrinth.height-1 and labyrinth.labyrinth[self.state[0]+1][self.state[1]] != labyrinth.symbols["wall"]:
            new_node = Node(state=(self.state[0]+1, self.state[1]), parent=self, action="Down")
            neighbors.append(new_node)
        # Check cell Left
        if self.state[1]-1 >= 0 and labyrinth.labyrinth[self.state[0]][self.state[1]-1] != labyrinth.symbols["wall"]:
            new_node = Node(state=(self.state[0], self.state[1]-1), parent=self, action="Left")
            neighbors.append(new_node)
        # Check cell Right
        if self.state[1]+1 <= labyrinth.width - 1 and labyrinth.labyrinth[self.state[0]][self.state[1]+1] != labyrinth.symbols["wall"]:
            new_node = Node(state=(self.state[0], self.state[1]+1), parent=self, action="Right")
            neighbors.append(new_node)
        
        return neighbors


class NodeA(Node):
    def __init__(self, state, parent, action, heuristic=0):
        super().__init__(state, parent, action)
        self.way_length = self.set_way_length()
        self.cost = self.set_cost(heuristic)
    
    def set_way_length(self):
        if self.parent is None:
            self.way_length = 0
        else:   
            self.way_length = self.parent.way_length + 1
        return self.way_length
    
    def get_way_length(self):
        return self.way_length

    def get_cost(self):
        return self.cost
    
    def set_cost(self, heuristic):
        if self.parent is None:
            self.cost = 0
        else:   
            self.cost = self.parent.cost + 1
        return self.way_length + heuristic
    
    def get_neighbors(self, labyrinth):
        neighbors = []
        # Check cell Up
        if self.state[0]-1 >= 0 and labyrinth.labyrinth[self.state[0]-1][self.state[1]] != labyrinth.symbols["wall"]:
            new_node = NodeA(state=(self.state[0]-1, self.state[1]), parent=self, action="Up", heuristic=labyrinth.heuristics[self.state[0]-1][self.state[1]])
            neighbors.append(new_node)
        # Check cell Down
        if self.state[0]+1 <= labyrinth.height-1 and labyrinth.labyrinth[self.state[0]+1][self.state[1]] != labyrinth.symbols["wall"]:
            new_node = NodeA(state=(self.state[0]+1, self.state[1]), parent=self, action="Down", heuristic=labyrinth.heuristics[self.state[0]+1][self.state[1]])
            neighbors.append(new_node)
        # Check cell Left
        if self.state[1]-1 >= 0 and labyrinth.labyrinth[self.state[0]][self.state[1]-1] != labyrinth.symbols["wall"]:
            new_node = NodeA(state=(self.state[0], self.state[1]-1), parent=self, action="Left", heuristic=labyrinth.heuristics[self.state[0]][self.state[1]-1])
            neighbors.append(new_node)
        # Check cell Right
        if self.state[1]+1 <= labyrinth.width - 1 and labyrinth.labyrinth[self.state[0]][self.state[1]+1] != labyrinth.symbols["wall"]:
            new_node = NodeA(state=(self.state[0], self.state[1]+1), parent=self, action="Right", heuristic=labyrinth.heuristics[self.state[0]][self.state[1]+1])
            neighbors.append(new_node)
    
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


class Labyrinth():
    def __init__(self,filename):
        self.width = 10
        self.height = 10
        self.symbols = LABYRINTH_SYMBOLS
        self.labyrinth = []
        self.start = (0,0)
        self.finish = None
        self.explored = []
        self.way = []
        self.method = None
        self.filename = filename
        #self.filename = os.path.join(os.path.dirname(__file__), filename)
 
    def read_from_txt_file(self):
        if self.filename is None:
            print(f"\nText file {self.filename} does not provided")
            raise Exception("Filename is not provided")

        if not os.path.exists(self.filename):
            print(f"\nText file {self.filename} does not exist.")
            raise Exception("File does not exist")
        
        #Clean the labyrinth from previous passes
        with open(self.filename, "r+") as file:
            content = file.read()
            content = content.replace(self.symbols["pass_all"], self.symbols["tunnel"])
            content = content.replace(self.symbols["pass_finish"], self.symbols["tunnel"])
            file.seek(0)
            file.write(content)
            #file.truncate()

        # Read the labyrinth from the file
        with open(self.filename, "r") as file:
            self.labyrinth = [list(line.strip("\n")) for line in file]

        self.width = len(self.labyrinth[0])
        self.height = len(self.labyrinth)
        
        # Find start and finish positions
        for y, row in enumerate(self.labyrinth):
            for x, symbol in enumerate(row):
                if symbol == self.symbols["start"]:
                    self.start = (y, x)
                elif symbol == self.symbols["finish"]:
                    self.finish = (y, x)

        print(f"\nText file {self.filename} read successfully.")
        return self.labyrinth
    
    def search(self):
        pass

    def write_to_txt_file(self):
        if self.filename is None:
            print(f"\nText file {self.filename} does not provided")
            raise Exception("Filename is not provided")
        '''
        if not os.path.exists(self.filename):
            print(f"\nText file {self.filename} does not exist.")
            raise Exception("File does not exist")
            #self.filename = generate_next_txt_filename(basic_filename=BASIC_PART_FILENAME)
        '''
        if self.labyrinth is None:
            raise Exception("Labyrinth is not generated")
        else:
            with open(self.filename, "w") as new_file:
                for row in self.labyrinth:
                    new_file.write("".join(row) + "\n")
            print(f"\nText file {self.filename} wrote successfully.")


    def write_to_html(self, clean=False, numbers=None):

        html_filename = self.filename.replace(".txt", ".html")

        if self.labyrinth is None:
            raise Exception("Labyrinth is not generated")
        else:
            html_content = "<html>\n<body>\n<table style='border: 1px solid grey; border-spacing: 0px;'>\n"
            html_content += f"<p>{self.method} (Way: {len(self.way)} , Explored: {len(self.explored)})</p>\n"
            
            for y in range(self.height):
                html_content += "<tr>\n"
                for x in range(self.width):
                    symbol = self.labyrinth[y][x]
                    if symbol == self.symbols["start"]:
                        current_color = LABYRINTH_HTML_COLOR["start"]
                        text = self.symbols["start"]
                    elif symbol == self.symbols["finish"]:
                        current_color = LABYRINTH_HTML_COLOR["finish"]
                        text = self.symbols["finish"]
                    elif symbol == self.symbols["wall"]:
                        current_color = LABYRINTH_HTML_COLOR["wall"]
                        text = ""
                    elif symbol == self.symbols["tunnel"]:
                        current_color = LABYRINTH_HTML_COLOR["tunnel"]
                        if numbers is not None:
                            text = numbers[y][x]
                        else:
                            text = ""
                    elif symbol == self.symbols["pass_finish"]:
                        current_color = LABYRINTH_HTML_COLOR["pass_finish"]
                        if numbers is not None:
                            text = numbers[y][x]
                        else:
                            text = self.symbols["pass_finish"]
                    elif symbol == self.symbols["pass_all"]:
                        current_color = LABYRINTH_HTML_COLOR["pass_all"]
                        if numbers is not None:
                            text = numbers[y][x]
                        else:
                            text = ""
                            #text = self.symbols["pass_all"]
                    html_content += f"<td style='background-color: {current_color}; border: 1px solid rgb(240, 241, 242); width: 20px; height: 20px; text-align: center; vertical-align: middle;'>{text}</td>\n"
                html_content += "</tr>\n"
            html_content += "</table>\n</body>\n</html>"
        
        if clean == True or not os.path.exists(html_filename):
            with open(html_filename, "w") as html_file:
                html_file.write("")
        
        with open(html_filename, "r+") as html_file:
            content = html_file.read()
            if content == "":
                html_file.write(html_content)
            else:
                content = content.replace("</body>\n</html>", "")
                html_file.seek(0)
                html_file.write(content)
                html_file.truncate()
                html_file.write("<br>")
                html_file.write(html_content)
                html_file.write("</body>\n</html>")

        print(f"\nHTML file {html_filename} created successfully\n")   

def generate_next_txt_filename(basic_filename="G"):
        folder = os.getcwd()
        files = os.listdir(folder)
        labyrinth_files = [file for file in files if file.startswith(basic_filename) and file.endswith(".txt")]
        numbers = [int(file.strip(basic_filename).strip(".txt")) for file in labyrinth_files]
        next_number = max(numbers) + 1 if numbers else 1
        new_filename = f"{basic_filename}{next_number:02}.txt"
        new_filepath = os.path.join(folder, new_filename)
        return new_filepath