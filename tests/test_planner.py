import goap
from unittest import TestCase


class Planner(TestCase):
    class GrabWood:
        preRequisite = {}
        effect = {'hasWood': True}
        cost = 8.

    class CutLog:
        preRequisite = {'hasAxe': True}
        effect = {'hasWood': True}
        cost = 2.

    class GrabAxe:
        preRequisite = {}
        effect = {'hasAxe': True}
        cost = 2.

    class GrabFood:
        preRequisite = {}
        effect = {'hasFood': True}
        cost = 2.

    def test_completed_goal(self):
        """
        When the goal is already satisfied then no action is planned.
        """
        state = {'foo': True}
        goal = state
        plan, cost = goap.plan(goal, state, [self.GrabFood])
        self.assertEqual([], plan)
        self.assertEqual(0., cost)

    def test_simple_case(self):
        """
        When we can go to the goal in one action, then do it.
        """
        state = {'hasWood': False}
        goal = {'hasWood': True}
        possible_actions = [self.GrabWood]
        expected_plan = [self.GrabWood]

        plan, cost = goap.plan(goal, state, possible_actions)

        self.assertEqual(expected_plan, plan)
        self.assertEqual(self.GrabWood.cost, cost)

    def test_sequence_of_action(self):
        """
        Schedule a sequence of action when it is required.
        """
        state = {}
        goal = {'hasAxe': True, 'hasFood': True}
        possible_actions = [self.GrabFood, self.GrabAxe]
        expected_plan = [self.GrabAxe, self.GrabFood]

        plan, cost = goap.plan(goal, state, possible_actions)

        # Order may vary here
        self.assertEqual(
            set(plan),
            set(expected_plan), "Plan does not contain everything needed.")

    def test_respect_prerequisites(self):
        """
        Chosen sequence of actions respects actions pre requisites.

        In this case, this means we should first execute a GrabAxe before
        attempting to CutLog.
        """
        state = {}
        goal = {'hasWood': True}
        possible_actions = [self.CutLog, self.GrabAxe]
        expected_plan = [self.GrabAxe, self.CutLog]

        plan, cost = goap.plan(goal, state, possible_actions)

        self.assertEqual(plan, expected_plan,
                         "Prerequisites do not seem to be respected.")

    def test_minize_cost(self):
        """
        Chosen sequence should seem to minimize the cost.

        We test this by providing an expensive GrabWood function, or a cheaper
        GrabAxe + CutWood combo. The planner should go through the cheaper
        route.
        """
        state = {}
        goal = {'hasWood': True}
        possible_actions = [self.GrabWood, self.CutLog, self.GrabAxe]
        expected_plan = [self.GrabAxe, self.CutLog]

        plan, cost = goap.plan(goal, state, possible_actions)

        self.assertEqual(plan, expected_plan, "Should take cheaper route")
