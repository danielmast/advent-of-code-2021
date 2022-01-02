
from day23.classes import Position, Setup

# Create initial 'setup'
# Determine neighbours of initial setup
# Administrate a table with shortest path from start setup to all others
# Administrate visited, unvisited setups


def main():
    setup = read_file('input.txt')
    setup.is_blocked()

    distances = find_distances(setup)
    energy = find_energy_to_organized_setup(distances)

    organized = get_organized_setup(distances)
    print_path_to(organized, distances)

    print(energy)


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    setup = Setup()
    for y in range(0, len(lines)):
        line = lines[y]
        for x in range(0, len(line)):
            c = lines[y][x]
            if c in ('A', 'B', 'C', 'D'):
                setup.add(c, Position(x, y))

    return setup


def find_distances(setup):
    visited = []
    unvisited = [setup]
    distances = {
        setup: [0, None]
    }

    current = [0, setup]
    i = 1
    total_number_of_neighbours = 0
    while len(unvisited) > 0:
        if (i - 1) % 100 == 0:
            print('len visited =', len(visited))
            print('len unvisited =', len(unvisited))
            print('avg #neighbours', total_number_of_neighbours / i)
            print('Current:')
            print(current[1])
            print()
        i += 1

        neighbours = current[1].get_relevant_neighbours()

        total_number_of_neighbours += len(neighbours)

        unvisited_neighbours = []
        for neighbour in neighbours:
            d = neighbour[0] + distances[current[1]][0]
            if neighbour[1] not in distances.keys() or d < distances[neighbour[1]][0]:
                distances[neighbour[1]] = [d, current[1]]
                if neighbour[1].is_organized():
                    organized = neighbour[1]
                    print('organized distance:', distances[organized])

            if neighbour[1] not in visited:
                unvisited_neighbours.append(neighbour)

        for neighbour in unvisited_neighbours:
            unvisited.append(neighbour[1])

        visited.append(current[1])
        unvisited.remove(current[1])

        if len(unvisited) == 0:
            return distances

        closest_neighbour = None
        closest_distance = None
        for neighbour in unvisited_neighbours:
            if closest_neighbour is None or neighbour[0] < closest_distance:
                closest_neighbour = neighbour[1]
                closest_distance = neighbour[0]

        if len(unvisited_neighbours) == 0:
            closest_unvisited_neighbour = get_closest_unvisited_neighbour(unvisited, distances)
            current = [distances[closest_unvisited_neighbour][0], closest_unvisited_neighbour]
        else:
            current = [distances[closest_neighbour][0], closest_neighbour]


def get_closest_unvisited_neighbour(unvisited, distances):
    closest_neighbour = None
    closest_distance = None
    for setup in unvisited:
        if closest_neighbour is None or distances[setup][0] < closest_distance:
            closest_neighbour = setup
            closest_distance = distances[setup][0]
    return closest_neighbour


def find_energy_to_organized_setup(distances):
    setup = get_organized_setup(distances)
    energy = distances[setup][0]
    return energy


def get_organized_setup(distances):
    for setup in distances.keys():
        if setup.is_organized():
            return setup


def print_path_to(setup, distances):
    path = []
    while setup is not None:
        path = [[distances[setup][0], setup]] + path
        setup = distances[setup][1]

    print('start:')
    for p in path:
        print(p[1])
        print('distance:', p[0])
        print()


if __name__ == "__main__":
    main()
