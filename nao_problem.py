#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from aima.search import Problem
from utils import from_state_to_dict


class NaoProblem(Problem):
    def __init__(self, initial, goal, moves):
        super().__init__(initial, goal)
        self.moves = moves

    def is_move_applicable(self, state, move_name, move):
        state_dict = from_state_to_dict(state)

        # Controllo tempo rimanente
        if state_dict['remaining_time'] < move.duration:
            return False

        # Controllo standing
        if 'standing' in move.preconditions:
            if state_dict['standing'] != move.preconditions['standing']:
                return False

        # Nessuna mossa ripetuta consecutivamente
        if state_dict['choreography'][-1] == move_name:
            return False

        return True

    def actions(self, state):
        state_dict = from_state_to_dict(state)
        return [move_name for move_name, move in self.moves.items() if self.is_move_applicable(state_dict, move_name, move)]

    def result(self, state, action):
        move = self.moves[action]
        state_dict = from_state_to_dict(state)

        # Aggiorna lo stato
        return {
            'choreography': state_dict['choreography'] + [action],
            'standing': move.postconditions.get('standing', state_dict['standing']),
            'remaining_time': state_dict['remaining_time'] - move.duration,
            'moves_done': state_dict['moves_done'] + 1,
        }

    def goal_test(self, state):
        state_dict = from_state_to_dict(state)
        goal_dict = from_state_to_dict(self.goal)
        return (
            state_dict['remaining_time'] >= goal_dict['remaining_time'] and
            state_dict['moves_done'] >= goal_dict['moves_done'] and
            state_dict['standing'] == goal_dict['standing']
        )
