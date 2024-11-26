from aima.search import Problem
from utils import from_state_to_dict
class NaoProblem(Problem):

    def __init__(self, initial, goal, moves, threshold, previous_moves_done):
        super().__init__(initial, goal)
        self.available_moves = moves
        self.previous_moves_done = previous_moves_done
        self.time_threshold = threshold

    def is_move_applicable(self, state, move_name, move):
        state_dict = from_state_to_dict(state)

        # Controlla se il tempo rimanente è sufficiente
        if state_dict['remaining_time'] < move.Moveduration:
            return False

        # Controlla che il movimento non sia identico all'ultimo eseguito
        last_move = state_dict['choreography'][-4:]
        if move_name in self.previous_moves_done or move_name in last_move:
            return False

        

        return True

    def actions(self, state):
        usable_actions = []
        for move_name, move in self.available_moves.items():
            if self.is_move_applicable(state, move_name, move):
                usable_actions.append(move_name)
        return usable_actions

    def result(self, state, action):
        nao_move = self.available_moves[action]
        state_dict = from_state_to_dict(state)

        return (('choreography', (*state_dict['choreography'], action)),
                ('remaining_time', state_dict['remaining_time'] - nao_move.Moveduration),
                ('moves_done', state_dict['moves_done'] + 1))

    def goal_test(self, state):
        state_dict = from_state_to_dict(state)
        goal_dict = from_state_to_dict(self.goal)

        goal_remaining_time = goal_dict['remaining_time']
        a = goal_remaining_time
        b = goal_remaining_time + self.time_threshold

        # Verifica i vincoli del goal
        time_constraint = (a <= state_dict['remaining_time'] <= b)
        moves_done_constraint = (state_dict['moves_done'] >= goal_dict['moves_done'])
        return time_constraint and moves_done_constraint