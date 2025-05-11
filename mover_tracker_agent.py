
# ------------------------ Agent.py ------------------------
import random, time
from Puzzle import State, move, num_solved_sides, num_pieces_correct_side, shuffle, n_move_state

class AgentClass:
    def __init__(self, QValues=None, cube=None):
        self.visited = []
        self.visit_count = {}
        self.revisits = 0
        self.QV = QValues if QValues is not None else {}
        self.R = {}
        self.start_state = cube if cube is not None else n_move_state(n=20)
        print(self.start_state)
        self.curr_state = self.start_state
        self.prev_state = None
        self.second_last_action = None
        self.actions = self.start_state.actions
        self.move_tracker = []  # List to track move sequence
        self.last_action = None
        self.move_stats = {action: 0 for action in self.actions}

    def register_patternsforCube(self):
        s = State()
        for action in self.actions:
            s_ = move(s, action)
            for action_ in self.actions:
                self.QV[(s_.__hash__(), action_)] = 10 if action_ == action else -10

    def QLearn(self, discount=0.95, episodes=15, epsilon=0.1):
        LEARNING_RATE = 0.6
        for i in range(episodes):
            print(f"===== EPISODE {i} =====")
            if self.curr_state.isGoalState():
                print("Goal reached during training.")
                return

            for action in self.actions:
                state_action = (self.curr_state.__hash__(), action)
                if state_action not in self.QV:
                    self.QV[state_action] = 0

            follow_policy = random.uniform(0, 1)
            if follow_policy > epsilon:
                best_action = max(self.actions, key=lambda a: self.QV[(self.curr_state.__hash__(), a)])
            else:
                best_action = random.choice(self.actions)

            self.curr_state.move(best_action)
            self.move_tracker.append(best_action)
            self.move_stats[best_action] += 1
            reward = self.reward(self.curr_state, best_action)
            max_future = max([self.QV.get((self.curr_state.__hash__(), a), 0) for a in self.actions])

            self.QV[(self.curr_state.__hash__(), best_action)] += LEARNING_RATE * (reward + discount * max_future - self.QV[(self.curr_state.__hash__(), best_action)])

            if self.curr_state.isGoalState():
                print("Goal reached!")
                break

    def Play(self):
        print("Starting playback of learned policy...")
        self.curr_state = self.start_state.copy()
        while not self.curr_state.isGoalState():
            best_action = max(self.actions, key=lambda a: self.QV.get((self.curr_state.__hash__(), a), -float('inf')))
            self.curr_state.move(best_action)
            self.move_tracker.append(best_action)
            print(self.curr_state)
            time.sleep(0.2)

        print("Final state reached!")

    def show_move_sequence(self):
        print("\n--- Move Sequence ---")
        for i, move in enumerate(self.move_tracker, 1):
            print(f"{i}. {move}")

    def save_move_sequence(self, filename="moves.txt"):
        with open(filename, "w") as f:
            for i, move in enumerate(self.move_tracker, 1):
                f.write(f"{i}. {move}\n")
        print(f"Move sequence saved to {filename}")

    def reward(self, state, action):
        next_state = move(state, action)
        if next_state.isGoalState():
            return 100
        reward = -0.1
        reward += num_solved_sides(next_state) - num_solved_sides(state)
        reward += (num_pieces_correct_side(next_state) - num_pieces_correct_side(state)) * 0.5
        return reward

# ---------------------- Main Script ----------------------
if __name__ == "__main__":
    agent = AgentClass()
    agent.register_patternsforCube()

    for ep in range(3):
        agent.QLearn(epsilon=0.2)

    agent.Play()
    agent.show_move_sequence()
    agent.save_move_sequence()
    print("Move statistics:", agent.move_stats)
    