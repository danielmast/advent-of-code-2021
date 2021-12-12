# Read file
# Store energy levels in 2D list
# Init flash counter
# Perform 100 steps
#  Per step:
#    Iterate over levels:
#      Level = (level + 1) % 10
#      if level == 0:
#        flash_counter += 1
#    Iterate over levels again, until number of flashes doesnt increase anymore:
#      if level > 0:
#        Level = (level + number of flashing neighbours) % 10
#        if level == 0:
#          flash_counter += 1
# Return flash counter

flash_count = 0

def main():
    levels = read_file('input.txt')
    print('Before any steps:')
    print_levels(levels)

    for step_number in range(1, 101):
        step(levels)

        print(f'After step {step_number}:')
        print_levels(levels)

    print(f'Flash count = {flash_count}')


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    levels = []

    for line in lines:
        row = digits(line)
        levels.append(row)

    return levels

def digits(line):
    return [int(char) for char in line.strip()]


def step(levels):
    for x in range(0, 10):
        for y in range(0, 10):
            levels[y][x] = (levels[y][x] + 1) % 10

    # print(f'After phase 1:')
    # print_levels(levels)

    previous_flash_count = None
    has_flashed = [[False]*10 for i in range(0, 10)]

    while previous_flash_count is None or previous_flash_count < flash_count:
        previous_flash_count = flash_count

        for x in range(0, 10):
            for y in range(0, 10):
                if levels[y][x] == 0 and not has_flashed[y][x]:
                    flash(levels, has_flashed, x, y)

        # print(f'After phase 2.x:')
        # print_levels(levels)


def flash(levels, has_flashed, x_in, y_in):
    for x in range(x_in - 1, x_in + 2):
        for y in range(y_in - 1, y_in + 2):
            if not (x == x_in and y == y_in) \
                    and x != -1 and x != len(levels) \
                    and y != -1 and y != len(levels) \
                    and levels[y][x] != 0:
                levels[y][x] = (levels[y][x] + 1) % 10
    has_flashed[y_in][x_in] = True
    global flash_count
    flash_count += 1


def flashing_neighbours_count(levels, old_flashes, x_in, y_in):
    count = 0
    for x in range(x_in - 1, x_in + 2):
        for y in range(y_in - 1, y_in + 2):
            if not (x == x_in and y == y_in) \
                    and x != -1 and x != len(levels) \
                    and y != -1 and y != len(levels)\
                    and levels[y][x] == 0\
                    and not old_flashes[y][x]:
                count += 1

    if count > 0:
        # print('')
        pass
    return count

def print_levels(levels):
    for row in levels:
        print(row)

    print()

if __name__ == "__main__":
    main()
