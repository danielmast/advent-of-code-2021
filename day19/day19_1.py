
class Scanner:
    def __init__(self, id):
        self.id = id
        self.beacons = []
        self.beacon_pair_distances = None
        self.position = None
        self.orientation = None

    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def set_beacon_pair_distances(self):
        distances = []
        for beacon1 in self.beacons:
            for beacon2 in self.beacons:
                if beacon1 != beacon2:
                    distance = get_distance(beacon1, beacon2)
                    distances.append([beacon1, beacon2, distance])
        self.beacon_pair_distances = distances

    def beacon_pair_distance_matches(self, other_scanner):
        matches = []
        for distance1 in self.beacon_pair_distances:
            for distance2 in other_scanner.beacon_pair_distances:
                if is_equal_distance(distance1[2], distance2[2]):
                    matches.append(distance1 + distance2 + [get_orientations(distance1[2], distance2[2])])
        return matches


class BeaconGroup:
    def __init__(self):
        self.group = []

    def add(self, scanner_id, beacon):
        self.group.append([scanner_id, beacon])

    def is_in(self, other_scanner_id, other_beacon):
        for scanner_id, beacon in self.group:
            if scanner_id == other_scanner_id and beacon == other_beacon:
                return True
        return False

    def matches(self, other_beacon_group):
        for other_scanner_id, other_beacon in other_beacon_group.group:
            if self.is_in(other_scanner_id, other_beacon):
                return True
        return False

    def merge(self, other_beacon_group):
        merged = self.copy()
        for other_scanner_id, other_beacon in other_beacon_group.group:
            if not merged.is_in(other_scanner_id, other_beacon):
                merged.add(other_scanner_id, other_beacon)
        return merged

    def copy(self):
        c = BeaconGroup()
        for scanner_id, beacon in self.group:
            c.add(scanner_id, beacon)
        return c


def main():
    scanners = read_file('input.txt')

    for scanner in scanners:
        scanner.set_beacon_pair_distances()

    scanners[0].position = [0, 0, 0]
    scanners[0].orientation = ['z', 'y', 'x']

    scanner_overlaps = get_scanner_overlaps(scanners)
    get_scanner_positions(scanners, scanner_overlaps)

    unique_beacons = get_unique_beacons(scanners)

    print(unique_beacons)
    print(f'Length = {len(unique_beacons)}')


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    scanner_id = None
    scanners = []

    for line in lines:
        if line.startswith('---'):
            scanner_id = int(line.split(' ')[2])
            scanners.append(Scanner(scanner_id))
        elif line == '\n':
            continue
        else:
            x, y, z = list(map(int, line.strip().split(',')))
            scanners[scanner_id].add_beacon([x, y, z])

    return scanners


def beacon_to_string(beacon):
    return ','.join(list(map(str, beacon)))


def get_distance(beacon1, beacon2):
    return [
        beacon1[0] - beacon2[0],
        beacon1[1] - beacon2[1],
        beacon1[2] - beacon2[2]
    ]


def is_equal_distance(distance1, distance2):
    if abs(distance1[0]) not in list(map(abs, distance2)):
        return False

    if abs(distance1[1]) not in list(map(abs, distance2)):
        return False

    if abs(distance1[2]) not in list(map(abs, distance2)):
        return False

    return len(get_orientations(distance1, distance2)) > 0


def get_orientations(distance1, distance2):
    orientations = []

    for m in range(0, len(valid_manipulations())):
        if manipulate(distance1, valid_manipulations()[m]) == distance2:
            orientations.append(valid_orientations()[m])

    return orientations


def manipulate(position, manipulation):
    result = [None, None, None]

    for i in range(0, 3):
        if manipulation[i] == 'x':
            result[i] = position[0]
        elif manipulation[i] == '-x':
            result[i] = -1 * position[0]
        elif manipulation[i] == 'y':
            result[i] = position[1]
        elif manipulation[i] == '-y':
            result[i] = -1 * position[1]
        elif manipulation[i] == 'z':
            result[i] = position[2]
        elif manipulation[i] == '-z':
            result[i] = -1 * position[2]
        else:
            print('unexpected')

    return result


