import goap

class IndexArms:
    cost = 1
    preRequisite = {
    }

    effect = {
        'indexed': True
    }


class RetractArms:
    cost = 1
    preRequisite = {
        'indexed': True
    }

    effect = {
        'deployed': False
    }

class BuildTower:
    cost = 1
    preRequisite = {
        'deployed': False,
        'has_blocks': True
    }

    effect = {
        'deployed': True,
        'tower_built': True
    }

class PickupBlocks:
    cost = 1
    preRequisite = {
        'deployed': False,
    }

    effect = {
        'deployed': True,
        'has_blocks': True
    }

class PressSwitch:
    cost = 1
    preRequisite = {
        'deployed': False,
    }

    effect = {
        'deployed': True,
        'switch_on': True
    }

ACTIONS=[RetractArms, IndexArms, BuildTower, PickupBlocks, PressSwitch]

def problem(planner):
    goal = {
        'deployed': False,
        'tower_built': True,
        'switch_on': True,
    }

    state = {}
    return planner(goal, state, ACTIONS)

p1 = sorted(str(s) for s in problem(goap.fast_plan)[0])
p2 = sorted(str(s) for s in problem(goap.plan)[0])

assert p1 == p2


import timeit

N = 100

t_slow = timeit.timeit('problem(goap.plan)', globals=globals(), number=N)
t_fast = timeit.timeit('problem(goap.fast_plan)', globals=globals(), number=N)

print("Solved the GoalAction {} times.".format(N))
print("Slow: {:.3f} Fast: {:.3f} ({:.1f}x speedup)".format(t_slow, t_fast, t_slow / t_fast))
