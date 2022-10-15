import enum
import random

from stablediffusion_dixit.image_generation.local_generation.local_image_generator import LocalImageGenerator
from flask_socketio import SocketIO, emit
from time import *

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
            return
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
        else:
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
        self.round_scores = {}
        self.scores = []
        self.all_images = {}
        self.anims_this_round = []
        self.anims_prev_rounds = []
        self.phase.trigger_state(self)

    def start_game(self):
        self.state = GamePhase.ActivePlayerPrompt
        self.state.trigger_state(self)
    def get_player(self,sid):
        for player in self.players:
            if player.sid == sid:
                return player
                
    def get_random_animation(self) -> str:
        premade_animations = [f"premade_animations/{n}.gif" for n in range(2)]
        if len(self.anims_prev_rounds) == 0:
            return random.choice(premade_animations)
        else:
            return random.choice(self.anims_prev_rounds)

    def receive_prompt(self, id, prompt):
        if self.phase == GamePhase.ActivePlayerPrompt:
            if id == self.get_active_player().sid:
                self.active_players_image_ticket = self.image_generator.request_generation(prompt, callback=self.receive_image_finished_generating)
                self.phase = GamePhase.ActivePlayerImageWait
                self.phase.trigger_state(self)

        elif self.phase == GamePhase.AllPlayersPrompt:
            player = self.get_player(id)
            self.other_players_image_tickets[player.sid] = self.image_generator.request_generation(prompt, callback=self.receive_image_finished_generating)
            if len(self.other_players_image_tickets) == len(self.players - 1):
                self.phase = GamePhase.AllPlayersImageWait
                self.phase.trigger_state(self)

    def receive_proceed_active_player(self, sid):
        active_player_sid = self.players[self.active_player]

        if sid == active_player_sid:
            self.state = GamePhase.AllPlayersPrompt
            self.phase.trigger_state(self)

    def receive_image_finished_generating(self, image_num, image_path, anim_path):
        self.anims_this_round.append(anim_path)

        if self.phase == GamePhase.ActivePlayerImageWait:
            if self.active_players_image_ticket == image_num:
                self.active_players_image = image_path
                self.phase = GamePhase.ActivePlayerGiveClue
                self.phase.trigger_state(self)
        elif self.phase in (GamePhase.AllPlayersImageWait, GamePhase.AllPlayersPrompt):
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
        
        #Set the votes dict(player -> id)
        voted_for = self.card_order[voted_for]
        self.votes[current_player] = voted_for
        if len(self.votes) == len(self.players) - 1:
            self.phase = GamePhase.ShowResults
            self.score_votes()
            self.phase.trigger_state(self)
    
    def score_votes(self):
        #Initialize tallies, keeps track of votes for each player
        tallies = {player.sid : 0 for player in self.players}

        #Increment tallies
        for vote in self.votes.values():
            tallies[vote] += 1
        active_sid = self.players[self.active_player].sid     # Get the active Players Sid

        #If No one voted for the active player
        if tallies[active_sid] == 0:
            for player in self.players:
                if not player == self.players[self.active_player]:
                    player.score += 2
                    self.round_scores[player] = 2

        #If everyone voted for the active player
        elif tallies[active_sid] == len(self.players) - 1:
            for player in self.players:
               player.score += 2 + tallies[player.sid]
               self.round_scores[player] = 2 + tallies[player.sid]

        #If at least one person voted for the active player
        else:
            for player in self.players:
                if player == self.players[self.active_player]:
                    self.players[self.active_player].score += 3
                    self.round_scores[player] = 3
                else:
                    if self.votes[player.sid] == active_sid:
                        self.score += 3
                        self.round_scores[player] = 3 + tallies[player.sid]
                    else: 
                        self.score += tallies[player.sid]
                        self.round_scores[player] = tallies[player.sid]
        for index,player in enumerate(self.players):
            self.scores[index] = player.score
    

    def get_active_player(self):
        return self.players[self.active_player]

    def active_player_write_prompt(self):
        active_player = self.get_active_player()

        emit("display_prompt", to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("display_waiting_screen", {
                    "state": "inactive_player_wait_active_image_prompt",
                    "image": self.get_random_animation()
                }, to=player.sid)

        for tv in self.tvs:
            emit("display_waiting_screen", {
                "state": "tv_waiting_active_prompt",
                "image": self.get_random_animation()
            }, to=tv.sid)

    def active_player_wait(self):
        active_player = self.get_active_player()

        emit("display_waiting_screen", {
            "state": "image_generation_active_players",
            "image": self.get_random_animation()
        }, to=active_player.sid)

        for tv in self.tvs:
            emit("display_waiting_screen", {
                "state": "tv_waiting_generation_active",
                "image": self.get_random_animation()
            }, to=tv.sid)


    def active_player_give_clue(self):
        active_player = self.get_active_player()

        emit("display_active_player_ok", {
            "image": self.active_players_image
        }, to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("display_waiting_screen", {
                    "state": "inactive_player_wait_active_clue"
                }, to=player.sid)

        for tv in self.tvs:
            emit("display_waiting_screen", {
                "state": "tv_waiting_clue_active",
                "image": self.get_random_animation()
            }, to=tv.sid)

    def non_active_players_give_prompt(self):
        active_player = self.get_active_player()

        emit("display_waiting_screen", {
            "state": "active_player_waiting_inactive_prompt",
            "image": self.get_random_animation()
        }, to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("write_prompt", to=player.sid)

        for tv in self.tvs:
            emit("display_waiting_screen", {
                "state": "tv_waiting_inactive_prompt",
                "image": self.get_random_animation()
            }, to=tv.sid)

    def non_active_players_wait(self):
        active_player = self.get_active_player()

        for player in self.players:
            if player.sid != active_player.sid:
                emit("display_waiting_screen", {
                    "state": "image_generation_inactive_players",
                    "image": self.get_random_animation()
                }, to=player.sid)

        for tv in self.tvs:
            emit("display_waiting_screen", {
                "state": "tv_waiting_generation_inactive",
                "image": self.get_random_animation()
            }, to=tv.sid)

    def non_active_players_vote(self):
        active_player = self.get_active_player()

        emit("display_waiting_screen", {
            "state": "active_player_wait_inactive_votes",
            "image": self.get_random_animation()
        }, to=active_player.sid)

        for player in self.players:
            if player.sid != active_player.sid:
                emit("vote", {
                    "number": len(self.players)
                }, to=player.sid)

        images = self.create_images_list()

        for tv in self.tvs:
            emit("tv_show_cards_vote", {
                "state": "tv_waiting_generation_inactive",
                "images": ""
            }, to=tv.sid)

    def create_images_list(self):
        active_player = self.get_active_player()
        active_player_image = self.active_players_image
        self.other_players_images
        

        return None

    def show_results(self):
        tallies = {player.sid : 0 for player in self.players}

        #Increment tallies
        for vote in self.votes.values():
            tallies[vote] += 1
        active_sid = self.players[self.active_player].sid    # Get the active Players Sid

        scores = {}

        for player in self.players:
            scores[player.nickname] = player.score
            

        #If No one voted for the active player
        if tallies[active_sid] == 0:
            result = "nobody"
        elif tallies[active_sid] == len(self.players) - 1:
            result = "everybody"
        else:
            result = "split"
        guess_active = (result == "split" or result == "everybody")
        for player in self.players:
            results = {
                "is_active_player": player.sid == active_sid,
                "result": result,
                "player_round_score": self.round_scores[player],
                "player_total_score": player.score,
                "guessed_active_player": guess_active,
                "num_bonus_votes" : tallies[player]
            }
            self.all_images = self.other_players_images
            self.all_images[self.get_active_player] = self.active_players_image
            emit("player_display_results",results,to=player.sid)
            for tv in self.tvs:
                emit("tv_display_results",{
                    "round_scores": self.round_scores,
                "player_scores": self.scores,
                "images" : self.all_images
                },to=tv.id)
            sleep(15)
            self.reset()

    def reset(self):
        self.active_player = (self.active_player + 1) % len(self.players)
        self.active_players_image = None
        self.active_players_image_ticket = None
        self.other_players_images = {}
        self.other_players_image_tickets = {}
        self.card_order = None
        self.votes = {}
        self.round_scores = {}
        self.anims_prev_rounds = self.anims_this_round
        self.anims_this_round = []
        self.all_images = {}
        self.active_player_write_prompt()



        

        
if __name__ == "__main__":
    GameState()