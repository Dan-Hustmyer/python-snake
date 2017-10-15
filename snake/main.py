from random import randint
import curses
import subprocess
import threading
import time

LEFT = 'LEFT'
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
SNAKE_CHAR = '█'
FOOD_CHAR = '*'
LEVEL_THRESHOLD = 2

X, Y = (30, 20)

VALID_MOVES = {
    LEFT: set((LEFT, UP, DOWN)),
    RIGHT: set((RIGHT, UP, DOWN)),
    UP: set((UP, LEFT, RIGHT)),
    DOWN: set((DOWN, LEFT, RIGHT))
}

snake = [(5, 5), (5, 6), (6, 6), (7, 6)]
food = (7,8)
direction = RIGHT
move_queue = []
points = 0
speed = 5
paused = False


def render(window):
    for x, y in snake:
        window.addch(y, x, SNAKE_CHAR)
    x, y = food
    window.addch(y, x, FOOD_CHAR)
    status = 'points: {}, speed: {}   '.format(points, speed)
    window.addstr(Y + 2, 0, status)
    window.refresh()


def is_inside_snake(next_point):
    for point in snake:
        if next_point == point:
            return True
    return False


def _gen_food ():
    x = randint(0, X - 1)
    y = randint(0, Y - 1)
    return (x, y)

def gen_food ():
    food = _gen_food()
    while is_inside_snake(food):
        food = _gen_food()
    return food

def move_snake(window, _direction):
    global direction
    global food
    global points
    global speed
    direction = _direction
    x, y = snake[-1]

    if direction == LEFT:
        next_point = (x - 1, y)
    elif direction == UP:
        next_point = (x, y - 1)
    elif direction == DOWN:
        next_point = (x, y + 1)
    elif direction == RIGHT:
        next_point = (x + 1, y)
    else:
        raise ValueError('Invalid direction: ' + direction)

    if next_point == food:
        food = gen_food()
        points += 1
        if not points % LEVEL_THRESHOLD:
            speed += 2
    else:
        x, y = snake.pop(0)
        window.addch(y, x, ' ')

    x, y = next_point

    if x < 0 or x >= X or y < 0 or y >= Y:
        raise ValueError('You crashed into a wall!')

    if is_inside_snake(next_point):
        raise ValueError('You just ate yourself')

    snake.append(next_point)


def handle_next_movement(window):
    global move_queue
    _direction = direction
    if move_queue:
        new_direction = move_queue.pop(0)
        if new_direction in VALID_MOVES[direction]:
            _direction = new_direction
    move_snake(window, _direction)

KEY_LEFT = 260
KEY_RIGHT = 261
KEY_UP = 259
KEY_DOWN = 258
KEY_P = 112


def on_press(key):
    global move_queue
    global paused

    if paused:
        paused = False
        return

    if key == KEY_LEFT:
        move_queue.append(LEFT)
    elif key == KEY_UP:
        move_queue.append(UP)
    elif key == KEY_DOWN:
        move_queue.append(DOWN)
    elif key == KEY_RIGHT:
        move_queue.append(RIGHT)
    elif key == KEY_P:
        paused = True


def start_loop(window):
    def get_ch():
        while True:
            key = window.getch()
            on_press(key)

    t = threading.Thread(target=get_ch)
    t.start()

    for y in range(Y):
        window.addch(y, X, '|')
    for x in range(X):
        window.addch(Y, x, '-')

    while True:
        if not paused:
            handle_next_movement(window)
        render(window)
        time.sleep(1 / speed)


def main():
    curses.wrapper(start_loop)


if __name__ == '__main__':
    main()
