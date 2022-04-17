import numpy as np
from meta import GameMeta
from union_find import UnionFind
from copy import deepcopy

class Move:
    def __init__(self, cell: tuple, sheep, dir):
        self.cell = cell    # position (x, y)
        self.sheep = sheep  # #sheep moving to new place
        self.dir = dir      # 1~6

    def getStep(self):
        return [self.cell, self.sheep, self.dir]

class State:
    def __init__(self, mapState: list, sheepState: list, player):
        self.mapState = mapState
        self.sheepState = sheepState
        self.current_player = player # 1 ~ GameMeta.PLAYERS
        self.skip = set()            # no more valid move for player i if i in self.skip

    def play(self, move: Move):
        dest_x, dest_y = self._get_dest(move)
        
        # ============= for debug purposes, delete before submission ============= 
        
        if self.mapState[move.cell[0]][move.cell[1]] != self.current_player:
            raise ValueError("The source cell does not belong to the current player.")

        if self.mapState[dest_x][dest_y] != GameMeta.TOKENS["free"]:
            raise ValueError("The destination cell is unavailable.")

        if self.sheepState[move.cell[0]][move.cell[1]] <= move.sheep:
            raise ValueError("The source cell does not have enough sheep.")

        if self.sheepState[dest_x][dest_y] != 0:
            raise ValueError("The destination cell is already occupied by sheep.")

        # ========================================================================

        self.mapState[dest_x][dest_y] = self.current_player
        self.sheepState[move.cell[0]][move.cell[1]] -= move.sheep
        self.sheepState[dest_x][dest_y] = move.sheep
        self.current_player = self._get_next_player(self.current_player)

    # return the next state after a given Move
    def get_next_state(self, move: Move):
        dest_x, dest_y = self._get_dest(move)
        nextMapState = deepcopy(self.mapState)
        nextSheepState = deepcopy(self.sheepState)
        
        # mapState
        nextMapState[dest_x][dest_y] = self.current_player
        
        #self.mapState = nextState.copy() # not sure if changing?
        
        # sheepState
        orig_x, orig_y = move.cell
        nextSheepState[orig_x][orig_y] -= move.sheep
        nextSheepState[dest_x][dest_y] = move.sheep
        
        #self.sheepState = nextSheepState.copy() # not sure if changing?
        
        return State(nextMapState, nextSheepState, self._get_next_player(self.current_player))
    
    # ************************************************************************
    # ************************** for move selections *************************
    # ************************************************************************

    def get_valid_moves(self) -> list:
        valid_move_list = []
        
        for cell in self._get_own_cells():
            for direction in self._get_valid_directions(cell):
                for num_sheep in self._get_valid_sheep(cell):
                    valid_move_list.append(Move(cell, num_sheep, direction))
        
        return valid_move_list

    @staticmethod
    def _get_next_player(player): 
        return player % GameMeta.PLAYERS + 1 # 1~4

    # find the destination of a Move
    def _get_dest(self, move: Move) -> tuple:
        dest_x, dest_y = move.cell
        pattern_x, pattern_y = self._get_direction_pattern(move.dir)

        while True:
            next_x = dest_x + pattern_x
            next_y = dest_y + pattern_y

            if self._out_of_bound((next_x, next_y)) or self.mapState[next_x][next_y] != GameMeta.TOKENS["free"]:
                break
            
            dest_x = next_x
            dest_y = next_y
        
        # ============= for debug purposes, delete before submission ============= 
        
        if move.cell[0] == dest_x and move.cell[1] == dest_y:
            # The given Move does not move at all
            raise ValueError("This is an invalid move!")

        # ========================================================================

        return (dest_x, dest_y)

    # return all cell owned by the current player
    def _get_own_cells(self) -> list:
        cell_list = []

        for i in range(GameMeta.BOARD_SIZE):
            for j in range(GameMeta.BOARD_SIZE):
                if self.mapState[i][j] == self.current_player:
                    cell_list.append((i, j))
        
        return cell_list

    # return valid direction to move for the given cell
    def _get_valid_directions(self, cell: tuple) -> list:
        valid_directions = []

        for dir in GameMeta.DIRECTIONS:
            pattern = self._get_direction_pattern(cell, dir)
            next_cell = (cell[0] + pattern[0], cell[1] + pattern[1])

            if not self._out_of_bound(next_cell) and self.mapState[next_cell[0]][next_cell[1]] == GameMeta.TOKENS["free"]:
                valid_directions.append(next_cell)
            
        return valid_directions

    @staticmethod
    def _get_direction_pattern(cell, dir) -> tuple:
        _, y = cell

        if dir == 1:
            return ((-1, -1) if y % 2 == 0 else (0, -1))
        elif dir == 2:
            return ((0, -1) if y % 2 == 0 else (1, -1))
        elif dir == 3:
            return (-1, 0)
        elif dir == 4:
            return (1, 0)
        elif dir == 5:
            return ((-1, 1) if y % 2 == 0 else (0, 1))
        elif dir == 6:
            return ((0, 1) if y % 2 == 0 else (1, 1))
        # ============= for debug purposes, delete before submission =============
        else:
            print(f"Unrecognized direction: {dir}.")
            raise ValueError()
        # ========================================================================

    @staticmethod
    def _out_of_bound(cell: tuple) -> bool:
        x, y = cell

        if x < 0 or x >= GameMeta.BOARD_SIZE:
            return True
        elif y < 0 or y >= GameMeta.BOARD_SIZE:
            return True
        else:
            return False

    # return valid number of sheep to move for the given cell
    def _get_valid_sheep(self, cell: tuple) -> list:
        x, y = cell

        min_sheep = 1
        max_sheep = self.sheepState[x][y]-1

        return list(range(min_sheep, max_sheep+1))

    # ************************************************************************
    # ************************ for score calculations ************************
    # ************************************************************************

    def gameover(self) -> bool:
        return len(self.skip) == GameMeta.PLAYERS

    # return points of all players based on rankings & scores
    def get_points(self) -> list:
        # return numpy array
        pass

    # return scores of all players
    def get_scores(self) -> list:
        pass

    def _get_connected_regions(self) -> dict:
        edge_list = self.get_edge()
        groups = UnionFind()
        
        # initialize the groups
        #g = [[Cell(-1,-1,-1,-1) for j in range(12)] for i in range(12)] # g[0][0] is the group leader cell of (0, 0)
        
        for edge in edge_list:
            groups.join(edge[0], edge[1])
        
        return groups.get_groups()
    
    # return all edge (neighbor relations) between same pid
    def get_edge(self) -> list:
        edge_list = []
        cell_list = self._get_own_cells()
        for c1 in cell_list:
            for c2 in cell_list:
                if(c1 != c2 and self._connected(c1, c2) and c1.pid == c2.pid):
                    edge_list.append((c1, c2))
                    
        return edge_list

    # check if 2 cells are connected, note: if c1 = c2, return True
    def _connected(self, c1: tuple, c2: tuple) -> bool:
        # trivial case
        dis_x = c2.x - c1.x
        dis_y = c2.y - c1.y
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
