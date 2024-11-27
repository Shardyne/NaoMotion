from aima.search import Problem
from utils import from_state_to_dict

class NaoProblem(Problem):

    def __init__(self, initial_state, goal_state, available_moves, time_buffer, executed_moves):
        super().__init__(initial_state, goal_state)
        self.available_moves = available_moves  # Dizionario delle mosse disponibili
        self.executed_moves = executed_moves  # Lista delle mosse già eseguite
        self.time_buffer = time_buffer  # Margine di tempo accettabile per il goal

    def is_move_valid(self, current_state, move_name, move_details):
        """
        Determina se una mossa è valida.
        Controlla che il tempo rimanente sia sufficiente e che la mossa non sia ripetuta di recente.
        """
        state_dict = from_state_to_dict(current_state)

        # Verifica se il tempo rimanente è sufficiente per eseguire la mossa
        if state_dict['remaining_time'] < move_details.Moveduration:
            return False

        # Verifica che la mossa non sia tra quelle già eseguite o tra le ultime eseguite
        recent_moves = state_dict['choreography'][-4:]  # Ultime 4 mosse eseguite
        if move_name in self.executed_moves or move_name in recent_moves:
            return False

        return True

    def actions(self, current_state):
        """
        Ritorna una lista di mosse valide che possono essere eseguite nello stato corrente.
        """
        valid_actions = []
        for move_name, move_details in self.available_moves.items():
            if self.is_move_valid(current_state, move_name, move_details):
                valid_actions.append(move_name)
        return valid_actions

    def result(self, current_state, selected_action):
        """
        Applica una mossa allo stato corrente e restituisce il nuovo stato.
        """
        selected_move = self.available_moves[selected_action]
        state_dict = from_state_to_dict(current_state)

        return (
            ('choreography', (*state_dict['choreography'], selected_action)),  # Aggiunge la mossa alla coreografia
            ('remaining_time', state_dict['remaining_time'] - selected_move.Moveduration),  # Aggiorna il tempo rimanente
            ('moves_done', state_dict['moves_done'] + 1)  # Incrementa il conteggio delle mosse
        )

    def goal_test(self, current_state):
        """
        Verifica se lo stato corrente soddisfa i criteri del goal.
        """
        state_dict = from_state_to_dict(current_state)
        goal_dict = from_state_to_dict(self.goal)

        # Vincolo sul tempo: il tempo rimanente deve essere compreso nel margine accettabile
        goal_remaining_time = goal_dict['remaining_time']
        time_constraint = (goal_remaining_time <= state_dict['remaining_time'] <= goal_remaining_time + self.time_buffer)

        # Vincolo sul numero di mosse eseguite
        moves_done_constraint = (state_dict['moves_done'] >= goal_dict['moves_done'])

        return time_constraint and moves_done_constraint
