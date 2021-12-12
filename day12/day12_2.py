
def main():
    graph = read_file('input.txt')
    paths = find_paths('start', 'end', ['start'], graph)
    print(f'Path count = {len(paths)}')


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    graph = {}

    for line in lines:
        start, end = line.strip().split('-')
        if start in graph.keys():
            graph[start].append(end)
        else:
            graph[start] = [end]

        if end in graph.keys():
            graph[end].append(start)
        else:
            graph[end] = [start]

    return graph


def find_paths(start, end, current_path, graph):
    if start == end:
        return [current_path]

    paths = []
    for neighbour in graph[start]:
        if is_valid_path(current_path + [neighbour]):
            paths += find_paths(neighbour, end, current_path + [neighbour], graph)
    return paths


def is_valid_path(path):
    visit_counts = get_visit_counts(path)
    small_caves_visited_twice_count = 0

    if ('start' in visit_counts.keys() and visit_counts['start'] != 1) \
            or ('end' in visit_counts.keys() and visit_counts['end'] != 1):
        return False

    for cave in visit_counts.keys():
        if cave == cave.lower():
            if visit_counts[cave] == 2:
                small_caves_visited_twice_count += 1
            if visit_counts[cave] > 2:
                return False

    if small_caves_visited_twice_count > 1:
        return False

    return True


def get_visit_counts(path):
    visit_counts = {}
    for cave in path:
        if cave in visit_counts.keys():
            visit_counts[cave] += 1
        else:
            visit_counts[cave] = 1
    return visit_counts


if __name__ == "__main__":
    main()
