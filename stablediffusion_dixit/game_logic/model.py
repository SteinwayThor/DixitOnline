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

    def trigger_state(self, state):
        if self.value == 0:
            print('hello')
        else:
            print('wack')

class GameState:
    def __init__(self):
        self.phase = GamePhase.WaitingToStart
        self.players = []
        self.active_player = None
        self.active_players_image = None
        self.other_players_images = {}
        self.tvs = []

        self.phase.trigger_state(self)

    def transition(self):
        next_p = self.phase.value + 1
        if next_p == 8:
            self.phase = GamePhase(1)
        else:
            self.phase = GamePhase(next_p)


    def receive_prompt(self, id, prompt):
        pass

    def receive_proceed_active_player(self, id):
        pass

    def receive_image_finished_generating(self, image_num):
        pass

    def receive_vote(self, id, voted_for):
        pass
    
        
if __name__ == "__main__":
    GameState()