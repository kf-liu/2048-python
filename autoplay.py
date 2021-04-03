        import random
        
        import logic
        import constants as c
        
        
        def gen():
            return random.randint(0, c.GRID_LEN - 1)
        
        class GameGrid():
            def __init__(self):
        
                self.commands = {c.KEY_UP: logic.up, c.KEY_DOWN: logic.down, c.KEY_LEFT: logic.left, c.KEY_RIGHT: logic.right, c.KEY_UP_ALT: logic.up, c.KEY_DOWN_ALT: logic.down, c.KEY_LEFT_ALT: logic.left, c.KEY_RIGHT_ALT: logic.right, c.KEY_H: logic.left, c.KEY_L: logic.right, c.KEY_K: logic.up, c.KEY_J: logic.down}
        
                self.grid_cells = []
                self.matrix = logic.new_game(c.GRID_LEN)
                self.history_matrixs = []
        
                print(self.matrix)
                dir = [c.KEY_UP, c.KEY_DOWN, c.KEY_LEFT, c.KEY_RIGHT]
                while True:
                    state = self.key_down(dir[random.randint(0,len(dir)-1)])
                    print(self.matrix, state)
                    if state != 'not over':
                        break
        
            def key_down(self, dir):
                key = dir
                print(key)
                if key in self.commands:
                    self.matrix, done = self.commands[dir](self.matrix)
                    if done:
                        self.matrix = logic.add_two(self.matrix)
                        self.history_matrixs.append(self.matrix)
                return logic.game_state(self.matrix)
        
            def generate_next(self):
                index = (gen(), gen())
                while self.matrix[index[0]][index[1]] != 0:
                    index = (gen(), gen())
                self.matrix[index[0]][index[1]] = 2
        
        
        game_grid = GameGrid()
