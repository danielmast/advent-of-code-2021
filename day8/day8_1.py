# Read file
# Iterate over lines
#   Per line, split input and output values
# Iterate over lines again
#   Sum up output values with length 2, 4, 3, 7

def main():
    lines = read_file('input.txt')
    count = count_digits_1_4_7_8(lines)
    print(f'Count = {count}')


def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()

    lines = []

    for file_line in file_lines:
        split = file_line.split('|')
        input_values = split[0].split()
        output_values = split[1].split()
        lines.append([input_values, output_values])

    return lines


def count_digits_1_4_7_8(lines):
    count = 0
    for line in lines:
        for output_value in line[1]:
            if len(output_value) in [2, 4, 3, 7]:
                count += 1
    return count


if __name__ == "__main__":
    main()
