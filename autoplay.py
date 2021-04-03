import random

import logic
import constants as c


class GameGrid():
    def __init__(self, dir = [c.KEY_UP]):
        
        ### prepare game 2048

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down, c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right, c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down, c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right, c.KEY_H: logic.left, c.KEY_L: logic.right, c.KEY_K: logic.up, c.KEY_J: logic.down}

        self.grid_cells = []
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.history_matrixs.append(self.matrix)
        self.history_matrixs.append(self.matrix)
        print(self.matrix)
        
        ### prepare game strategy
        dirs = [c.KEY_UP, c.KEY_LEFT, c.KEY_RIGHT, c.KEY_DOWN]
        for d in dir:
            dirs.remove(d)
        history_dir = -1
        
        ### play
        while True:
            ### for strategy1.4 serpentine(snakelike), when change direction
            if self.matrix[0][0] == 256 and self.matrix[0][c.GRID_LEN - 1] != 0:
                dirs = [c.KEY_UP, c.KEY_RIGHT, c.KEY_LEFT, c.KEY_DOWN]
                print("dirs change 256")
            ### for strategy1, when invalid direction
            if self.matrix == self.history_matrixs[-2]: # duplicate
                history_dir = history_dir + 1
                print("    ", history_dir)
                if history_dir < len(dir): # try wanted directions
                    d = dir[history_dir]
                else: # try other directions
                    d = dirs[history_dir - len(dir)]
            else:
                history_dir = -1
                d = dir[random.randint(0,len(dir)-1)]
            ### if random
            # d = dir[random.randint(0,len(dir)-1)]
            ### key down
            state = self.key_down(d)
            print(self.matrix, state)
            if state != 'not over':
                break # game over

    def key_down(self, dir):
        key = dir
        if key in self.commands:
            self.matrix, done = self.commands[dir](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
        return logic.game_state(self.matrix)

game_grid = GameGrid()
