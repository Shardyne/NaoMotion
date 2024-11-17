#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from aima.search import iterative_deepening_search
from nao_problem import NaoProblem
from utils import from_state_to_dict, play_song, do_moves


class NaoMove:
    """Classe per rappresentare un movimento del robot."""
    def __init__(self, duration, preconditions=None, postconditions=None):
        self.duration = duration
        self.preconditions = preconditions if preconditions else {}
        self.postconditions = postconditions if postconditions else {}

def initialize_moves():
    """Definisce i movimenti disponibili per il robot."""
    return {
        'StandUp': NaoMove(1.21, {'standing': False}, {'standing': True}),
        'AirGuitar': NaoMove(5.4, {'standing': True}, {'standing': True}),
        'ArmDance': NaoMove(13.03, {'standing': True}, {'standing': True}),
        'ArmsOpening': NaoMove(8.15, {'standing': True}, {'standing': True}),
        'BlowKisses': NaoMove(5.27, {'standing': True}, {'standing': True}),
        'Bow': NaoMove(4.81, {'standing': True}, {'standing': True}),
        'Clap': NaoMove(4.99, {'standing': True}, {'standing': True}),
        'ComeOn': NaoMove(5.35, {'standing': True}, {'standing': True}),
        'DanceMove': NaoMove(7.49, {'standing': True}, {'standing': True}),
        'DiagonalLeft': NaoMove(4.17, {'standing': True}, {'standing': True}),
        'DiagonalRight': NaoMove(6.46, {'standing': True}, {'standing': True}),
        'DoubleMovementGloryJoy': NaoMove(0.07, {'standing': True}, {'standing': True}),
        'Joy': NaoMove(4.50, {'standing': True}, {'standing': True}),
        'M_Crouch': NaoMove(1.65, {'standing': True}, {'standing': False}),
        'M_Hello': NaoMove(5.47, {'standing': True}, {'standing': True}),
        'M_SitRelax': NaoMove(15.46, {'standing': True}, {'sitting': True}),
        'M_Sit': NaoMove(11.37, {'standing': True}, {'sitting': True}),
        'M_Stand': NaoMove(3.45, {'sitting': True}, {'standing': True}),
        'M_StandInit': NaoMove(1.96, {'standing': True}, {'standing': True}),
        'M_StandZero': NaoMove(2.77, {'standing': True}, {'standing': True}),
        'M_WipeForehead': NaoMove(5.44, {'standing': True}, {'standing': True}),
        'MoveBackward': NaoMove(4.79, {'standing': True}, {'standing': True}),
        'MoveForward': NaoMove(3.75, {'standing': True}, {'standing': True}),
        'PulpFiction': NaoMove(6.83, {'standing': True}, {'standing': True}),
        'Rhythm': NaoMove(4.97, {'standing': True}, {'standing': True}),
        'RightArm': NaoMove(14.26, {'standing': True}, {'standing': True}),
        'RotationFootLLeg': NaoMove(7.5, {'standing': True}, {'standing': True}),
        'RotationFootRLeg': NaoMove(7.64, {'standing': True}, {'standing': True}),
        'SprinklerL': NaoMove(5.08, {'standing': True}, {'standing': True}),
        'SprinklerR': NaoMove(5.19, {'standing': True}, {'standing': True}),
        'StayingAlive': NaoMove(11.93, {'standing': True}, {'standing': True}),
        'TheRobot': NaoMove(7.56, {'standing': True}, {'standing': True}),
        'Union_arms': NaoMove(10.31, {'standing': True}, {'standing': True}),
        'Wave': NaoMove(5.99, {'standing': True}, {'standing': True}),
    }


def initialize_positions():
    """Definisce le posizioni obbligatorie e iniziali/finali."""
    initial_pos = ('M_StandInit', NaoMove(1.60))
    mandatory_positions = [
        ('M_WipeForehead', NaoMove(4.48)),
        ('M_Stand', NaoMove(2.32)),
        ('M_Hello', NaoMove(4.34)),
        ('M_Sit', NaoMove(9.84)),
        ('M_SitRelax', NaoMove(3.92)),
        ('M_StandZero', NaoMove(1.4)),
    ]
    final_goal_pos = ('M_Crouch', NaoMove(1.32))
    return [initial_pos, *mandatory_positions, final_goal_pos]


def main(robot_ip, port):
    moves = initialize_moves()
    positions = initialize_positions()
    total_steps = len(positions) - 1

    # Calcola il tempo medio perso nelle posizioni obbligatorie
    total_time_lost = sum(pos[1].duration for pos in positions)
    mean_time_lost_per_step = total_time_lost / total_steps

    solution = ()
    print("PIANIFICAZIONE DELLA COREOGRAFIA:")
    start_planning = time.time()

    for step in range(1, len(positions)):
        start_pos = positions[step - 1]
        end_pos = positions[step]
        remaining_time = 180.0 / total_steps - mean_time_lost_per_step

        # Stato iniziale e goal per il problema
        initial_state = {
            'choreography': [start_pos[0]],
            'standing': end_pos[1].preconditions.get('standing', True),
            'remaining_time': remaining_time,
            'moves_done': 0,
        }
        goal_state = {
            'standing': end_pos[1].preconditions.get('standing', True),
            'remaining_time': 0,
            'moves_done': 3,  # Fissato a 3 mosse tra le posizioni obbligatorie
        }

        # Risoluzione con iterativa approfondita
        problem = NaoProblem(initial_state, goal_state, moves)
        partial_solution = iterative_deepening_search(problem)
        if partial_solution is None:
            raise RuntimeError(f"Passo {step}: nessuna soluzione trovata!")

        # Aggiunge la coreografia trovata
        state_dict = from_state_to_dict(partial_solution.state)
        current_choreography = state_dict['choreography']
        print(f"Passo {step}: {', '.join(current_choreography)}")
        solution += tuple(current_choreography)

    end_planning = time.time()
    solution += (positions[-1][0],)

    print("\nSTATISTICHE:")
    print(f"Tempo di pianificazione: {end_planning - start_planning:.2f} secondi")
    print("-------------------------------------------------------")

    # Esecuzione della coreografia
    print("\nESECUZIONE DELLA DANZA:")
    play_song("Don't stop me now - Queen.mp3")
    start_dance = time.time()
    do_moves(solution, robot_ip, port)
    end_dance = time.time()
    print(f"Lunghezza della coreografia: {end_dance - start_dance:.2f} secondi.")


if __name__ == "__main__":
    import sys

    robot_ip = "127.0.0.1"
    port = 9559
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
        robot_ip = sys.argv[1]
    elif len(sys.argv) == 2:
        robot_ip = sys.argv[1]

    main(robot_ip, port)
