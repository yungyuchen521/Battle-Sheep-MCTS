class Cell:
    def __init__(self, x, y, pid, sheep):
        self.x = x          # position - row
        self.y = y          # position - column
        self.pid = pid      # player id (-1 ~ 4), -1: outside, 0: empty
        self.sheep = sheep  # number of sheep

class Action:
    def __init__(self, cell: Cell, sheep, direction):
        self.cell = cell
        self.sheep = sheep  # number of sheep moving to the new cell
        self.dir = direction      # moving direction 1~6

class State:
    def __init__(self, mapState: list, sheepState: list):
        self.mapState = mapState
        self.sheepState = sheepState

    # return the next state after a given action
    def get_next_state(self, action: Action):
        dest_x, dest_y = self.get_dest_xy(action)
        
        nextState = self.mapState.copy()
        nextSheepState = self.sheepState.copy()
        
        # mapState
        nextState[dest_x][dest_y] = action.cell.pid
        
        #self.mapState = nextState.copy() # not sure if changing?
        
        # sheepState
        orig_x = action.cell.x
        orig_y = action.cell.y
        orig_sheep = action.cell.sheep
        
        nextSheepState[orig_x][orig_y] = orig_sheep - action.sheep
        nextSheepState[dest_x][dest_y] = orig_sheep + action.sheep
        
        #self.sheepState = nextSheepState.copy() # not sure if changing?
        
        return nextState, nextSheepState
    
    # find the destination's x, y
    def get_dest_xy(self, action: Action) -> (int, int):
        now_x = action.cell.x
        now_y = action.cell.y
        while(True):
            # get the moving direction
            if(action.dir == 3):
                dir_x = -1
                dir_y = 0
            elif(action.dir == 4):
                dir_x = 1
                dir_y = 0
            elif(action.dir == 1):
                if(now_y%2 == 0):
                    dir_x = -1
                    dir_y = -1
                else:
                    dir_x = 0
                    dir_y = -1
            elif(action.dir == 2):
                if(now_y%2 == 1):
                    dir_x = 1
                    dir_y = -1
                else:
                    dir_x = 0
                    dir_y = -1
            elif(action.dir == 5):
                if(now_y%2 == 0):
                    dir_x = -1
                    dir_y = 1
                else:
                    dir_x = 0
                    dir_y = 1
            elif(action.dir == 6):
                if(now_y%2 == 1):
                    dir_x = 1
                    dir_y = 1
                else:
                    dir_x = 0
                    dir_y = 1
                
            # check if the direction will move outside the edge, if true, return immediately
            if(now_x + dir_x < 0 or now_x + dir_x >= 12 or now_y + dir_y < 0 or now_y + dir_y >= 12):
                return now_x, now_y
                
            # know that the direction is not at edge, and the direction is movable
            elif(self.mapState[now_x + dir_x][now_y + dir_y] == 0):
                now_x = now_x + dir_x
                now_y = now_y + dir_y
                
            # is not at edge & direction not movable( = reached dest.), return immediately
            else:
                return now_x, now_y
            
    def _get_connected_regions(self) -> dict:
        edge_list = self.get_edge()
        groups = UnionFind()
        
        # initialize the groups
        #g = [[Cell(-1,-1,-1,-1) for j in range(12)] for i in range(12)] # g[0][0] is the group leader cell of (0, 0)
        
        for edge in edge_list:
            groups.join(edge[0], edge[1])
        
        return groups.get_groups()
    
    # return all cell own by any player
    def get_owned_cell(self) -> list:
        cell_list = []
        for i in range(12):
            for j in range(12):
                if(self.state.mapState[i][j] != -1 and self.state.mapState[i][j] != 0):
                    cell = Cell(i, j, self.state.mapState[i][j], self.state.sheepState[i][j])
                    cell_list.append(cell)
        
        return cell_list
    
    # return all edge (neighbor relations) between same pid
    def get_edge(self) -> list:
        edge_list = []
        cell_list = self.get_owned_cell()
        for c1 in cell_list:
            for c2 in cell_list:
                if(c1 != c2 and self._connected(c1, c2) and c1.pid == c2.pid):
                    edge_list.append((c1, c2))
                    
        return edge_list

    # check if 2 cells are connected, note: if c1 = c2, return True
    def _connected(self, c1: Cell, c2: Cell) -> bool:
        # trivial case
        dis_x = c2.x - c1.x
        dix_y = c2.y - c1.y
        if(abs(dis_x) >= 2 or abs(dis_y) >=2):
            return False
        
        # case 1: when c1's y is even
        if(c1.y % 2 == 0):
            neighbor_list = [(-1,-1), (0, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (0, 0)]
            if ((dis_x, dis_y) in neighbor_list == False):
                return False
            else:
                return True
            
        # case 2: when c1's y is odd
        else:
            neighbor_list = [(0,-1), (1, -1), (-1, 0), (1, 0), (0, 1), (1, 1), (0, 0)]
            if ((dis_x, dis_y) in neighbor_list == False):
                return False
            else:
                return True

class Agent:
    def __init__(self, pid, state: State):
        self.pid = pid     # player id
        self.state = state

    # return all valid actions
    def get_valid_actions(self) -> list:
        valid_action_list = []
        
        cell_list = self.get_own_cell()
        for cell in cell_list: 
            for direction in [1, 2, 3, 4, 5, 6]:
                for num_sheep in (range(1,17)):
                    action = Action(cell, num_sheep, direction)
                    if(_valid_action(action)):
                        valid_action_list.append(action)
                        
        return valid_action_list 
        
    # return all cell own by pid
    def get_own_cell(self) -> list:
        cell_list = []
        for i in range(12):
            for j in range(12):
                if(self.state.mapState[i][j] == self.pid):
                    cell = Cell(i, j, self.pid, self.state.sheepState[i][j])
                    cell_list.append(cell)
        
        return cell_list
    # check if an action is valid (only check itself's)
    def _valid_action(self, action: Action) -> bool:
        # check cell
        cell_x = action.cell.x
        cell_y = action.cell.y
        if(self.state.mapState[cell_x][cell_y] != self.pid):
            return False
        
        # check sheep num
        if(action.sheep > self.state.sheepState[cell_x][cell_y] or action.sheep <= 0):
            return False
        
        # check dir
        if(action.dir > 6 or action.dir < 1):
            return False
        elif((cell_x, cell_y) == self.state.get_dest_xy(action.dir)): # being blocked
            return False
            
        return True

    class UnionFind:
    """
    Notes:
        unionfind data structure specialized for finding connected regions.
    Attributes:
        parent (dict): Each group parent
        rank (dict): Each group rank
        groups (dict): Stores the groups and chain of cells
        ignored (list): The neighborhood of board edges has to be ignored
    """

    def __init__(self) -> None:
        """
        Initialize parent and rank as empty dictionaries, we will
        lazily add items as necessary.
        """
        self.parent = {}
        self.rank = {}
        self.groups = {}
        self.ignored = []

    def join(self, x : Cell, y: Cell) -> bool:
        """
        Merge the groups of x and y if they were not already,
        return False if they were already merged, true otherwise
        
        """
        rep_x = self.find(x)
        rep_y = self.find(y)

        if rep_x == rep_y:
            return False
        if self.rank[rep_x] < self.rank[rep_y]:
            self.parent[rep_x] = rep_y

            self.groups[rep_y].extend(self.groups[rep_x])
            del self.groups[rep_x]
        elif self.rank[rep_x] > self.rank[rep_y]:
            self.parent[rep_y] = rep_x

            self.groups[rep_x].extend(self.groups[rep_y])
            del self.groups[rep_y]
        else:
            self.parent[rep_x] = rep_y
            self.rank[rep_y] += 1

            self.groups[rep_y].extend(self.groups[rep_x])
            del self.groups[rep_x]

        return True

    def find(self, x: Cell):
        """
        Get the representative element associated with the set in
        which element x resides. Uses grandparent compression to compression
        the tree on each find operation so that future find operations are faster.
        """
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            if x in self.ignored:
                self.groups[x] = []
            else:
                self.groups[x] = [x]

        px = self.parent[x]
        if x == px:
            return x

        gx = self.parent[px]
        if gx == px:
            return px

        self.parent[x] = gx

        return self.find(gx)

    def connected(self, x, y) -> bool:
        """
        Check if two elements are in the same group.
        Args:
            x (tuple): game board cell
            y (tuple): game board cell
        """
        return self.find(x) == self.find(y)

    def set_ignored_elements(self, ignore):
        """
        Elements in ignored, edges has to be ignored
        """
        self.ignored = ignore

    def get_groups(self) -> dict:
        """
        Returns:
            Groups
        """
        return self.groups
