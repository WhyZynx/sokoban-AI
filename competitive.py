DIRECTIONS = {
    'North': (-1, 0),
    'South': (1, 0),
    'West': (0, -1),
    'East': (0, 1),
    'Stay': (0, 0)
}


def load_competitive_map(path):
    walls = set()
    boxes = set()
    destinations = set()
    agents = []

    with open(path) as file:
        lines = file.read().splitlines()

    height = len(lines)
    width = max(len(line) for line in lines)

    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            position = (row, col)

            if char == '%':
                walls.add(position)
            elif char == 'A':
                agents.append(position)
            elif char == 'B':
                boxes.add(position)
            elif char == 'D':
                destinations.add(position)
            elif char == 'C':
                boxes.add(position)
                destinations.add(position)

    if len(agents) != 2:
        raise ValueError('Competitive map must have 2 agents.')

    return walls, boxes, destinations, agents[0], agents[1], height, width


class CompetitiveGame:
    def __init__(
        self,
        walls,
        boxes,
        destinations,
        agent1,
        agent2,
        max_steps,
        height=None,
        width=None
    ):
        self.walls = set(walls)
        self.boxes = set(boxes)
        self.destinations = set(destinations)

        self.agent1 = agent1
        self.agent2 = agent2

        self.max_steps = max_steps
        self.current_step = 0

        self.height = height
        self.width = width

        self.box_owner = {}

        self.last_conflict = False
        self.last_action1 = None
        self.last_action2 = None

    def inside(self, position):
        if self.height is None or self.width is None:
            return True

        row, col = position

        return 0 <= row < self.height and 0 <= col < self.width

    def blocked(self, position):
        return not self.inside(position) or position in self.walls

    def stay(self, agent):
        return {
            'agent_from': agent,
            'agent_to': agent,
            'box_from': None,
            'box_to': None
        }

    def get_intent(self, agent, action):
        if action not in DIRECTIONS or action == 'Stay':
            return self.stay(agent)

        dr, dc = DIRECTIONS[action]
        new_agent = (agent[0] + dr, agent[1] + dc)

        if self.blocked(new_agent):
            return self.stay(agent)

        if new_agent in self.boxes:
            new_box = (new_agent[0] + dr, new_agent[1] + dc)

            if self.blocked(new_box) or new_box in self.boxes:
                return self.stay(agent)

            return {
                'agent_from': agent,
                'agent_to': new_agent,
                'box_from': new_agent,
                'box_to': new_box
            }

        return {
            'agent_from': agent,
            'agent_to': new_agent,
            'box_from': None,
            'box_to': None
        }

    def has_conflict(self, move1, move2):
        if move1['agent_to'] == move2['agent_to']:
            return True

        if (
            move1['agent_to'] == move2['agent_from']
            and move2['agent_to'] == move1['agent_from']
        ):
            return True

        if move1['box_to'] is not None:
            if move1['box_to'] == move2['agent_to']:
                return True

            if move1['box_to'] == move2['agent_from']:
                return True

        if move2['box_to'] is not None:
            if move2['box_to'] == move1['agent_to']:
                return True

            if move2['box_to'] == move1['agent_from']:
                return True

        if move1['box_to'] is not None and move2['box_to'] is not None:
            if move1['box_to'] == move2['box_to']:
                return True

        if move1['box_from'] is not None and move2['box_from'] is not None:
            if move1['box_from'] == move2['box_from']:
                return True

        if move1['box_to'] is not None and move2['box_from'] is not None:
            if move1['box_to'] == move2['box_from']:
                return True

        if move2['box_to'] is not None and move1['box_from'] is not None:
            if move2['box_to'] == move1['box_from']:
                return True

        return False

    def step(self, action1, action2):
        if self.is_finished():
            return

        if action1 not in DIRECTIONS:
            action1 = 'Stay'

        if action2 not in DIRECTIONS:
            action2 = 'Stay'

        move1 = self.get_intent(self.agent1, action1)
        move2 = self.get_intent(self.agent2, action2)

        conflict = self.has_conflict(move1, move2)

        if conflict:
            self.last_conflict = True
            self.last_action1 = action1
            self.last_action2 = action2

            move1 = self.stay(self.agent1)
            move2 = self.stay(self.agent2)
        else:
            self.last_conflict = False
            self.last_action1 = None
            self.last_action2 = None

        self.apply_moves(move1, move2)
        self.current_step += 1

    def apply_moves(self, move1, move2):
        new_boxes = set(self.boxes)

        if move1['box_from'] is not None:
            new_boxes.discard(move1['box_from'])

        if move2['box_from'] is not None:
            new_boxes.discard(move2['box_from'])

        if move1['box_to'] is not None:
            new_boxes.add(move1['box_to'])

        if move2['box_to'] is not None:
            new_boxes.add(move2['box_to'])

        self.agent1 = move1['agent_to']
        self.agent2 = move2['agent_to']
        self.boxes = new_boxes

        self.update_owner(move1, 1)
        self.update_owner(move2, 2)

    def update_owner(self, move, player):
        old_box = move['box_from']
        new_box = move['box_to']

        if old_box is None:
            return

        if old_box in self.box_owner:
            del self.box_owner[old_box]

        if new_box in self.destinations:
            self.box_owner[new_box] = player

    def get_score(self):
        score1 = 0
        score2 = 0

        for box, owner in self.box_owner.items():
            if box not in self.boxes:
                continue

            if box not in self.destinations:
                continue

            if owner == 1:
                score1 += 1
            elif owner == 2:
                score2 += 1

        return score1, score2

    def is_finished(self):
        return self.current_step >= self.max_steps

    def get_winner(self):
        score1, score2 = self.get_score()

        if score1 > score2:
            return 'Agent 1'

        if score2 > score1:
            return 'Agent 2'

        return 'Draw'

    def show_state(self):
        score1, score2 = self.get_score()

        print('Step:', self.current_step)
        print('Agent 1:', self.agent1)
        print('Agent 2:', self.agent2)
        print('Boxes:', self.boxes)
        print('Score:', score1, '-', score2)
        print('Conflict:', self.last_conflict)