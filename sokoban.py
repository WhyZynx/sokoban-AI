import sys
import time
import heapq

from collections import deque
from itertools import count


DIRECTIONS = {
    'North': (-1, 0),
    'South': (1, 0),
    'West': (0, -1),
    'East': (0, 1)
}

MOVE_COST = 1
PUSH_COST = 1
INF = float('inf')


class Sokoban:
    def __init__(self, path):
        with open(path) as file:
            lines = file.read().splitlines()

        self.height = len(lines)
        self.width = max(len(line) for line in lines)

        self.walls = set()
        self.goals = set()

        boxes = set()
        agent = None

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                position = (row, col)

                if char == '%':
                    self.walls.add(position)

                elif char == 'A':
                    agent = position

                elif char == 'B':
                    boxes.add(position)

                elif char == 'D':
                    self.goals.add(position)

                elif char == 'C':
                    boxes.add(position)
                    self.goals.add(position)

        self.initial = (agent, frozenset(boxes))

        self.build_distances()

    def is_wall(self, position):
        row, col = position

        return (
            position in self.walls
            or row < 0
            or row >= self.height
            or col < 0
            or col >= self.width
        )

    def is_goal(self, state):
        agent, boxes = state
        return boxes <= self.goals

    def actions(self, state):
        agent, boxes = state

        for action, direction in DIRECTIONS.items():
            dr, dc = direction

            new_agent = (agent[0] + dr, agent[1] + dc)

            if self.is_wall(new_agent):
                continue

            if new_agent in boxes:
                new_box = (new_agent[0] + dr, new_agent[1] + dc)

                if self.is_wall(new_box) or new_box in boxes:
                    continue

                new_boxes = (boxes - {new_agent}) | {new_box}

                yield action, (new_agent, new_boxes), PUSH_COST

            else:
                yield action, (new_agent, boxes), MOVE_COST

    def build_distances(self):
        self.distances = {goal: 0 for goal in self.goals}
        queue = deque(self.goals)

        while queue:
            box = queue.popleft()

            for dr, dc in DIRECTIONS.values():
                previous_box = (box[0] - dr, box[1] - dc)
                previous_agent = (box[0] - 2 * dr, box[1] - 2 * dc)

                if self.is_wall(previous_box) or self.is_wall(previous_agent):
                    continue

                if previous_box not in self.distances:
                    self.distances[previous_box] = self.distances[box] + 1
                    queue.append(previous_box)

    def heuristic(self, state):
        agent, boxes = state
        total = 0

        for box in boxes:
            distance = self.distances.get(box, INF)

            if distance == INF:
                return INF

            total += distance

        return total


def search(game, use_astar=False):
    start = game.initial

    if use_astar:
        start_h = game.heuristic(start)
    else:
        start_h = 0

    order = count()

    queue = [
        (start_h, next(order), 0, start)
    ]

    best_cost = {start: 0}
    parent = {start: None}

    expanded = 0

    while queue:
        priority, _, cost, state = heapq.heappop(queue)

        if cost > best_cost.get(state, INF):
            continue

        expanded += 1

        if game.is_goal(state):
            actions = []

            while parent[state] is not None:
                old_state, action = parent[state]
                actions.append(action)
                state = old_state

            actions.reverse()

            return actions, cost, expanded

        for action, new_state, move_cost in game.actions(state):
            new_cost = cost + move_cost

            if new_cost < best_cost.get(new_state, INF):
                if use_astar:
                    h = game.heuristic(new_state)
                else:
                    h = 0

                if h == INF:
                    continue

                best_cost[new_state] = new_cost
                parent[new_state] = (state, action)

                heapq.heappush(
                    queue,
                    (new_cost + h, next(order), new_cost, new_state)
                )

    return None, None, expanded


if __name__ == '__main__':
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = 'maps/example_map.txt'

    game = Sokoban(path)

    for name, use_astar in [
        ('UCS', False),
        ('A*', True)
    ]:
        start = time.time()

        actions, cost, expanded = search(game, use_astar)

        elapsed = time.time() - start

        print()
        print('===', name, '===')

        if actions is None:
            print('No solution')
        else:
            print('Actions:', actions)
            print('Total cost:', cost)

        print('Expanded:', expanded)
        print('Time:', f'{elapsed:.4f}s')