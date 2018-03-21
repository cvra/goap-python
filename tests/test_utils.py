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

