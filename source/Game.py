class Game(object):

    class Rules(object):
        def __init__(self):
            self.endgame_point_transfer_scale = 0
            self.wildcard_value = 0
            self.wildcard_retention_penalty = 25

    def __init__(self):
        self.turns_completed = 0
        self.players = list()

    def check_for_completion(self):
        pass


    def do_round(self):
        player_index = self.turns_completed % len(self.players)
        player = self.players[player_index]


    def execute(self):
        # Load board

        # Begin taking turns
        turn_counter = 0
        consecutive_passes = 0
        running = True
        while running:
            # Get the next player, or leave game loop if number of players is too few
            if len(self.players) < 2:
                break
            player_index = turn_counter % len(self.players)
            player = self.players[player_index]  # get the next player

            # Have player take turn


            # Revise game state after turn
            if PLAYER_PASSED:
                consecutive_passes += 1

                if consecutive_passes >=

            if player.is_participating():
                turn_counter += 1
            else:
                del self.players[player_index]

