import goap
from unittest import TestCase


class SatisfiesGoal(TestCase):
    def test_empty_goal_empty_state(self):
        """"
        Checks that the most basic case, i.e. empty goal and empty state is
        valid.
        """
        goal = {}
        state = {}
        self.assertTrue(
            goap.satisfies_goal(goal, state),
            "Empty goal should be satisfied by any state")

    def test_non_empty_goal_empty_state(self):
        """
        Checks that an empty state does not satisfy a non empty goal.
        """
        goal = {'foo': True}
        state = {}
        self.assertFalse(
            goap.satisfies_goal(goal, state),
            "Empty state should not satisfy a goal")

    def test_different_value_in_state_and_world(self):
        """
        Checks that a different value in state and goal do not match.
        """
        goal = {'foo': True}
        state = {'foo': False}
        self.assertFalse(
            goap.satisfies_goal(goal, state), "State should not match")


class UpdateState(TestCase):
    def test_empty_state_update(self):
        """
        Checks that a state updated by an empty effect is itself.
        """
        state = {'foo': True}
        effect = {}
        self.assertEqual(state,
                         goap.update_state(state, effect),
                         "Empty effect should not change the state.")

    def test_change_value(self):
        """
        Checks that we can change the value in the effect.
        """
        expected = {'foo': True, 'bar': True}
        effect = {'foo': True}

        state = {'foo': False, 'bar': True}

        self.assertEqual(expected,
                         goap.update_state(state, effect),
                         "Should change value of foo")

    def test_does_not_modify_in_place(self):
        """
        Checks that the dict is not changed in place.
        """
        effect = {'foo': True}
        initial_state = {'foo': False, 'bar': True}

        # Copy the state
        state = dict(initial_state)
        goap.update_state(state, effect)

        # Check that the dict was not changed itself
        self.assertEqual(state, initial_state, "State should not be changed.")


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
