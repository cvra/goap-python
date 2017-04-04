import goap

class Action:
    """
    A standard action.
    """
    preRequisite = {}
    effect = {}
    cost = 0.


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

    def execute(self):
        print("Fetching rocks from crater #{}".format(self.crater))


class DepositRocks(Action):
    """
    Go put rocks in the cargo bay.
    """
    preRequisite = {
        'robot_full': True
    }

    effect = {
        'robot_full': False
    }

    def execute(self):
        print("Emptying robot in cargo bay")

ACTIONS = [EmptyCrater(i) for i in range(6)] + [
    DepositRocks()
]

state = {
    'robot_full': True
}

for i in range(6):
    state['crater{}_empty'.format(i)] = False

goal = {
    'robot_full': False
}

for i in range(6):
    goal['crater{}_empty'.format(i)] = True

plan, cost = goap.plan(goal, state, ACTIONS, max_plan_length=20)

if plan is None:
    print("Cannot find a plan!")
else:
    for action in plan:
        action.execute()
