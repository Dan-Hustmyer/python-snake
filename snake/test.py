import curses
import threading
import time


window = curses.initscr()

def get_ch():
    while True:
        c = window.getch()
        window.addstr(0, 0, str(c))
        window.refresh()

t = threading.Thread(target=get_ch)
# print('starting thread')
t.start()
# print('started thread')


for i in range(3):
    window.addstr(10, 10 + i, 'test')

    window.refresh()

    time.sleep(1)

del window
