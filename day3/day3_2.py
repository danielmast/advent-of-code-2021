# Read file
# Init list of counters per digit
# Iterate over lines
#   Split line in digits and add to counters per digit
#   Also keep track of total line count
# Compute for each digit if count >= 50% and store that in boolean list (called most_common)
# Init competing_for list with same length as lines and all values to 'Both'
# Compute ratings:
# Iterate over x-position of digits
#    Iterate over lines:
#        if competing_for[line_number] is not None:
#          If most_common[x] == line[x] and competing_for[line_number] != 'co2':
#            competing_for[line_number] = 'oxygen':
#          If most_common[x] != line[x] and competing_for[line_number] != 'oxygen':
#            competing_for[line_number] = 'co2':

def main():
    input = open('input.txt', 'r')
    lines = list(map(lambda line : line.strip(), input.readlines()))

    width = 12
    counts = [0] * width

    for line in lines:
        current_digits = digits(line)
        for i in range(0, width):
            counts[i] += current_digits[i]

    competing_for = ['both'] * len(lines)

    x = 0
    while not has_winners(competing_for):
        most_common_oxygen = most_common(x, lines, competing_for, 'oxygen')
        most_common_co2 = most_common(x, lines, competing_for, 'co2')
        for l in range(0, len(lines)):
            line = lines[l]
            if competing_for[l] is not None:
                if most_common_oxygen == int(line[x]) and competing_for[l] != 'co2':
                    competing_for[l] = 'oxygen'
                elif most_common_co2 == 1 - int(line[x]) and competing_for[l] != 'oxygen':
                    competing_for[l] = 'co2'
                elif count(competing_for, competing_for[l]) > 1 or competing_for[l] == 'both':
                    competing_for[l] = None

        x += 1

    oxygen_generator_rating = int(winner(lines, competing_for, 'oxygen'), 2)
    co2_scrubber_rating = int(winner(lines, competing_for, 'co2'), 2)
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    print(f'Oxygen generator rating = {oxygen_generator_rating}, CO2 scrubber rating = {co2_scrubber_rating}, life support rating = {life_support_rating}')


def most_common(x, lines, competing_for, rating):
    ones = 0
    total = 0
    for l in range(0, len(lines)):
        if competing_for[l] == rating or competing_for[l] == 'both':
            ones += int(lines[l][x])
            total += 1

    if total == 0:
        return None
    result = boolean_to_digit(ones / total >= 0.5)
    return result


def get_most_common(counts, number_of_lines):
    return list(map(lambda count: boolean_to_digit(count >= 0.5 * number_of_lines), counts))


def boolean_to_digit(b):
    if b:
        return 1
    else:
        return 0


def digits(binary_number):
    return [int(char) for char in binary_number]


def has_winners(competing_for):
    return count(competing_for, 'oxygen') == 1 and count(competing_for, 'co2') == 1


def winner(lines, competing_for, rating):
    for i in range(0, len(competing_for)):
        if competing_for[i] == rating:
            return lines[i]


def count(competing_for, rating):
    count = 0
    for i in competing_for:
        if i == rating:
            count += 1

    return count


if __name__ == "__main__":
    main()
