class Cell:
    def __init__(self, x, y, pid, sheep):
        self.x = x          # position - row
        self.y = y          # position - column
        self.pid = pid      # player id (-1 ~ 4), -1: outside, 0: empty
        self.sheep = sheep  # number of sheep

class Action:
    def __init__(self, cell: Cell, sheep, dir):
        self.cell = cell
        self.sheep = sheep  # number of sheep moving to the new cell
        self.dir = dir      # moving direction 1~6

class State:
    def __init__(self, mapState: list, sheepState: list):
        self.mapState = mapState
        self.sheepState = sheepState

    # return the next state after a given action
    def get_next_state(self, action: Action):
        pass
    
    # find the destination's x, y
    def get_dest_xy(self, action: Action) -> int, int:
        now_x = action.cell.x
        now_y = action.cell.y
        while(True):
            # get the moving direction
            if(action.dir == 3):
                dir_x = -1
                dir_y = 0
            else if(action.dir == 4):
                dir_x = 1
                dir_y = 0
            else if(action.dir == 1 and now_x == and now_y ==):
                dir_x = 
                dir_y = 
            else if(action.dir == 2 and now_x == and now_y ==):
                dir_x = 
                dir_y = 
            else if(action.dir == 5 and now_x == and now_y ==):
                dir_x = 
                dir_y = 
            else if(action.dir == 6 and now_x == and now_y ==):
                dir_x = 
                dir_y = 
                
            # check if the direction will move outside the edge, if true, return immediately
            if(now_x + dir_x < 0 or now_x + dir_x >= 12 or now_y + dir_y < 0 or now_y + dir_y >= 12):
                return now_x, now_y
                
            # know that the direction is not at edge, check if the direction is movable
            else if(self.mapState[now_x + dir_x][now_y + dir_y] == 0):
                now_x = now_x + dir_x
                now_y = now_y + dir_y
                
            # is not at edge & direction not movable( = reached dest.), return immediately
            else:
                return now_x, now_y

    def _get_connected_regions(self):
        pass

    # check if 2 cells are connected
    def _connected(self, c1: Cell, c2: Cell) -> bool:
        dis_x = abs(c1.x - c2.x)
        dix_y = abs(c1.y - c2.y)
        if(dis_x >= 2 or dis_y >=2):
            return False
        return True # Note: if c1 = c2, return True

class Agent:
    def __init__(self, pid, state: State):
        self.pid = pid     # player id
        self.state = state

    # return position for InitPos in Sample.py
    def get_init_pos(self):
        pass

    # return action for GetStep in Sample.py
    def choose_action(self) -> Action:
        pass

    # return all valid actions
    def get_valid_actions(self) -> list:
        pass

    # check if an action is valid
    def _valid_action(self, action: Action) -> bool:
        pass
