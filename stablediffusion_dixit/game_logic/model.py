import enum
import random

from stablediffusion_dixit.image_generation.local_generation.local_image_generator import LocalImageGenerator
from flask_socketio import SocketIO, emit

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
            pass
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

        print("reached strange state")
        exit()

class GameState:
    def __init__(self):
        self.image_generator = LocalImageGenerator()

        self.phase = GamePhase.WaitingToStart
        self.players = []  # Player object
        self.active_player = 0  # Index
        self.active_players_image = None
        self.active_players_image_ticket = None
        self.other_players_images = {}
        self.other_players_image_tickets = {}
        self.card_order = None
        self.tvs = []
        self.votes = {}

        self.anims_this_round = []
        self.anims_prev_rounds = []

        self.phase.trigger_state(self)

    def get_random_animation(self) -> str:
        premade_animations = [f"premade_animations/{n}.gif" for n in range(2)]
        if len(self.anims_prev_rounds) == 0:
            return random.choice(premade_animations)
        else:
            return random.choice(self.anims_prev_rounds)

    def receive_prompt(self, id, prompt):
        if self.phase == GamePhase.ActivePlayerPrompt:
            if id == self.active_player:
                self.active_players_image_ticket = self.image_generator.request_generation(prompt, callback=self.receive_image_finished_generating)
                self.phase = GamePhase.ActivePlayerImageWait

                # TODO Send messages to everyone to show waiting screen

        elif self.phase == GamePhase.AllPlayersPrompt:
            pass

    def receive_proceed_active_player(self, sid):
        active_player_sid = self.players[self.active_player]
        
        if sid == active_player_sid:
            self.phase.trigger_state(self)
        



    def receive_image_finished_generating(self, image_num, image_path, anim_path):
        self.anims_this_round.append(anim_path)

        if self.phase == GamePhase.ActivePlayerImageWait:
            if self.active_players_image_ticket == image_num:
                self.active_players_image = image_path
                self.phase = GamePhase.ActivePlayerGiveClue
                self.phase.trigger_state(self)
        elif self.phase == GamePhase.AllPlayersImageWait:
            for player_id, player_image_ticket in self.other_players_image_tickets.items():
                if player_image_ticket == image_num:
                    self.other_players_images[player_id] = image_path

            if len(self.other_players_images) == len(self.other_players_image_tickets):
                self.phase = GamePhase.SelectActiveImage
                self.phase.trigger_state(self)

    def receive_vote(self, sid, voted_for):
        #Find the player who voted
        current_player = None
        for player in self.players:
            if player.id == sid:
                current_player = player
        #Set the votes dict
        self.votes[current_player] = voted_for
        if len(self.votes) == len(self.players):
            self.phase = GamePhase.ShowResults
            self.score_votes()
            self.phase.trigger_state(self)
    
    def score_votes(self):
        #Initialize tallies, keeps track of votes for each player
        tallies = {player.sid : 0 for player in self.players}

        #Increment tallies
        for vote in self.votes.values():
            tallies[vote] += 1
        active_sid = self.players[self.active_player]   # Get the active Players Sid

        #If No one voted for the active player
        if tallies[active_sid] == 0:
            for player in self.players:
                if not player == self.players[self.active_player]:
                    player.score += 2

        #If everyone voted for the active player
        elif tallies[active_sid] == len(self.players) - 1:
            for player in self.players:
               player.score += 2 + tallies[player.sid]

        #If at least one person voted for the active player
        else:
            for player in self.players:
                if player == self.players[self.active_player]:
                    self.players[self.active_player].score += 3
                else:
                    if self.votes[player.sid] == active_sid:
                        self.score += 3
                    self.score += tallies[player.sid]
    

    def get_active_player(self):
        for player in self.players:
            if player.sid == self.active_player:
                return player

    def active_player_write_prompt(self):
        active_player = self.players[self.active_player]

        emit("write_prompt", to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("display_waiting_screen", {
                    "text": f"Wait for {active_player.nickname} to enter a image prompt",
                    "image": self.get_random_animation()
                }, to=player.sid)

    def active_player_wait(self):
        pass


    def active_player_give_clue(self):
        active_player = self.players[self.active_player]

        emit("display_active_player_ok", {
            "image": self.active_players_image
        }, to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("display_waiting_screen", {
                    "text": f"Listen for {active_player.nickname}'s clue!"
                }, to=player.sid)

    def non_active_players_give_prompt(self):
        active_player = self.players[self.active_player]

        emit("display_waiting_screen", {
            "text": "Wait for other players to give a prompt",
            "image": self.get_random_animation()
        }, to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("write_prompt", to=player.sid)

    def non_active_players_wait(self):
        for player in self.players:
            emit("display_waiting_screen", {
            "text": "Wait for the generated images."
            }, to=player.sid)

    def non_active_players_vote(self):
        active_player = self.players[self.active_player]

        emit("display_waiting_screen", {
            "text": "Wait for other players to vote."
        }, to=active_player)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("vote", to=player)

    def show_results(self):
        pass
    
        
if __name__ == "__main__":
    GameState()