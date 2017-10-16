from collections import deque
from random import randint
from tkinter import Tk, Canvas, Frame, BOTH

BLOCK_SIZE = 10

KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'
KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_QUIT = 'q'

VALID_DIRECTIONS = {
    KEY_LEFT: set((KEY_LEFT, KEY_UP, KEY_DOWN)),
    KEY_RIGHT: set((KEY_RIGHT, KEY_UP, KEY_DOWN)),
    KEY_UP: set((KEY_UP, KEY_LEFT, KEY_RIGHT)),
    KEY_DOWN: set((KEY_DOWN, KEY_LEFT, KEY_RIGHT))
}

MOVEMENTS = {
    KEY_LEFT: lambda x, y: (x - 1, y),
    KEY_RIGHT: lambda x, y: (x + 1, y),
    KEY_UP: lambda x, y: (x, y - 1),
    KEY_DOWN: lambda x, y: (x, y + 1)
}


class Snake:
    def __init__(self):
        self.direction = KEY_RIGHT
        self.points = deque(((5, 5), (5, 6), (6, 6), (7, 6)))
        self.moves = deque()

    def shorten(self):
        self.points.popleft()

    @property
    def next_move(self):
        direction = self.moves.popleft() if self.moves else self.direction
        u, w = self.points[-1]
        return MOVEMENTS[direction](u, w)

    def move(self, point):
        self.points.append(point)

    def add_move(self, direction):
        prev_direction = self.moves[-1] if self.moves else self.direction
        if direction in VALID_DIRECTIONS[prev_direction]:
            self.direction = direction
            self.moves.append(direction)

    @property
    def head(self):
        return self.points[-1]

    def is_at(self, point):
        return self.head == point

    def __contains__(self, point):
        points = set(self.points)
        return point in points


class Game:
    def __init__(self, snake, X, Y, level_threshold=2):
        self.snake = snake
        self.X = X
        self.Y = Y
        self.level_threshold = level_threshold
        self.food = (7, 8)
        self.score = 0
        self.speed = 5

    def add_score(self):
        self.food = self.gen_food()
        self.score += 1
        if not self.score % self.level_threshold:
            self.speed += 1
        print('points: {}, speed: {}'.format(self.score, self.speed))

    def gen_food(self):
        while True:
            food = randint(0, self.X - 1), randint(0, self.Y - 1)
            if food not in self.snake:
                return food

    def add_move(self, direction):
        self.snake.add_move(direction)

    def move_snake(self):
        snake = self.snake
        x, y = point = snake.next_move

        if x < 0 or x >= self.X or y < 0 or y >= self.Y:
            raise ValueError('You crashed into a wall!')

        if (x, y) in self.snake:
            raise ValueError('You just ate yourself!')

        snake.move(point)

        if snake.is_at(self.food):
            self.add_score()
        else:
            self.snake.shorten()


class UI(Frame):
    def __init__(self, window, game, snake_color='#00f', food_color='#f00'):
        super().__init__(window)
        self.window = window
        self.game = game
        self.snake_color = snake_color
        self.food_color = food_color

        self.master.title('Snake')
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(window)
        self.canvas.pack(fill=BOTH, expand=1)

    def draw_rect(self, x, y, color):
        canvas = self.canvas
        x1 = x * BLOCK_SIZE
        y1 = y * BLOCK_SIZE
        x2 = x1 + BLOCK_SIZE
        y2 = y1 + BLOCK_SIZE
        return canvas.create_rectangle(x1, y1, x2, y2, outline='', fill=color)

    def render(self):
        game = self.game
        self.canvas.delete('all')

        for x, y in game.snake.points:
            self.draw_rect(x, y, color=self.snake_color)
        x, y = game.food
        self.draw_rect(x, y, color=self.food_color)

    def on_press(self, event):
        window = self.window
        key = event.keysym

        if key in VALID_DIRECTIONS:
            self.game.add_move(key)
        elif key == KEY_QUIT:
            window.destroy()

    def tick(self):
        game = self.game
        game.move_snake()
        self.render()
        self.window.after(int(1000 / game.speed), self.tick)


def main(X=30, Y=20):
    window = Tk()
    window.geometry('{}x{}'.format(X * BLOCK_SIZE, Y * BLOCK_SIZE))
    window.resizable(False, False)
    game = Game(Snake(), X=X, Y=Y)
    ui = UI(window, game)
    window.bind('<Key>', ui.on_press)
    ui.tick()
    window.mainloop()


if __name__ == '__main__':
    main()
