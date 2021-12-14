# Read file
# Store dots in 2d list (=paper)
# Store the fold instructions in a list
# Write a function fold(axis, line)
# Write a function fold_x(line)
#   Create new 2d list with width = (width-1) / 2
#   First iterate over first paper until that column (and all rows) and copy into new paper
#   Then iterate over second paper, starting from other half of fold_line and copy into new paper (in reverse order)

def main():
    paper, instructions = read_file('input.txt')
    print_paper(paper)

    for instruction in instructions:
        paper = fold(paper, instruction)
        print_paper(paper)
        print(f'Dot count = {count_dots(paper)}')

    print_paper(paper)


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    width, height = get_dimensions(lines)
    paper = [['.'] * width for i in range(0, height)]

    instructions = []

    newline_reached = False
    for pos in lines:
        if not newline_reached:
            if pos == '\n':
                newline_reached = True
                continue

            x, y = list(map(int, pos.split(',')))
            paper[y][x] = '#'
        else:
            axis, pos = pos.split()[2].split('=')
            instructions.append([axis, int(pos)])

    return paper, instructions


def get_dimensions(lines):
    max_x = 0
    max_y = 0
    for line in lines:
        if line == '\n':
            return max_x + 1, max_y + 1

        x, y = list(map(int, line.split(',')))
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y


def fold(paper, instruction):
    if instruction[0] == 'x':
        return fold_x(paper, instruction[1])
    else:
        return fold_y(paper, instruction[1])


def fold_x(paper, line):
    old_width = len(paper[0])
    old_height = len(paper)
    new_width = line
    new_height = old_height
    folded = [['.'] * new_width for i in range(0, new_height)]

    for x in range(0, new_width):
        for y in range(0, old_height):
            folded[y][x] = paper[y][x]

    for x in range(new_width + 1, old_width):
        for y in range(0, old_height):
            if paper[y][x] == '#':
                folded[y][2 * new_width - x] = paper[y][x]

    return folded

def fold_y(paper, line):
    old_width = len(paper[0])
    old_height = len(paper)
    new_width = old_width
    new_height = line
    folded = [['.'] * new_width for i in range(0, new_height)]

    for x in range(0, old_width):
        for y in range(0, new_height):
            folded[y][x] = paper[y][x]

    for x in range(0, old_width):
        for y in range(new_height + 1, old_height):
            if paper[y][x] == '#':
                folded[2 * new_height - y][x] = paper[y][x]

    return folded


def print_paper(paper):
    for row in paper:
        print(''.join(row))
    print()


def count_dots(paper):
    count = 0
    for row in paper:
        for item in row:
            if item == '#':
                count += 1
    return count

if __name__ == "__main__":
    main()
