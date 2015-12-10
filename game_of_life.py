import sys
import signal
import argparse
from time import sleep

GREEN = '\033[92m'
BLUE = '\033[94m'
ENDC = '\033[0m'

DEAD = GREEN + '0' + ENDC
ALIVE = BLUE + '1' + ENDC

TIME = 0.05
TERMINAL_HEIGHT = 45


def kill_handler(signal, frame):
    '''
    Signal handler for killing the execution.
    '''
    print('Thank you for playing.')
    sys.exit(0)


def parse_args(args):
    '''
    Parse command line arguments.
    '''
    parser = argparse.ArgumentParser(description='Parser of Game of Life application.')
    parser.add_argument('caller_name', metavar='caller_name', help='The name of the application script.')
    parser.add_argument('-f', '--input_file', metavar='input_file', required=True, help='The name of the file that contains world initial state.')
    parser.add_argument('-term', '--terminal_height', metavar='terminal_height', type=int, help='The height of the terminal where application runs.')
    parser.add_argument('-time', '--time', metavar='time_interval', help='The time interval in seconds between the display of two states of evolution.')
    args_list = parser.parse_args(args)
    args_dict = {}
    args_dict['filename'] = args_list.input_file
    args_dict['terminal_height'] = args_list.terminal_height if args_list.terminal_height else TERMINAL_HEIGHT
    args_dict['time'] = float(args_list.time) if args_list.time else TIME
    return args_dict


def grid_initialization(filename):
    '''
    Initialize grid from file.
    '''
    grid = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            cl = []
            for ch in line:
                if ch == '0':
                    cl.append(DEAD)
                elif ch == '1':
                    cl.append(ALIVE)
            grid.append(cl)
    return grid


def display(grid, term):
    '''
    Display the grid.
    '''
    outp = ''
    for row in grid:
        cl = ''
        for col in row:
            cl += col
        outp += cl + '\n'
    outp = outp.strip('\n')
    while len(outp.split('\n')) < term:
        outp += '\n'
    print(outp)


def life_decision(x, y, grid):
    '''
    Decide if a death or a birth occurs for a specific grid position.
    '''
    neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (x+i not in range(0, len(grid))) or (y+j not in range(0, len(grid[x+i]))) or ((i == 0) and (j == 0)):
                continue
            if grid[x+i][y+j] == ALIVE:
                neighbors += 1
    position = grid[x][y]
    if grid[x][y] == DEAD:
        if neighbors == 3:
            position = ALIVE
    else:
        if (neighbors < 2) or (neighbors > 3):
            position = DEAD
    return position


def evolve(grid):
    '''
    Evolve to the next state of the world.
    '''
    tmp = []
    for i in grid:
        tmp_ln = []
        for j in i:
            tmp_ln.append(DEAD)
        tmp.append(tmp_ln)
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            tmp[x][y] = life_decision(x, y, grid)
    return tmp


def main(args):
    signal.signal(signal.SIGINT, kill_handler)
    grid = grid_initialization(args['filename'])
    while True:
        display(grid, args['terminal_height'])
        grid = evolve(grid)
        sleep(args['time'])


if __name__ == '__main__':
    args = parse_args(sys.argv)
    main(args)
