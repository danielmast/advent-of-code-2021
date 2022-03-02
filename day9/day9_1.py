# Read file
# Iterate over lines
#   Per line, split input and output values
# Iterate over lines again
#   Sum up output values with length 2, 4, 3, 7

def main():
    lines = read_file('input.txt')
    risk = risk_sum(lines)
    print(f'Risk = {risk}')


def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()

    lines = []

    for file_line in file_lines:
        lines.append(file_line.strip())

    return lines


def risk_sum(lines):
    sum = 0
    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(line)):
            risk = int(lines[y][x])

            top = None
            if y > 0:
                top = int(lines[y-1][x])

            bottom = None
            if y < len(lines) - 1:
                bottom = int(lines[y+1][x])

            left = None
            if x > 0:
                left = int(lines[y][x-1])

            right = None
            if x < len(lines[0]) - 1:
                right = int(lines[y][x+1])

            if is_low_point(risk, top, bottom, left, right):
                print(f'Low point: x = {x}, y = {y}, risk = {risk}')
                sum += risk + 1

    return sum


def is_low_point(risk, top, bottom, left, right):
    if top is None or top > risk:
        if bottom is None or bottom > risk:
            if left is None or left > risk:
                if right is None or right > risk:
                    return True
    return False


if __name__ == "__main__":
    main()
