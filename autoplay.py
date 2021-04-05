import random

import logic
import constants as c


class GameGrid():

    def __init__(self, strtg=2.2):

        # prepare game 2048

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down, c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right}

        self.grid_cells = []
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.history_matrixs.append(self.matrix)
        self.history_matrixs.append(self.matrix)
        print(self.matrix)
        
        # prepare game strategy
        dirs = [c.KEY_UP, c.KEY_LEFT, c.KEY_RIGHT, c.KEY_DOWN]
        # for strategy1 direction-first
        if int(strtg) == 1:
            if strtg == 1.1:  # line
                dir = [c.KEY_UP]
            elif strtg == 1.2:  # corner
                dir = [c.KEY_UP, c.KEY_LEFT]
            elif strtg == 1.4:  # serpentine(snakelike)
                dir = [c.KEY_UP, c.KEY_LEFT]
            for d in dir:
                dirs.remove(d)
            history_dir = -1
        elif int(strtg == 2):
            return
        
        # play
        while True:
            if int(strtg) == 0:
                d = dirs[random.randint(0,len(dir)-1)]
            elif int(strtg) == 1:
                # for strategy1.4 serpentine(snakelike), when change direction
                if strtg == 1.4 and self.matrix[0][0] == 256 and self.matrix[0][c.GRID_LEN - 1] != 0:
                    dirs = [c.KEY_UP, c.KEY_RIGHT, c.KEY_LEFT, c.KEY_DOWN]
                    print("dirs change 256")
                # for strategy1, when invalid direction
                if self.matrix == self.history_matrixs[-2]:  # duplicate
                    history_dir = history_dir + 1
                    print("    ", history_dir)
                    if history_dir < len(dir):  # try wanted directions
                        d = dir[history_dir]
                    else:  # try other directions
                        d = dirs[history_dir - len(dir)]
                else:
                    history_dir = -1
                    d = dir[random.randint(0, len(dir)-1)]
            elif int(strtg) == 2:
                merged = []
                if strtg == 2.1:  #strategy2.1 more merged_numbers
                    for d in dirs:
                        m, d, n, g = self.commands[d](self.matrix)
                        merged.append(n)
                    for m in merged:
                        if m != 0:
                            d = dirs[merged.index(max(merged))]
                            break
                    if d != dirs[merged.index(max(merged))]:
                        d = dirs[random.randint(0,len(dirs)-1)]
                    print(d, merged)
                if strtg == 2.2:  #strategy2.2 more merged_grids
                    for d in dirs:
                        m, d, n, g = self.commands[d](self.matrix)
                        merged.append(g)
                    for m in merged:
                        if m != 0:
                            d = dirs[merged.index(max(merged))]
                            break
                    if d != dirs[merged.index(max(merged))]:
                        d = dirs[random.randint(0,len(dirs)-1)]
                    print(d, merged)
            else:
                return False
            # key down
            state = self.key_down(d)
            print(self.matrix, state)
            if state != 'not over':
                break  # game over
        print(strtg)
        return

    def key_down(self, dir):
        key = dir
        if key in self.commands:
            self.matrix, done, n, g = self.commands[dir](self.matrix)
            if done:
                self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
        return logic.game_state(self.matrix)

game_grid = GameGrid()
