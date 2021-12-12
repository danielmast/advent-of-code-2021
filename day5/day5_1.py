# Read file
# Get max x and y coordinate
# Construct 2D list (called cover) of zeroes with size (y_max, x_max)
# Iterate over lines:
#   Init x, y to line_start
#   Increment x and y based on if line is horizontal/vertical, UNTIL (x,y) is line_end
#     Increment cover[y][x] with 1
# Iterate over cover list and count where >= 2

def main():
    width, height, lines = read_file('input.txt')
    cover = [[0] * width for h in range(height) ]

    draw_lines(lines, cover)
    min_draw = 2
    count = count_draws(cover, min_draw)

    print(f'Number of points where at least {min_draw} lines overlap = {count}')


def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()

    max_x = 0
    max_y = 0
    lines = []

    for file_line in file_lines:
        split = file_line.split()
        line_start = list(map(int, split[0].split(',')))
        line_end = list(map(int, split[2].split(',')))

        lines.append([line_start, line_end])

        if line_start[0] > max_x:
            max_x = line_start[0]
        if line_end[0] > max_x:
            max_x = line_end[0]
        if line_start[1] > max_y:
            max_y = line_start[1]
        if line_end[1] > max_y:
            max_y = line_end[1]

    return max_y + 1, max_y + 1, lines


def draw_lines(lines, cover):
    for line in lines:
        x = line[0][0]
        y = line[0][1]

        if not is_horizontal(line) and not is_vertical(line):
            continue

        end_reached = False
        while not end_reached:
            cover[y][x] += 1
            end_reached = x == line[1][0] and y == line[1][1]

            if is_horizontal(line):
                x += x_increment(line)
            elif is_vertical(line):
                y += y_increment(line)
            else:
                end_reached = True
                continue


def count_draws(cover, min_cover):
    count = 0
    for row in cover:
        for cell in row:
            if cell >= min_cover:
                count += 1

    return count


def is_horizontal(line):
    return line[0][1] == line[1][1]


def is_vertical(line):
    return line[0][0] == line[1][0]


def x_increment(line):
    if line[0][0] < line[1][0]:
        return 1
    else:
        return -1


def y_increment(line):
    if line[0][1] < line[1][1]:
        return 1
    else:
        return -1


if __name__ == "__main__":
    main()
