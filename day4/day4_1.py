# Read file
# Read chosen numbers
# Read bingo boards
# Iterate over numbers, cross off on each bingo board (if present)
# Check if a bingo board has won
# Compute score of that bingo board

def main():
    numbers, boards = read_file('input.txt')
    cross_off_numbers(numbers, boards)


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    numbers = list(map(int, lines[0].split(',')))
    boards = read_boards(lines[2:])

    return numbers, boards


def read_boards(lines):
    boards = [[]]
    board_counter = 0

    for line in lines:
        if line == '\n':
            board_counter += 1
            boards.append([])
        else:
            row = list(map(int, line.split()))
            boards[board_counter].append(row)

    return boards


def cross_off_numbers(numbers, boards):
    for number in numbers:
        for board in boards:
            cross_off_number(number, board)
            if (has_won(board)):
                score = compute_score(number, board)
                print(f'Board has won with score: {score}')
                return


def has_won(board):
    for row in board:
        if sum(row) == -5:
            return True

    for column_index in range(0, 5):
        column_sum = 0
        for row in board:
            column_sum += row[column_index]

        if column_sum == -5:
            return True

    return False


def compute_score(number, board):
    unmarked_sum = 0
    for row in board:
        for cell in row:
            if cell != -1:
                unmarked_sum += cell
    return unmarked_sum * number


def cross_off_number(number, board):
    for row in board:
        try:
            index = row.index(number)
            row[index] = -1
        except ValueError:
            pass

if __name__ == "__main__":
    main()
