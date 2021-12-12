
def main():
    lines = read_file('input.txt')
    output_values = get_output_values(lines)
    sum_output_values = sum(output_values)
    print(f'Sum of output values = {sum_output_values}')


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


def get_output_values(lines):
    output_values = []
    for line in lines:
        segments = get_segments(line[0])
        output_values.append(get_output_value(line[1], segments))
    return output_values


def get_output_value(output_value_parts, segments):
    output_value = ''
    for output_value_part in output_value_parts:
        output_value += get_output_value_part(output_value_part, segments)
    return int(output_value)


def get_output_value_part(output_value_part, segments):
    if is_zero(output_value_part, segments):
        return '0'
    elif is_one(output_value_part, segments):
        return '1'
    elif is_two(output_value_part, segments):
        return '2'
    elif is_three(output_value_part, segments):
        return '3'
    elif is_four(output_value_part, segments):
        return '4'
    elif is_five(output_value_part, segments):
        return '5'
    elif is_six(output_value_part, segments):
        return '6'
    elif is_seven(output_value_part, segments):
        return '7'
    elif is_eight(output_value_part, segments):
        return '8'
    elif is_nine(output_value_part, segments):
        return '9'
    else:
        raise Exception('No output value found')


def get_segments(input_values):
    one = get_1(input_values)
    four = get_4(input_values)
    seven = get_7(input_values)

    letter_frequencies = get_letter_frequencies(input_values)
    segments = {}
    segments['top'] = subtract(seven, one)
    segments['bottom_left'] = occurring_x_times(letter_frequencies, 4)
    segments['top_left'] = occurring_x_times(letter_frequencies, 6)
    segments['bottom_right'] = occurring_x_times(letter_frequencies, 9)
    segments['top_right'] = subtract(one, segments['bottom_right'])
    segments['middle'] = subtract(four, segments['top_left'] + segments['top_right'] + segments['bottom_right'])
    segments['bottom'] = subtract('abcdefg',
                                  segments['top'] + segments['bottom_left'] + segments['top_left']
                                  + segments['bottom_right'] + segments['top_right'] + segments['middle'])
    return segments


def get_1(input_values):
    return get_input_value_for_length(input_values, 2)


def get_4(input_values):
    return get_input_value_for_length(input_values, 4)


def get_7(input_values):
    return get_input_value_for_length(input_values, 3)


def get_input_value_for_length(input_values, length):
    for input_value in input_values:
        if len(input_value) == length:
            return input_value


def subtract(minuend, subtrahend):
    result = minuend
    for c in subtrahend:
        result = result.replace(c, '')
    return result


def get_letter_frequencies(input_values):
    letter_frequencies = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0}
    for input_values in input_values:
        for letter in input_values:
            letter_frequencies[letter] += 1
    return letter_frequencies


def occurring_x_times(letter_frequencies, x):
    for letter in letter_frequencies:
        if letter_frequencies[letter] == x:
            return letter


def is_zero(output_value, segments):
    return len(output_value) == 6 \
           and segments['top'] in output_value \
           and segments['top_left'] in output_value \
           and segments['top_right'] in output_value \
           and segments['bottom_left'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


def is_one(output_value, segments):
    return len(output_value) == 2 \
           and segments['top_right'] in output_value \
           and segments['bottom_right'] in output_value


def is_two(output_value, segments):
    return len(output_value) == 5 \
           and segments['top'] in output_value \
           and segments['top_right'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_left'] in output_value \
           and segments['bottom'] in output_value


def is_three(output_value, segments):
    return len(output_value) == 5 \
           and segments['top'] in output_value \
           and segments['top_right'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


def is_four(output_value, segments):
    return len(output_value) == 4 \
           and segments['top_left'] in output_value \
           and segments['top_right'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_right'] in output_value


def is_five(output_value, segments):
    return len(output_value) == 5 \
           and segments['top'] in output_value \
           and segments['top_left'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


def is_six(output_value, segments):
    return len(output_value) == 6 \
           and segments['top'] in output_value \
           and segments['top_left'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_left'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


def is_seven(output_value, segments):
    return len(output_value) == 3 \
           and segments['top'] in output_value \
           and segments['top_right'] in output_value \
           and segments['bottom_right'] in output_value


def is_eight(output_value, segments):
    return len(output_value) == 7 \
           and segments['top'] in output_value \
           and segments['top_left'] in output_value \
           and segments['top_right'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_left'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


def is_nine(output_value, segments):
    return len(output_value) == 6 \
           and segments['top'] in output_value \
           and segments['top_left'] in output_value \
           and segments['top_right'] in output_value \
           and segments['middle'] in output_value \
           and segments['bottom_right'] in output_value \
           and segments['bottom'] in output_value


if __name__ == "__main__":
    main()
