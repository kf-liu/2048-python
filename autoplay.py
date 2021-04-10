import random

import logic
import constants as c

import csv


class GameGrid():

    def __init__(self, strtg="1.4.1"):

        # prepare game 2048

        self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down, c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right}

        self.grid_cells = []
        self.matrix = logic.new_game(c.GRID_LEN)
        self.history_matrixs = []
        self.history_matrixs.append(self.matrix)
        self.history_matrixs.append(self.matrix)
        self.score = 0
        
        # prepare game strategy
        strtg = strtg.split(".")
        for n, s in enumerate(strtg):
            strtg[n] = int(s)
        strtg.append(0)
        strtg.append(0)

        self.dir = []
        self.dirs = [c.KEY_UP, c.KEY_LEFT, c.KEY_RIGHT, c.KEY_DOWN]
        self.history_dir = -1
        self.line = 1
        
        # for strategy1 direction-first
        if strtg[0] == 1:
            if strtg[1] == 1:  # line
                self.set_dir([c.KEY_UP])
            elif strtg[1] == 2:  # corner
                self.set_dir([c.KEY_UP, c.KEY_LEFT])
            elif strtg[1] == 4:  # serpentine(snakelike)
                self.set_dir([c.KEY_UP, c.KEY_LEFT])
        
        # play
        while True:
            if strtg[0] == 0:
                d = self.dirs[random.randint(0,len(self.dirs)-1)]
            elif strtg[0] == 1:
                # for strategy1.4 serpentine(snakelike), when change direction
                if strtg[1] == 4 and self.matrix[0][c.GRID_LEN - 1] != 0 and self.matrix[0][0] != 0:
                    if strtg[2] == 0 and self.matrix[0][0] == 256:
                        self.set_dir([c.KEY_UP, c.KEY_RIGHT])
                    if strtg[2] == 1 :
                        # main direction
                        if self.matrix[0][c.GRID_LEN - 1] > 8:
                            if self.matrix[0][0] == 128:
                                self.set_dir([c.KEY_UP])
                            elif self.matrix[0][0] == 256:
                                self.set_dir([c.KEY_UP, c.KEY_RIGHT])
                            elif self.matrix[0][0] == 512:
                                self.set_dir([c.KEY_UP, c.KEY_RIGHT])
                        elif self.matrix[0][c.GRID_LEN - 1] < 4:
                            self.set_dir([c.KEY_UP])
                        # consider more lines
                        if self.matrix[0][0] < 256:
                            self.line = 1
                        ##else:
                            ##self.line = 2
                        # disoder
                        for i in range(self.line):
                            for j in range(c.GRID_LEN - 1):
                                if self.matrix[i][j] < self.matrix[i][j+1]:
                                    self.set_dir([c.KEY_UP, c.KEY_LEFT])
                        if c.KEY_RIGHT in self.dir and self.matrix[0][c.GRID_LEN - 1] < self.matrix[1][c.GRID_LEN - 1]:
                            self.set_dir([c.KEY_UP])
                # for strategy1, when invalid direction
                d = self.dup()
                print("1", d, self.dir)
                if d == "continue":
                    continue
                if d == "not dup":
                    self.history_dir = -1
                    d = self.dir[random.randint(0, len(self.dir)-1)]
                if d == c.KEY_RIGHT and d in self.dir:
                    m, done, n, g = self.commands[d](self.matrix)
                    if m[0][0] == 0:
                        self.set_dir([c.KEY_UP])
                        continue
            elif strtg[0] == 2:
                d = self.more_merged(strtg[1])
                if d == "not dup":
                    d = self.dirs[random.randint(0,len(self.dirs)-1)]
            # key down
            print("2", d)
            state = self.key_down(d)
            print(self.matrix)
            if state != 'not over':
                break  # game over
##        self.record(strtg)
        return

    def key_down(self, dir):
        key = dir
        if key in self.commands:
            self.matrix, done, n, g = self.commands[dir](self.matrix)
            self.score += n * 2
            if done:
                self.matrix = logic.add_two(self.matrix)
            self.history_matrixs.append(self.matrix)
        return logic.game_state(self.matrix)
        
    def set_dir(self, dir):
        self.dirs = [c.KEY_UP, c.KEY_LEFT, c.KEY_RIGHT, c.KEY_DOWN]
        self.dir = dir
        for d in dir:
            self.dirs.remove(d)
    
    def dup(self):
        if self.matrix == self.history_matrixs[-2]:  # duplicate
            self.history_dir = self.history_dir + 1
            if self.history_dir < len(self.dir):  # try wanted directions
                d = self.dir[self.history_dir]
                return d
            else:  # try other directions
                print(self.history_dir, self.dir, len(self.dir))
                d = self.dirs[self.history_dir - len(self.dir)]
                print("3", d)
                if d in [c.KEY_RIGHT, c.KEY_DOWN]:
                    self.key_down(d)
                    self.key_down(self.oppo(d))
                    return "continue"
                else:
                    return d
        else:
            return "not dup"
            
    def more_merged(self, n_g):
        merged = []
        for d in self.dirs:
            m, d, n, g = self.commands[d](self.matrix)
            l = [n,g]
            merged.append(l[n_g-1])
        for md in merged:
            if md != 0:
                d = self.dirs[merged.index(max(merged))]
                return d
        if d != self.dirs[merged.index(max(merged))]:
            return False
            
    def max(self):
        max = 2
        for i in self.matrix:
            for j in i:
                if j > max:
                    max = j
        return max
        
    def record(self, strtg):
        max = self.max()
        csv_writer.writerow([strtg[0], strtg[1], strtg[2], max, self.score])
        return True
    
    def oppo(self, dir):
        dirs = [c.KEY_UP, c.KEY_LEFT, c.KEY_DOWN, c.KEY_RIGHT]
        return dirs[(dirs.index(dir) + 2) % 4]


if False:
    f = open('detail.csv','a+',encoding='utf-8')  # count details
    csv_writer = csv.writer(f)
    ss = ['0', '1.1', '1.2', '1.4', '2.1', '2.2']
    for s in ss:
        print(s)
        for i in range(1000):
            if i % 100 == 0:
                print(i)
            game_grid = GameGrid(s)
    f.close()

if False:
    f = open('total.csv','w',encoding='utf-8')  # count total numbers
    csv_writer = csv.writer(f)
    csv_writer.writerow(["","s","s0","s1","s2","s1.1","s1.2","s1.4","s2.1","s2.2","s2.1.0","s2.1.1","s2.2.0","s2.2.1"])
    f.close()

game_grid = GameGrid()
