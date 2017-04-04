def satisfies_goal(goal, state):
    """
    Checks if the given goal is satisfied by the given world state.
    """
    for key, value in goal.items():
        try:
            if state[key] != value:
                return False
        except KeyError:
            return False

    return True


def update_state(state, effect):
    """
    Returns the given state updated by the desired effect.
    """
    state = dict(state)
    state.update(effect)
    return state


def plan(goal, state, actions, max_plan_length=10):
    """
    Returns a sequence of element from actions that takes the given state to the goal and the cost associated with the given plan.
    """
    # Avoid infinite recurson
    if max_plan_length <= 0:
        return

    current_cost = float('inf')
    current_plan = None

    # If the state already satisfies the goal, then no action is required
    if satisfies_goal(goal, state):
        return [], 0.

    # Do a DFS search of the planning tree
    for a in actions:
        # Abort the search if we do not meet the action pre requisites
        if not satisfies_goal(a.preRequisite, state):
            continue

        # Computes the new path recursively
        new_plan = plan(goal,
                        update_state(state, a.effect), actions,
                        max_plan_length - 1)

        # If we found a plan and it is cheaper than the current cost, then pick
        # it
        if new_plan is not None:
            new_plan, new_cost = new_plan
            if a.cost + new_cost < current_cost:
                current_plan = [a] + new_plan
                current_cost = a.cost + new_cost

    return current_plan, current_cost
