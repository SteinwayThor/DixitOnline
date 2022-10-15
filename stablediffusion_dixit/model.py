import enum


class GamePhase(enum.Enum):
    WaitingToStart = 0
    ActivePlayerPrompt = 1
    ActivePlayerImageWait = 2
    ActivePlayerGiveClue = 3
    AllPlayersPrompt = 4
    AllPlayersImageWait = 5
    SelectActiveImage = 6
    ShowResults = 7

class GameState:
    def __init__(self):
        self.phase = GamePhase.WaitingToStart
        self.players = []
        self.active_player = None
        self.active_players_image = None
        self.other_players_images = {}
        self.tvs = []

