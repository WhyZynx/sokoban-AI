import heapq
import time
from collections import deque


class Agent1:
    DIRECTIONS = {
        'North': (-1, 0),
        'South': (1, 0),
        'East': (0, 1),
        'West': (0, -1)
    }

    DECISION_LIMIT = 0.65
    SEARCH_DEPTH = 10

    def __init__(self):
        self.name = 'Agent 1 - GBFS'
        self.last_action = 'Stay'
        self.last_decision_time = 0
        self.recent_positions = []
        self.goal_distances = {}

    def get_state(self, game):
        return game.agent1, game.agent2, frozenset(game.boxes)

    def blocked(self, position, game):
        if hasattr(game, 'inside') and not game.inside(position):
            return True

        return position in game.walls

    def prepare_distances(self, game):
        self.goal_distances = {}

        for goal in game.destinations:
            distances = {goal: 0}
            queue = deque([goal])

            while queue:
                box = queue.popleft()
                distance = distances[box]

                for dr, dc in self.DIRECTIONS.values():
                    old_box = (box[0] - dr, box[1] - dc)
                    old_agent = (box[0] - 2 * dr, box[1] - 2 * dc)

                    if self.blocked(old_box, game):
                        continue

                    if self.blocked(old_agent, game):
                        continue

                    if old_box not in distances:
                        distances[old_box] = distance + 1
                        queue.append(old_box)

            self.goal_distances[goal] = distances

    def box_goal_distance(self, box):
        distances = []

        for values in self.goal_distances.values():
            if box in values:
                distances.append(values[box])

        return min(distances) if distances else 1000

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
            new_agent = (agent1[0] + dr, agent1[1] + dc)

            if self.blocked(new_agent, game):
                continue

            if new_agent == agent2:
                continue

            if new_agent in boxes:
                new_box = (new_agent[0] + dr, new_agent[1] + dc)

                if self.blocked(new_box, game):
                    continue

                if new_box in boxes or new_box == agent2:
                    continue

            actions.append(action)

        return actions

    def move(self, state, action):
        agent1, agent2, boxes = state
        dr, dc = self.DIRECTIONS[action]

        new_agent = (agent1[0] + dr, agent1[1] + dc)
        new_boxes = set(boxes)

        if new_agent in new_boxes:
            new_box = (new_agent[0] + dr, new_agent[1] + dc)
            new_boxes.remove(new_agent)
            new_boxes.add(new_box)

        return new_agent, agent2, frozenset(new_boxes)

    def evaluate(self, state, game):
        agent1, agent2, boxes = state
        score = 0
        unfinished = []

        for box in boxes:
            if box in game.destinations:
                score += 1000
            else:
                unfinished.append(box)

        for box in unfinished:
            distance = self.box_goal_distance(box)
            score -= distance * 10

        if unfinished:
            distances = []

            for box in unfinished:
                distance = self.bfs_distance(agent1, box, game)
                distances.append(distance)

            score -= min(distances)

        if agent1 in self.recent_positions:
            score -= 200

        return score

    def root_actions(self, state, game):
        actions = self.get_valid_actions(state, game)

        if game.last_conflict and game.last_action1 in actions:
            actions.remove(game.last_action1)

        fresh = []

        for action in actions:
            new_state = self.move(state, action)
            new_position = new_state[0]

            if new_position not in self.recent_positions:
                fresh.append(action)

        if fresh:
            return fresh

        return actions

    def search(self, game):
        start_time = time.perf_counter()
        start = self.get_state(game)

        start_score = self.evaluate(start, game)
        queue = [(-start_score, 0, start, [])]

        visited = set()
        best_path = []
        best_score = -float('inf')
        counter = 0

        while queue:
            if time.perf_counter() - start_time >= self.DECISION_LIMIT:
                break

            _, _, state, path = heapq.heappop(queue)

            if state in visited:
                continue

            visited.add(state)

            score = self.evaluate(state, game)

            if path and score > best_score:
                best_score = score
                best_path = path

            if len(path) >= self.SEARCH_DEPTH:
                continue

            if not path:
                actions = self.root_actions(state, game)
            else:
                actions = self.get_valid_actions(state, game)

            for action in actions:
                new_state = self.move(state, action)

                if new_state in visited:
                    continue

                new_score = self.evaluate(new_state, game)

                counter += 1
                heapq.heappush(
                    queue,
                    (-new_score, counter, new_state, path + [action])
                )

        if best_path:
            return best_path[0]

        actions = self.root_actions(start, game)

        if not actions:
            return 'Stay'

        best_action = actions[0]
        best_score = -float('inf')

        for action in actions:
            new_state = self.move(start, action)
            score = self.evaluate(new_state, game)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def choose_action(self, game):
        start_time = time.perf_counter()

        self.prepare_distances(game)
        action = self.search(game)

        self.last_action = action
        self.last_decision_time = time.perf_counter() - start_time

        self.recent_positions.append(game.agent1)

        if len(self.recent_positions) > 6:
            self.recent_positions.pop(0)

        return action