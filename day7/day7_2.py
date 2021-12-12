
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

    cost_per_distance = get_cost_per_distance(len(counts))

    for c in range(0, len(costs)):
        for p in range(0, len(counts)):
            if c != p:
                costs[c] += cost_per_distance[abs(p - c)] * counts[p]

    return costs


def get_cost_per_distance(max_distance):
    cost_per_distance = [0] * max_distance
    for c in range(1, len(cost_per_distance)):
        cost_per_distance[c] = cost_per_distance[c - 1] + c

    return cost_per_distance

if __name__ == "__main__":
    main()
