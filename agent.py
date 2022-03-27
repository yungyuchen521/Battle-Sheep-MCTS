class Cell:
    def __init__(self, x, y, pid, sheep):
        self.x = x          # position - row
        self.y = y          # position - column
        self.pid = pid      # player id (-1 ~ 4)
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

    def _get_connected_regions(self):
        pass

    # check if 2 cells are connected
    def _connected(self, c1: Cell, c2: Cell) -> bool:
        pass

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