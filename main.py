#!/usr/bin/python
# -*- coding: utf-8 -*-

from aima.search import *
from nao_problem import NaoProblem
from utils import *

# Funzione per verificare le condizioni iniziali della posizione "standing"
def precondition_standing(position):
    return position != 'M_SitRelax'

# Funzione per verificare le condizioni finali della posizione "standing"
def postcondition_standing(position):
    return position not in ('M_Sit', 'M_SitRelax')

class NaoMove:
    """
    Questa classe definisce le informazioni relative
    a una particolare mossa.
    """
    def __init__(self, duration=None, preconditions=None, postconditions=None):
        self.duration = duration
        self.preconditions = preconditions if preconditions is not None else {}
        self.postconditions = postconditions if postconditions is not None else {}

def main(robot_ip, port):
    # Lista delle mosse disponibili per il robot
    moves = {
        'AirGuitar': NaoMove(4.10, {'standing': True}, {'standing': True}),
        'Finger': NaoMove(4.10, {'standing': True}, {'standing': True}),
        'DanceTwist': NaoMove(4.10, {'standing': True}, {'standing': True}),
        'Handup': NaoMove(4.10, {'standing': True}, {'standing': True}),
        'ArmDance': NaoMove(10.42, {'standing': True}, {'standing': True}),
        'BlowKisses': NaoMove(4.58, {'standing': True}, {'standing': True}),
        'Bow': NaoMove(3.86, {'standing': True}, {'standing': True}),
        'DiagonalRight': NaoMove(2.56, {'standing': True}, {'standing': True}),
        'DanceMove': NaoMove(7.3, {'standing': True}, {'standing': True}),
        'SprinklerL': NaoMove(4.6, {'standing': True}, {'standing': True}),
        'SprinklerR': NaoMove(4.36, {'standing': True}, {'standing': True}),
        'RightArm': NaoMove(9.19, None, None),
        'TheRobot': NaoMove(7, {'standing': True}, {'standing': True}),
        'ComeOn': NaoMove(3.62, {'standing': True}, {'standing': True}),
        'StayingAlive': NaoMove(5.90, {'standing': True}, {'standing': True}),
        'Rhythm': NaoMove(2.95, {'standing': True}, {'standing': True}),
        'PulpFiction': NaoMove(5.80, {'standing': True}, {'standing': True}),
        'Wave': NaoMove(3.72, None, None),
        'Clap': NaoMove(4.10, None, None),
        'ArmsOpening': NaoMove(8.15, {'standing': True}, {'standing': True}),
        'DiagonalLeft': NaoMove(4.17, {'standing': True}, {'standing': True}),
        'DoubleMovement': NaoMove(6.76),
        'Glory': NaoMove(3.90),
        'Joy': NaoMove(5.19),
        'MoveBackward': NaoMove(4.79),
        'MoveForward': NaoMove(3.75),
        'RotationFootLLeg': NaoMove(7.50),
        'Union_arms': NaoMove(10.31),
    }

    # Posizioni iniziali, obbligatorie e finali
    initial_pos = ('M_StandInit', NaoMove(2.1))
    mandatory_pos = [
        ('M_WipeForehead', NaoMove(5.48)),
        ('M_Stand', NaoMove(2.82)),
        ('M_Hello', NaoMove(5.19)),
        ('M_Sit', NaoMove(11.57)),
        ('M_SitRelax', NaoMove(15.62)),
        ('M_StandZero', NaoMove(1.4))
    ]
    final_goal_pos = ('M_Crouch', NaoMove(1.32))

    pos_list = [initial_pos, *mandatory_pos, final_goal_pos]
    number_of_steps = len(pos_list) - 1

    # Lista per tracciare le mosse già eseguite
    executed_moves = []

    # Calcolare il tempo totale per le mosse obbligatorie
    total_time = sum(pos[1].duration for pos in pos_list)

    # Consideriamo il tempo totale come distribuito uniformemente su ciascun passo
    mean_time_lost_because_of_mandatory_positions = total_time / number_of_steps

    # Fase di pianificazione
    solution = tuple()
    print("PLANNED CHOREOGRAPHY:")
    start_planning = time.time()
    last_move = None

    for index in range(1, len(pos_list)):
        # Pianificazione tra posizione di partenza e posizione finale
        starting_pos = pos_list[index - 1]
        ending_pos = pos_list[index]

        if ending_pos[0] in executed_moves:
            print(f"Skipping move {ending_pos[0]} as it was already executed.")
            print(f"Moves executed so far: {executed_moves}")
            continue  # Salta la mossa che è già stata eseguita

        choreography = (starting_pos[0],)  # Coreografia iniziale
        initial_standing = postcondition_standing(starting_pos[0])
        goal_standing = precondition_standing(ending_pos[0])
        remaining_time = 110.0 / number_of_steps - mean_time_lost_because_of_mandatory_positions

        cur_state = (
            ('choreography', choreography),
            ('standing', initial_standing),
            ('remaining_time', remaining_time),
            ('moves_done', 0)
        )

        cur_goal_state = (
            ('standing', goal_standing),
            ('remaining_time', 0),
            ('moves_done', 2)
        )

        keys = list(moves.items())
        random.shuffle(keys)
        moves = dict(keys)

        cur_problem = NaoProblem(cur_state, cur_goal_state, moves, 1, solution)
        cur_solution = iterative_deepening_search(cur_problem)

        if cur_solution is None:
            raise RuntimeError(f'Step {index} - no solution was found!')

        cur_solution_dict = from_state_to_dict(cur_solution.state)
        cur_choreography = cur_solution_dict['choreography']
        print(f"Step {index}: \t" + ", ".join(cur_choreography))
        solution += cur_choreography

        # Aggiungi la mossa corrente alla lista delle mosse eseguite
        executed_moves.extend(cur_choreography)
        moves = {move: details for move, details in moves.items() if move not in executed_moves}

    # Fase di conclusione della pianificazione
    end_planning = time.time()
    solution += (final_goal_pos[0],)
    state_dict = from_state_to_dict(cur_solution.state)
    print("\nINFO:")
    print(f"Time required for the planning : %.2f seconds." % (end_planning - start_planning))
    print(f"Estimated choreography duration time: {110 - state_dict['remaining_time']}")
    print("-------------------------------------------------------")
    
    # Esecuzione della danza
    print("\nRunning...")
    play_song("Daft Punk - Something About Us.mp3")
    start_dance = time.time()
    do_moves(solution, robot_ip, port)
    end_dance = time.time()
    print(f"Real choreography duration time: %.2f seconds." % (end_dance - start_dance))

if __name__ == "__main__":
    robot_ip = "127.0.0.1"
    port = 9559  # Inserisci la porta NAO
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        robot_ip = sys.argv[1]
    elif len(sys.argv) == 2:
        robot_ip = sys.argv[1]
    
    main(robot_ip, port)
