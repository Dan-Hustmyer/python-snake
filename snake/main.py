from random import randint
from tkinter import Tk, Canvas, Frame, BOTH


X, Y = (30, 20)
BLOCK_SIZE = 10

KEY_LEFT = 'Left'
KEY_RIGHT = 'Right'
KEY_UP = 'Up'
KEY_DOWN = 'Down'
KEY_P = 'p'

LEFT = 'LEFT'
UP = 'UP'
DOWN = 'DOWN'
RIGHT = 'RIGHT'
LEVEL_THRESHOLD = 2

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


def draw_rect(canvas, x, y, color = '#00f'):
    x1 = x * BLOCK_SIZE
    y1 = y * BLOCK_SIZE
    x2 = x1 + BLOCK_SIZE
    y2 = y1 + BLOCK_SIZE
    return canvas.create_rectangle(x1, y1, x2, y2, outline='', fill=color)


def render(canvas):
    canvas.delete('all')

    for x, y in snake:
        draw_rect(canvas, x, y)
    x, y = food
    draw_rect(canvas, x, y, color='#f00')


def is_inside_snake(next_point):
    for point in snake:
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

def move_snake(_direction):
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
        print('points: {}, speed: {}'.format(points, speed))

    else:
        snake.pop(0)

    x, y = next_point

    if x < 0 or x >= X or y < 0 or y >= Y:
        raise ValueError('You crashed into a wall!')

    if is_inside_snake(next_point):
        raise ValueError('You just ate yourself')

    snake.append(next_point)


def handle_next_movement():
    _direction = direction
    if move_queue:
        new_direction = move_queue.pop(0)
        if new_direction in VALID_MOVES[direction]:
            _direction = new_direction
    move_snake(_direction)


def main():
    root = Tk()
    root.geometry('{}x{}'.format(X * BLOCK_SIZE,
                                 Y * BLOCK_SIZE))

    frame = Frame()
    frame.master.title('Snake')
    frame.pack(fill=BOTH, expand=1)

    canvas = Canvas(frame)
    canvas.pack(fill=BOTH, expand=1)

    paused = False


    def on_press(event):
        nonlocal paused

        key = event.keysym
        print('key', key)

        if paused:
            paused = False
            tick()
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
            root.after_cancel(tick_job)
            paused = True

    tick_job = None

    def tick():
        nonlocal tick_job
        if not paused:
            handle_next_movement()
            tick_job = root.after(int(1000 / speed), tick)
        render(canvas)


    root.bind('<Key>', on_press)
    tick_job = tick()
    root.mainloop()


if __name__ == '__main__':
    main()
