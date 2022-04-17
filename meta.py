class MCTSMeta:
    EXPLORATION = 0.5
    RAVE_CONST = 300
    RANDOMNESS = 0.5
    POOLRAVE_CAPACITY = 10
    K_CONST = 10
    A_CONST = 0.25
    WARMUP_ROLLOUTS = 7


class GameMeta:
    PLAYERS = 4
    INF = float('inf')

    RANKING_PTS = [5, 3, 2, 1] # points for players with 1st, 2nd, 3rd, 4th highest points
    DIRECTIONS = [1, 2, 3, 4, 5, 6]
    TOKENS = {"wall": -1, "free": 0, "player1": 1, "player2": 2, "player3": 3, "player4": 4}
    
    BOARD_SIZE = 12
    MIN_SHEEP = 1
    MAX_SHEEP = 16