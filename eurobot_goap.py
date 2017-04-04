#!/usr/bin/env python3
"""
A simple demo application for the Goal Oriented Action Planner.

Simulates an Eurobot 2017 robot that has to fetches rocks from craters and returns them to base.
"""

import argparse
import random

import goap


class ActionExecutionError(RuntimeError):
    pass


class Action:
    """
    A standard action.
    """
    preRequisite = {}
    effect = {}
    cost = 0.

    def execute(self, state):
        pass


class EmptyCrater(Action):
    """
    Empties a crater
    """
    cost = 10.

    def __init__(self, crater):
        self.crater = crater
        self.preRequisite = {
            'crater{}_empty'.format(crater): False,
            'robot_full': False,
        }

        self.effect = {
            'crater{}_empty'.format(crater): True,
            'robot_full': True,
        }

    def execute(self, state):
        print("Fetching rocks from crater #{}\t".format(self.crater), end='')

        # 30% chance of failure:
        if random.random() < 0.3:
            print("FAIL")
            raise ActionExecutionError

        state.update({
            'crater{}_empty'.format(self.crater): True,
            'robot_full': True,
        })

        print("OK")


class DepositRocks(Action):
    """
    Go put rocks in the cargo bay.
    """
    preRequisite = {'robot_full': True}

    effect = {'robot_full': False}

    def execute(self, state):
        print("Emptying robot in cargo bay")
        state.update({'robot_full': False, })


ACTIONS = [EmptyCrater(i) for i in range(6)] + [DepositRocks()]


def setup_state():
    state = {'robot_full': True}

    for i in range(6):
        state['crater{}_empty'.format(i)] = False

    return state


def setup_goal():
    goal = {'robot_full': False}

    for i in range(6):
        goal['crater{}_empty'.format(i)] = True

    return goal


def execute_game(state, goal):
    plan, cost = goap.plan(goal, state, ACTIONS, max_plan_length=20)

    while plan:
        action = plan.pop(0)
        try:
            action.execute(state)  # also update states
        except ActionExecutionError:
            # If an action failed, replan
            plan, cost = goap.plan(goal, state, ACTIONS, max_plan_length=20)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)

    return parser.parse_args()


def main():
    args = parse_args()
    execute_game(setup_state(), setup_goal())


if __name__ == '__main__':
    main()