def reverse_manipulation(manipulation):
    result = [None, None, None]

    for i in range(0, 3):
        negation = ''
        if '-' in manipulation[i]:
            negation = '-'

        manip_axis = number_to_axis(i)
        if manipulation[i] == 'x':
            result[0] = negation + manip_axis
        elif manipulation[i] == '-x':
            result[0] = negation + manip_axis
        elif manipulation[i] == 'y':
            result[1] = negation + manip_axis
        elif manipulation[i] == '-y':
            result[1] = negation + manip_axis
        elif manipulation[i] == 'z':
            result[2] = negation + manip_axis
        elif manipulation[i] == '-z':
            result[2] = negation + manip_axis
    return result


def number_to_axis(number):
    if number == 0:
        return 'x'
    elif number == 1:
        return 'y'
    elif number == 2:
        return 'z'


def valid_orientations():
    return [
        # facing, up, right
        ['z', 'y', 'x'],
        ['z', '-y', '-x'],
        ['z', 'x', '-y'],
        ['z', '-x', 'y'],
        ['-z', 'y', '-x'],
        ['-z', '-y', 'x'],
        ['-z', 'x', 'y'],
        ['-z', '-x', '-y'],
        ['y', 'x', 'z'],
        ['y', '-x', '-z'],
        ['y', 'z', '-x'],
        ['y', '-z', 'x'],
        ['-y', 'x', '-z'],
        ['-y', '-x', 'z'],
        ['-y', 'z', 'x'],
        ['-y', '-z', '-x'],
        ['x', 'y', '-z'],
        ['x', '-y', 'z'],
        ['x', 'z', 'y'],
        ['x', '-z', '-y'],
        ['-x', 'y', 'z'],
        ['-x', '-y', '-z'],
        ['-x', 'z', '-y'],
        ['-x', '-z', 'y']
    ]


def valid_manipulations():
    manipulations = []
    for o in valid_orientations():
        manipulations.append([o[2], o[1], o[0]])
    return manipulations


def get_max_orientation(matches):
    occurrences = {}
    for match in matches:
        orientations = match[6]

        for orientation in orientations:
            orientation = ','.join(orientation)

            if orientation in occurrences.keys():
                occurrences[orientation] += 1
            else:
                occurrences[orientation] = 1

    max_orientation = None
    max_occurrence = 0
    for orientation in occurrences.keys():
        if occurrences[orientation] > max_occurrence:
            max_orientation = orientation
            max_occurrence = occurrences[orientation]

    print(f'max orientation = {max_orientation} ({max_occurrence})')
    return max_orientation.split(',')


def get_overlapping_beacon_groups(scanner1, scanner2):
    distance_matches = scanner1.beacon_pair_distance_matches(scanner2)
    print(f'#distance_matches: {len(distance_matches)}')

    if len(distance_matches) == 0:
        return [], None

    max_orientation = get_max_orientation(distance_matches)
    filtered_matches = filter_matches(distance_matches, max_orientation)

    beacon_groups = to_beacon_groups(scanner1, scanner2, filtered_matches)
    merged_beacon_groups = merge_beacon_groups_multiple(beacon_groups)

    print(f'#matching_beacons: {len(merged_beacon_groups)}')

    if len(merged_beacon_groups) >= 12:
        print('OVERLAP')
        return merged_beacon_groups, max_orientation

    return [], None


def get_scanner_positions(scanners, scanner_overlaps):
    for s in scanner_overlaps[0].keys():
        scanner = scanners[s]
        if scanner.position is None:
            get_position(scanner, scanners, scanner_overlaps, [0, scanner.id])


def get_position(scanner, scanners, scanner_overlaps, path):
    prev_scanner_id = path[len(path) - 2]
    prev_scanner = scanners[prev_scanner_id]
    beacon_groups = scanner_overlaps[prev_scanner_id][scanner.id]
    get_position_scanner2(prev_scanner, scanner, beacon_groups)

    for neighbour in scanner_overlaps[scanner.id]:
        if neighbour not in path:
            get_position(scanners[neighbour], scanners, scanner_overlaps, path + [neighbour])


