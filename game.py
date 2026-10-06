DIRECTIONS = {
    'North': (-1, 0),
    'South': (1, 0),
    'West': (0, -1),
    'East': (0, 1)
}


class Game:
    def __init__(self, sokoban):
        self.sokoban = sokoban
        self.agent = sokoban.initial[0]
        self.boxes = set(sokoban.initial[1])
        self.actions = []
        self.current_step = 0
        self.history = []

    def set_actions(self, actions):
        self.reset()
        self.actions = actions or []

    def move(self, action):
        if action not in DIRECTIONS:
            return False

        dr, dc = DIRECTIONS[action]
        new_agent = (self.agent[0] + dr, self.agent[1] + dc)

        if self.sokoban.is_wall(new_agent):
            return False

        if new_agent in self.boxes:
            new_box = (new_agent[0] + dr, new_agent[1] + dc)

            if self.sokoban.is_wall(new_box) or new_box in self.boxes:
                return False

            self.boxes.remove(new_agent)
            self.boxes.add(new_box)

        self.agent = new_agent
        return True

    def forward(self):
        if self.current_step >= len(self.actions):
            return

        state = (self.agent, set(self.boxes), self.current_step)
        action = self.actions[self.current_step]

        if self.move(action):
            self.history.append(state)
            self.current_step += 1

    def backward(self):
        if self.history:
            self.agent, self.boxes, self.current_step = self.history.pop()

    def reset(self):
        self.agent = self.sokoban.initial[0]
        self.boxes = set(self.sokoban.initial[1])
        self.current_step = 0
        self.history = []

    def is_goal(self):
        return self.boxes <= self.sokoban.goals