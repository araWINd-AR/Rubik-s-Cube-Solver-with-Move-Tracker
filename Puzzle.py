# ------------------------ Puzzle.py ------------------------
import random
import copy

COLORS = ['White', 'Yellow', 'Red', 'Orange', 'Blue', 'Green']
SIDES = 6

class State:
    def __init__(self, size=4, c=None):
        self.size = size
        self.actions = ['front', 'back', 'left', 'right', 'top', 'bottom']

        if c:
            self.d = c
            self.__front__ = c["front"]
            self.__back__ = c["back"]
            self.__left__ = c["left"]
            self.__right__ = c["right"]
            self.__top__ = c["top"]
            self.__bottom__ = c["bottom"]
        else:
            self.__front__ = repeat_as_list(COLORS[0], size)
            self.__back__ = repeat_as_list(COLORS[1], size)
            self.__left__ = repeat_as_list(COLORS[2], size)
            self.__right__ = repeat_as_list(COLORS[3], size)
            self.__top__ = repeat_as_list(COLORS[4], size)
            self.__bottom__ = repeat_as_list(COLORS[5], size)

        self.__sides__ = [self.__front__, self.__back__, self.__left__, self.__right__, self.__top__, self.__bottom__]
        self.d = {
            "front": self.__front__, "back": self.__back__, "left": self.__left__,
            "right": self.__right__, "top": self.__top__, "bottom": self.__bottom__
        }

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"FRONT: {self.__front__}\nBACK: {self.__back__}\nLEFT: {self.__left__}\nRIGHT: {self.__right__}\nTOP: {self.__top__}\nBOTTOM: {self.__bottom__}"

    def __hash__(self):
        return hash(str(self))

    def isGoalState(self):
        for side in self.__sides__:
            color = side[0][0]
            for row in side:
                if any(cell != color for cell in row):
                    return False
        return True

    def move(self, action):
        if action == 'front': self.turn_front()
        elif action == 'back': self.turn_back()
        elif action == 'left': self.turn_left()
        elif action == 'right': self.turn_right()
        elif action == 'top': self.turn_top()
        elif action == 'bottom': self.turn_bottom()
        self.__sides__ = [self.__front__, self.__back__, self.__left__, self.__right__, self.__top__, self.__bottom__]

    def turn_front(self): self.__front__ = rotate_2d(self.__front__)
    def turn_back(self): self.__back__ = rotate_2d(self.__back__)
    def turn_left(self): self.__left__ = rotate_2d(self.__left__)
    def turn_right(self): self.__right__ = rotate_2d(self.__right__)
    def turn_top(self): self.__top__ = rotate_2d(self.__top__)
    def turn_bottom(self): self.__bottom__ = rotate_2d(self.__bottom__)

# Utilities

def repeat_as_list(value, rep_count):
    return [[value for _ in range(rep_count)] for _ in range(rep_count)]

def rotate_2d(matrix):
    return [list(reversed(col)) for col in zip(*matrix)]

def move(state, action):
    new_state = state.copy()
    new_state.move(action)
    return new_state

def shuffle(state, n=5):
    new_state = state.copy()
    for _ in range(n):
        new_state = move(new_state, random.choice(new_state.actions))
    return new_state

def n_move_state(n=5):
    base = State()
    return shuffle(base, n)

def num_solved_sides(state):
    solved = 0
    for side in state.__sides__:
        color = side[0][0]
        if all(cell == color for row in side for cell in row):
            solved += 1
    return solved

def num_pieces_correct_side(state):
    correct = 0
    for side in state.__sides__:
        color = side[1][1]  # middle piece color
        for row in side:
            correct += row.count(color)
    return correct
