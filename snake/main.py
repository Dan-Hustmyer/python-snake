from collections import deque
from random import randint
from tkinter import Tk, Canvas, Frame, BOTH

X, Y = (30, 20)
BLOCK_SIZE = 10

KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'
KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_PAUSE = 'p'
KEY_QUIT = 'q'
KEY_RESTART = 'n'

LEFT = 'LEFT'
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEVEL_THRESHOLD = 2
SNAKE_COLOR = '#00f'
FOOD_COLOR = '#f00'

DIRECTIONS_BY_KEY = {
    KEY_LEFT: LEFT,
    KEY_RIGHT: RIGHT,
    KEY_UP: UP,
    KEY_DOWN: DOWN
}

VALID_MOVES = {
    LEFT: set((LEFT, UP, DOWN)),
    RIGHT: set((RIGHT, UP, DOWN)),
    UP: set((UP, LEFT, RIGHT)),
    DOWN: set((DOWN, LEFT, RIGHT))
}


class Game:
    def __init__(self):
        self.snake = deque(((5, 5), (5, 6), (6, 6), (7, 6)))
        self.food = (7, 8)
        self.direction = RIGHT
        self.moves = deque()
        self.points = 0
        self.speed = 5
        self.paused = False


game = Game()

window = Tk()
window.geometry('{}x{}'.format(X * BLOCK_SIZE, Y * BLOCK_SIZE))

frame = Frame()
frame.master.title('Snake')
frame.pack(fill=BOTH, expand=1)

canvas = Canvas(frame)
canvas.pack(fill=BOTH, expand=1)

tick_job = None


def draw_rect(canvas, x, y, color=SNAKE_COLOR):
    x1 = x * BLOCK_SIZE
    y1 = y * BLOCK_SIZE
    x2 = x1 + BLOCK_SIZE
    y2 = y1 + BLOCK_SIZE
    return canvas.create_rectangle(x1, y1, x2, y2, outline='', fill=color)


def render(canvas):
    # this could be optimized by moving the tail to the head, or just appending
    # the head when the snake eats
    canvas.delete('all')

    for x, y in game.snake:
        draw_rect(canvas, x, y)
    x, y = game.food
    draw_rect(canvas, x, y, color=FOOD_COLOR)


def is_inside_snake(next_point):
    for point in game.snake:
        if next_point == point:
            return True
    return False


def _gen_food():
    x = randint(0, X - 1)
    y = randint(0, Y - 1)
    return (x, y)


def gen_food():
    food = _gen_food()
    while is_inside_snake(food):
        food = _gen_food()
    return food


def get_next_point(direction):
    game.direction = direction
    x, y = game.snake[-1]

    if direction == LEFT:
        return (x - 1, y)
    elif direction == UP:
        return (x, y - 1)
    elif direction == DOWN:
        return (x, y + 1)
    elif direction == RIGHT:
        return (x + 1, y)
    else:
        raise ValueError('Invalid direction: ' + direction)


def move_snake(direction):
    next_point = get_next_point(direction)

    if next_point == game.food:
        game.food = gen_food()
        game.points += 1
        if not game.points % LEVEL_THRESHOLD:
            game.speed += 2
        print('points: {}, speed: {}'.format(game.points, game.speed))

    else:
        game.snake.popleft()

    x, y = next_point

    if x < 0 or x >= X or y < 0 or y >= Y:
        raise ValueError('You crashed into a wall!')

    if is_inside_snake(next_point):
        raise ValueError('You just ate yourself')

    game.snake.append(next_point)


def handle_next_movement():
    direction = game.moves.popleft() if game.moves else game.direction
    game.direction = direction
    move_snake(direction)


def add_move(direction):
    prev_direction = game.moves[-1] if game.moves else game.direction
    if direction in VALID_MOVES[prev_direction]:
        game.moves.append(direction)


def on_press(event):
    global game
    key = event.keysym

    if game.paused:
        game.paused = False
        tick()
        return

    if key in DIRECTIONS_BY_KEY:
        add_move(DIRECTIONS_BY_KEY[key])
    elif key == KEY_PAUSE:
        window.after_cancel(tick_job)
        game.paused = True
    elif key == KEY_QUIT:
        window.destroy()
    elif key == KEY_RESTART:
        game = Game()
        window.after_cancel(tick_job)
        tick()


def tick():
    global tick_job
    if not game.paused:
        handle_next_movement()
        tick_job = window.after(int(1000 / game.speed), tick)
    render(canvas)


def main():
    window.bind('<Key>', on_press)
    window.resizable(False, False)
    tick()
    window.mainloop()


if __name__ == '__main__':
    main()
