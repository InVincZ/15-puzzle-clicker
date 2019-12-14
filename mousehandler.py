import win32api, win32con, win32gui
import time
import random

def mousePositioner(current_pos, direction):
        win32api.SetCursorPos(current_pos)
        random_time = random.randrange(1, 3, 1)/10
        # print(random_time)
        time.sleep(random_time)
        switcher={
                'Left':(current_pos[0] - 39, current_pos[1]),
                'Right':(current_pos[0] + 39, current_pos[1]),
                'Up':(current_pos[0], current_pos[1] - 39),
                'Down':(current_pos[0], current_pos[1] + 39),
             }
        win32api.SetCursorPos(switcher.get(direction,"Invalid direction."))
        return switcher.get(direction,"Invalid direction.")

def leftClick(current_pos,delay):
    # mousePositioner((current_pos[0], current_pos[1]))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(delay)
    # print("Clicked position " + str(current_pos[0]) + ", " + str(current_pos[1]) + ": Delay=" + str(delay))  #completely optional. But nice for debugging purposes.


def main(starting_position, moves):
    # Position 1: (5507, 782)
    # Find starting position
    # starting_position = (1,1)
    # moves = ['up', 'left', 'down', 'right']
    # print(starting_position)
    # current_pos = (5507, 782)
    current_pos = (6885, 975)
    win32api.SetCursorPos(current_pos)

    for i in range(0, starting_position[1]):
        current_pos = mousePositioner(current_pos, 'Right')
    for j in range(0, starting_position[0]):
        current_pos = mousePositioner(current_pos, 'Down')

    moves = moves.split(",")
    moves = [x.strip(' ') for x in moves]
    # print(moves)
    # print(moves[0:-1])
    # Mouse now on starting position -> Start solving puzzle
    for i,m in enumerate(moves[0:-1]):
        print('Moves remaining: ' + str(len(moves[0:-1])-i) + ' - Current move: ' + m)
        current_pos = mousePositioner(current_pos, m)
        leftClick(current_pos,random.randrange(1, 4, 1)/10)


if __name__ == '__main__':
    main()