def get_position_scanner2(scanner1, scanner2, beacon_groups):
    if len(beacon_groups[0]) == 0:
        return

    index_scanner1 = 0
    index_scanner2 = 1
    if scanner1.id > scanner2.id:
        index_scanner1 = 1
        index_scanner2 = 0
    scanner1_beacon1 = list(map(int, beacon_groups[0][0].group[index_scanner1][1].split(',')))
    scanner1_beacon2 = list(map(int, beacon_groups[0][1].group[index_scanner1][1].split(',')))
    scanner2_beacon1 = list(map(int, beacon_groups[0][0].group[index_scanner2][1].split(',')))
    scanner2_beacon2 = list(map(int, beacon_groups[0][1].group[index_scanner2][1].split(',')))

    absolute_scanner1_beacon1 = get_absolute(scanner1_beacon1, scanner1)
    absolute_scanner1_beacon2 = get_absolute(scanner1_beacon2, scanner1)

    scanner2_absolute_orientations = get_orientations(
        get_distance(absolute_scanner1_beacon1, absolute_scanner1_beacon2),
        get_distance(scanner2_beacon1, scanner2_beacon2)
    )

    if len(scanner2_absolute_orientations) > 1:
        print('unexpected')
    scanner2_absolute_orientation = scanner2_absolute_orientations[0]

    scanner2_relative_orientation = beacon_groups[1]

    manipulation_scanner2 = [
        scanner2_absolute_orientation[2],
        scanner2_absolute_orientation[1],
        scanner2_absolute_orientation[0],
    ]
    reversed_manipulation_scanner2 = reverse_manipulation(manipulation_scanner2)
    manipulated_scanner2_beacon1 = manipulate(scanner2_beacon1, reversed_manipulation_scanner2)

    scanner2.position = [
        absolute_scanner1_beacon1[0] - manipulated_scanner2_beacon1[0],
        absolute_scanner1_beacon1[1] - manipulated_scanner2_beacon1[1],
        absolute_scanner1_beacon1[2] - manipulated_scanner2_beacon1[2]
    ]

    scanner2.orientation = scanner2_absolute_orientation


def get_absolute(beacon, scanner):
    manipulation = [
        scanner.orientation[2],
        scanner.orientation[1],
        scanner.orientation[0],
    ]

    reversed_manipulation = reverse_manipulation(manipulation)
    manipulated = manipulate(beacon, reversed_manipulation)
    return [
        manipulated[0] + scanner.position[0],
        manipulated[1] + scanner.position[1],
        manipulated[2] + scanner.position[2]
    ]


def filter_matches(matches, max_orientation):
    filtered = []
    for match in matches:
        orientations = match[6]
        if max_orientation in orientations:
            filtered.append(match)
    return filtered


def to_beacon_groups(scanner1, scanner2, matches):
    beacon_groups = []
    for match in matches:
        beacon_group1 = BeaconGroup()
        beacon_group1.add(scanner1.id, beacon_to_string(match[0]))
        beacon_group1.add(scanner2.id, beacon_to_string(match[3]))
        beacon_groups.append(beacon_group1)
        beacon_group2 = BeaconGroup()
        beacon_group2.add(scanner1.id, beacon_to_string(match[1]))
        beacon_group2.add(scanner2.id, beacon_to_string(match[4]))
        beacon_groups.append(beacon_group2)
    return beacon_groups


def get_scanner_overlaps(scanners):
    overlaps = {}
    for s1 in range(0, len(scanners)):
        overlaps[s1] = {}

    for s1 in range(0, len(scanners)):
        scanner1 = scanners[s1]
        for s2 in range(s1 + 1, len(scanners)):
            scanner2 = scanners[s2]
            print(f'Scanner {s1} vs Scanner {s2}:')

            beacon_groups = get_overlapping_beacon_groups(scanner1, scanner2)

            if len(beacon_groups[0]) >= 12:
                overlaps[s1][s2] = beacon_groups
                overlaps[s2][s1] = beacon_groups
    return overlaps


def merge_beacon_groups(beacon_groups):
    result = []
    added = [False] * len(beacon_groups)
    for g1 in range(0, len(beacon_groups)):
        group1 = beacon_groups[g1]
        for g2 in range(g1 + 1, len(beacon_groups)):
            if added[g1] or added[g2]:
                continue

            group2 = beacon_groups[g2]

            if group1.matches(group2):
                merged = group1.merge(group2)
                result.append(merged)
                added[g1] = True
                added[g2] = True
        if not added[g1]:
            result.append(group1)
            added[g1] = True

    return result


def merge_beacon_groups_multiple(all_beacon_groups):
    previous_length = None
    merged = all_beacon_groups
    while previous_length is None or len(merged) < previous_length:
        previous_length = len(merged)
        merged = merge_beacon_groups(merged)

    return merged


def get_unique_beacons(scanners):
    beacons = []
    for scanner in scanners:
        for beacon in scanner.beacons:
            absolute_beacon = get_absolute(beacon, scanner)
            if absolute_beacon not in beacons:
                beacons.append(absolute_beacon)
    return beacons


if __name__ == "__main__":
    main()
