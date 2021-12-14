# Read file
# Read polymer
# Read rules in list
# Create insert function
# Copy input string in result string
# Iterate over input string. Check for every x and x+1 letter if it matches one of the rules
# If so, insert in result string
# Repeat 10 times
# Count occurrences of letters, get max and min
# Subtract max from min and return

def main():
    polymer, rules = read_file('input.txt')
    print(polymer)

    for step in range(0, 10):
        polymer = insert_step(polymer, rules)
        print(polymer)

    frequencies = get_frequencies(polymer)
    max_frequency, min_frequency = max_and_min_frequency(frequencies)
    print(f'Max - min frequency: {max_frequency - min_frequency}')

def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    polymer = lines[0].strip()
    rules = []

    for line in lines[2:]:
        pattern, insertion = line.strip().split(' -> ')
        rules.append([pattern, insertion])

    return polymer, rules

def insert_step(polymer, rules):
    result = polymer
    insert_count = 0

    e = 0
    for e in range(0, len(polymer) - 1):
        bit = polymer[e] + polymer[e+1]

        for rule in rules:
            if bit == rule[0]:
                split = e + 1 + insert_count
                result = result[:split] + rule[1] + result[split:]
                insert_count += 1

    return result


def get_frequencies(polymer):
    frequencies = {}
    for element in polymer:
        if element in frequencies.keys():
            frequencies[element] += 1
        else:
            frequencies[element] = 1
    return frequencies


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
