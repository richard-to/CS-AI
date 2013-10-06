
tree = [
    "A",
    [
        [
            "B",
            [3, 12, 8]
        ],
        [
            "C",
            [2, 4, 6]
        ],
        [
            "D",
            [14, 5, 2]
        ],

    ]
]


def minimaxDecision(state):
    bestMove = float("-inf")
    for a in actions(state[1]):
        predictedMove = minValue(a)
        if predictedMove > bestMove:
            bestMove = predictedMove
    print bestMove


def maxValue(state):
    if terminalTest(state):
        return utility(state)
    else:
        v = float("-inf")
        for a in actions(state[1]):
            v = max(v, minValue(a))
        return v


def minValue(state):
    if terminalTest(state):
        return utility(state)
    else:
        v = float("inf")
        for a in actions(state[1]):
            v = min(v, maxValue(a))
        return v


def terminalTest(state):
    return isinstance(state, int)


def utility(state):
    return state


def actions(state):
    return state


def max(current, new):
    if new > current:
        return new
    else:
        return current


def min(current, new):
    if new < current:
        return new
    else:
        return current


def main():
    minimaxDecision(tree)


if __name__ == '__main__':
    main()