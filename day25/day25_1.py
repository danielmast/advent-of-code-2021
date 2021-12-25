
# Read file
# Iterate over steps
# Per step:
# iterate over east-facing cucumbers just to check if they can move one location
# for all that can, move
# iterate over south-facing cucumbers just to check if they can move one location
# for all that can, move

# moving right means: (x + 1) % width
# moving south means: (y + 1) % height

def main():
    map, width, height = read_file('input.txt')

    print('Initial state:')
    print_map(map)

    s = 1
    has_moved = True
    while has_moved:
        has_moved = step(map, width, height)
        print(f'After {s} step:')
        print_map(map)
        s += 1


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    map = []
    for line in lines:
        map.append(list(line.strip()))

    width = len(map[0])
    height = len(map)

    return map, width, height


def step(map, width, height):
    has_moved = False

    can_move = [[False] * width for i in range(0, height)]
    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if map[y][x] == '>' and map[y][(x + 1) % width] == '.':
                can_move[y][x] = True
                has_moved = True

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if can_move[y][x]:
                if map[y][x] == '>':
                    map[y][x] = '.'
                    map[y][(x + 1) % width] = '>'

    can_move = [[False] * width for i in range(0, height)]

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if map[y][x] == 'v' and map[(y + 1) % height][x] == '.':
                can_move[y][x] = True
                has_moved = True

    for y in range(0, len(map)):
        for x in range(0, len(map[y])):
            if can_move[y][x]:
                if map[y][x] == 'v':
                    map[y][x] = '.'
                    map[(y + 1) % height][x] = 'v'
                else:
                    print('unexpected')

    return has_moved


def print_map(map):
    for row in map:
        print(''.join(row))
    print()


if __name__ == "__main__":
    main()
