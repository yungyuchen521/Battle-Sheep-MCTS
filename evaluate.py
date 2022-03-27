from agent import State

class Evaluate:
    def __init__(self, state: State):
        self.state = state

    # evaluate the curret state for the spcified player
    def evaluate(self, pid):
        # by rankings?
        # by points?
        # others?
        pass

    # return current rankings
    # [ p1 ranking, p2 ranking, p3 ranking, p4 ranking ]
    def _get_rankings(self) -> list:
        pass

    # return current points of the specified player
    def _get_point(self, pid):
        pass