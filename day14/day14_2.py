# Parse the string and store the number of occurrences of each pattern in the rules
# Iterate over the rules
# Update the counts
# Example:
# ABCDE
# AB = 0, BC = 3, CD = 5
# Apply BC -> F (becoming ABFCDE)
# The new occurrences are: AB = 0, BC = 0, BF = BF + 3 (if this pattern exists in rules), FC = FC +3, CD = 5

# For every combination of two letters, store its occurring frequency
# Update those occurrences when a rule is applied
# In the end, iterate over occurrences to count number of occurrences per letter
# Copy occurrences before applying rules

def main():
    very_first_bit, very_last_bit, bit_frequencies, rules = read_file('input.txt')

    for step in range(0, 40):
        very_first_bit, very_last_bit, bit_frequencies = insert_step(very_first_bit, very_last_bit, bit_frequencies, rules)

    frequencies = get_frequencies(very_first_bit, very_last_bit, bit_frequencies)
    max_frequency, min_frequency = max_and_min_frequency(frequencies)
    print(f'Max - min frequency: {max_frequency - min_frequency}')

def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    polymer = lines[0].strip()
    first_bit = polymer[:2]
    last_bit = polymer[-2:]

    bit_frequencies = {}
    for i in range(0, len(polymer) - 1):
        bit = polymer[i] + polymer[i+1]
        if bit in bit_frequencies.keys():
            bit_frequencies[bit] += 1
        else:
            bit_frequencies[bit] = 1

    rules = []

    for line in lines[2:]:
        pattern, insertion = line.strip().split(' -> ')
        rules.append([pattern, insertion])

    return first_bit, last_bit, bit_frequencies, rules


def insert_step(very_first_bit, very_last_bit, bit_frequencies, rules):
    new_very_first_bit = None
    new_very_last_bit = None
    result = bit_frequencies.copy()

    for rule in rules:
        bit = rule[0]
        if bit in bit_frequencies.keys():
            first_letter = bit[0]
            second_letter = bit[1]
            middle_letter = rule[1]
            new_first_bit = first_letter + middle_letter
            new_second_bit = middle_letter + second_letter

            if new_first_bit in result.keys():
                result[new_first_bit] += bit_frequencies[bit]
            else:
                result[new_first_bit] = bit_frequencies[bit]

            if new_second_bit in result.keys():
                result[new_second_bit] += bit_frequencies[bit]
            else:
                result[new_second_bit] = bit_frequencies[bit]

            result[bit] -= bit_frequencies[bit]

            if new_very_first_bit is None and bit == very_first_bit:
                new_very_first_bit = new_first_bit
            elif new_very_last_bit is None and bit == very_last_bit:
                new_very_last_bit = new_second_bit

    return new_very_first_bit, new_very_last_bit, result


def get_frequencies(very_first_bit, very_last_bit, bit_frequencies):
    frequencies = {}
    for bit in bit_frequencies.keys():
        if bit == very_first_bit:
            add(frequencies, bit[0], 0.5 * bit_frequencies[bit] + 0.5)
            add(frequencies, bit[1], 0.5 * bit_frequencies[bit])
        elif bit == very_last_bit:
            add(frequencies, bit[0], 0.5 * bit_frequencies[bit])
            add(frequencies, bit[1], 0.5 * bit_frequencies[bit] + 0.5)
        else:
            add(frequencies, bit[0], 0.5 * bit_frequencies[bit])
            add(frequencies, bit[1], 0.5 * bit_frequencies[bit])
    return frequencies


def add(frequencies, element, number):
    if element in frequencies.keys():
        frequencies[element] += number
    else:
        frequencies[element] = number


def max_and_min_frequency(frequencies):
    max_element = None
    max_frequency = 0
    min_element = None
    min_frequency = 0

    for element in frequencies.keys():
        if max_element is None or max_frequency < frequencies[element]:
            max_element = element
            max_frequency = frequencies[element]
        if min_element is None or min_frequency > frequencies[element]:
            min_element = element
            min_frequency = frequencies[element]
    return max_frequency, min_frequency


if __name__ == "__main__":
    main()
