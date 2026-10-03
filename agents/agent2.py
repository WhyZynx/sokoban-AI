import heapq
import time
from collections import deque


class Agent2:
    DIRECTIONS = {
        'South': (1, 0),
        'North': (-1, 0),
        'West': (0, -1),
        'East': (0, 1)
    }

    DECISION_LIMIT = 0.65
    SEARCH_DEPTH = 10

    def __init__(self):
        self.name = 'Agent 2 - A*'
        self.last_action = 'Stay'
        self.last_decision_time = 0
        self.recent_positions = []

    def get_state(self, game):
        return game.agent1, game.agent2, frozenset(game.boxes)

    def blocked(self, position, game):
        if hasattr(game, 'inside') and not game.inside(position):
            return True

        return position in game.walls

    def bfs_distance(self, start, target, game):
        if start == target:
            return 0

        queue = deque([(start, 0)])
        visited = {start}

        while queue:
            position, distance = queue.popleft()

            for dr, dc in self.DIRECTIONS.values():
                new_position = (position[0] + dr, position[1] + dc)

                if self.blocked(new_position, game):
                    continue

                if new_position in visited:
                    continue

                if new_position == target:
                    return distance + 1

                visited.add(new_position)
                queue.append((new_position, distance + 1))

        return 1000

    def get_valid_actions(self, state, game):
        agent1, agent2, boxes = state
        actions = []

        for action, (dr, dc) in self.DIRECTIONS.items():
            new_agent = (agent2[0] + dr, agent2[1] + dc)

            if self.blocked(new_agent, game):
                continue

            if new_agent == agent1:
                continue

            if new_agent in boxes:
                new_box = (new_agent[0] + dr, new_agent[1] + dc)

                if self.blocked(new_box, game):
                    continue

                if new_box in boxes or new_box == agent1:
                    continue

            actions.append(action)

        return actions

    def move(self, state, action):
        agent1, agent2, boxes = state
        dr, dc = self.DIRECTIONS[action]

        new_agent = (agent2[0] + dr, agent2[1] + dc)
        new_boxes = set(boxes)

        if new_agent in new_boxes:
            new_box = (new_agent[0] + dr, new_agent[1] + dc)
            new_boxes.remove(new_agent)
            new_boxes.add(new_box)

        return agent1, new_agent, frozenset(new_boxes)

    def heuristic(self, state, game):
        agent1, agent2, boxes = state
        unfinished = []

        for box in boxes:
            if box not in game.destinations:
                unfinished.append(box)

        if not unfinished:
            return 0

        box_cost = 0

        for box in unfinished:
            distances = []

            for goal in game.destinations:
                distance = self.bfs_distance(box, goal, game)
                distances.append(distance)

            if distances:
                box_cost += min(distances)

        agent_cost = 1000

        for box in unfinished:
            distance = self.bfs_distance(agent2, box, game)
            agent_cost = min(agent_cost, distance)

        completed = len(boxes) - len(unfinished)
        value = box_cost * 5 + agent_cost - completed * 20

        if agent2 in self.recent_positions:
            value += 200

        return value

    def root_actions(self, state, game):
        actions = self.get_valid_actions(state, game)

        if game.last_conflict and game.last_action2 in actions:
            actions.remove(game.last_action2)

        fresh = []

        for action in actions:
            new_state = self.move(state, action)
            new_position = new_state[1]

            if new_position not in self.recent_positions:
                fresh.append(action)

        if fresh:
            return fresh

        return actions

    def search(self, game):
        start_time = time.perf_counter()
        start = self.get_state(game)

        start_h = self.heuristic(start, game)
        queue = [(start_h, 0, 0, start, [])]

        best_cost = {start: 0}
        best_path = []
        best_h = float('inf')
        counter = 0

        while queue:
            if time.perf_counter() - start_time >= self.DECISION_LIMIT:
                break

            _, _, cost, state, path = heapq.heappop(queue)

            if cost > best_cost.get(state, float('inf')):
                continue

            h = self.heuristic(state, game)

            if path and h < best_h:
                best_h = h
                best_path = path

            if len(path) >= self.SEARCH_DEPTH:
                continue

            if not path:
                actions = self.root_actions(state, game)
            else:
                actions = self.get_valid_actions(state, game)

            for action in actions:
                new_state = self.move(state, action)
                new_cost = cost + 1

                if new_cost >= best_cost.get(new_state, float('inf')):
                    continue

                new_h = self.heuristic(new_state, game)

                best_cost[new_state] = new_cost
                counter += 1

                heapq.heappush(
                    queue,
                    (
                        new_cost + new_h,
                        counter,
                        new_cost,
                        new_state,
                        path + [action]
                    )
                )

        if best_path:
            return best_path[0]

        actions = self.root_actions(start, game)

        if not actions:
            return 'Stay'

        best_action = actions[0]
        best_h = float('inf')

        for action in actions:
            new_state = self.move(start, action)
            h = self.heuristic(new_state, game)

            if h < best_h:
                best_h = h
                best_action = action

        return best_action

    def choose_action(self, game):
        start_time = time.perf_counter()

        action = self.search(game)

        self.last_action = action
        self.last_decision_time = time.perf_counter() - start_time

        self.recent_positions.append(game.agent2)

        if len(self.recent_positions) > 6:
            self.recent_positions.pop(0)

        return action