# Read file
# Store numbers in list
# Init counts list with size = max(numbers_list) + 1
# Iterate over list and increment count for that position
# Init cost list with size = len(counts)
#   For cost_index in range(0, len(counts))
#     costs[cost_index] = 0
#     For position in range(0, len(counts))
#       costs[cost_index] += (position - cost_index) * counts[position]
# Get position of min(costs)

def main():
    crab_positions = read_file('input.txt')
    print(crab_positions)

    counts = get_counts(crab_positions)
    print(counts)

    costs = get_costs(counts)
    print(costs)

    min_cost = min(costs)
    print(f'Min cost = {min_cost}')



def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()
    return list(map(int, file_lines[0].split(',')))


def get_counts(crab_positions):
    counts = [0] * (max(crab_positions) + 1)

    for crab in crab_positions:
        counts[crab] += 1

    return counts


def get_costs(counts):
    costs = [0] * len(counts)

    for c in range(0, len(costs)):
        for p in range(0, len(counts)):
            if c != p:
                costs[c] += abs(p - c) * counts[p]

    return costs

if __name__ == "__main__":
    main()
