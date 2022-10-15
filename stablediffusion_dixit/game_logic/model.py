import enum

from stablediffusion_dixit.image_generation.local_generation.local_image_generator import LocalImageGenerator


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
        elif self.value == 1:
            state.active_player_write_prompt()
        elif self.value == 2:
            state.active_player_wait()
        elif self.value == 3:
            state.active_player_give_clue()
        elif self.value == 4:
            state.non_active_players_give_prompt()
        elif self.value == 5:
            state.non_active_players_wait()
        elif self.value == 6:
            state.non_active_players_vote()
        elif self.value == 7:
            state.show_results()

        exit()

class GameState:
    def __init__(self):
        self.image_generator = LocalImageGenerator()

        self.phase = GamePhase.WaitingToStart
        self.players = []
        self.active_player = None
        self.active_players_image = None
        self.active_players_image_ticket = None
        self.other_players_images = {}
        self.tvs = []

    def receive_prompt(self, id, prompt):
        if self.phase == GamePhase.ActivePlayerPrompt:
            if id == self.active_player:
                self.active_players_image_ticket = self.image_generator.request_generation(prompt, callback=self.receive_image_finished_generating)
                self.phase = GamePhase.ActivePlayerImageWait

                # TODO Send messages to everyone to show waiting screen

        elif self.phase == GamePhase.AllPlayersPrompt:
            pass

    def receive_proceed_active_player(self, id):
        pass

    def receive_image_finished_generating(self, image_num, image_path, anim_path):
        if self.phase == GamePhase.ActivePlayerImageWait:
            if self.active_players_image_ticket == image_num:
                self.active_players_image = image_path
                # TODO Send message to active player to give clue
                self.phase = GamePhase.ActivePlayerGiveClue
                self.phase.trigger_state()
        pass

    def receive_vote(self, id, voted_for):
        pass

    def active_player_write_prompt():
        pass

    def active_player_wait():
        pass

    def active_player_give_clue():
        pass

    def non_active_players_give_prompt():
        pass

    def non_active_players_wait():
        pass

    def non_active_players_vote():
        pass

    def show_results():
        pass
    
        
if __name__ == "__main__":
    GameState()