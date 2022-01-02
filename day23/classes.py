from copy import copy


def get_destination_room_xs():
    return {
        'A': 3,
        'B': 5,
        'C': 7,
        'D': 9
    }


def get_destination_rooms():
    destination_room_xs = get_destination_room_xs()
    destination_rooms = {}

    for letter in destination_room_xs.keys():
        positions = [
            Position(destination_room_xs[letter], 2),
            Position(destination_room_xs[letter], 3)
        ]
        destination_rooms[letter] = Room(letter, positions)

    return destination_rooms


def get_energy(letter):
    energies = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }
    return energies[letter]


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __copy__(self):
        return Position(self.x, self.y)

    def get_open_space_neighbours(self, burrow):
        open_space_neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if abs(dx) + abs(dy) != 1:
                    continue

                neighbour = Position(self.x + dx, self.y + dy)
                if burrow.burrow[neighbour.y][neighbour.x] == '.':
                    open_space_neighbours.append(neighbour)
        return open_space_neighbours

    def is_in_hallway(self):
        return self.x in range(1, 12) and self.y == 1

    def is_in_room(self):
        destination_rooms = get_destination_rooms()
        for letter in destination_rooms.keys():
            if self in destination_rooms[letter].positions:
                return True
        return False

    def is_in_destination_room(self, letter):
        return self in get_destination_rooms()[letter].positions

    def is_right_outside_room(self):
        return self.y == 1 and self.x in (3, 5, 7, 9)


class Room:
    def __init__(self, letter, positions):
        self.letter = letter
        self.positions = positions

    def is_empty(self, setup):
        for position in self.positions:
            if setup.get_amphipod_at_position(position) is not None:
                return False
        return True


class Setup:
    def __init__(self):
        self.setup = {
            'A': [],
            'B': [],
            'C': [],
            'D': []
        }

    def __eq__(self, other):
        if isinstance(other, Setup):
            return self.__key() == other.__key()
        return NotImplemented

    def __str__(self):
        empty_burrow = [
            list('#############'),
            list('#...........#'),
            list('###.#.#.#.###'),
            list('  #.#.#.#.#'),
            list('  #########')
        ]

        for letter in self.setup.keys():
            for position in self.setup[letter]:
                empty_burrow[position.y][position.x] = letter

        half_result = []
        for line in empty_burrow:
            half_result.append(''.join(line))

        return '\n'.join(half_result)

    def __key(self):
        aa = self.sort('A')
        bb = self.sort('B')
        cc = self.sort('C')
        dd = self.sort('D')

        return aa[0].x, aa[0].y, aa[1].x, aa[1].y, bb[0].x, bb[0].y, bb[1].x, bb[1].y, \
               cc[0].x, cc[0].y, cc[1].x, cc[1].y, dd[0].x, dd[0].y, dd[1].x, dd[1].y

    def sort(self, letter):
        l1 = self.setup[letter][0]
        l2 = self.setup[letter][1]
        if l1.x < l2.x:
            return [l1, l2]
        elif l1.x == l2.x:
            if l1.y < l2.y:
                return [l1, l2]

        return [l2, l1]

    def __hash__(self):
        return hash(self.__key())

    def is_organized(self):
        return Position(3, 2) in self.setup['A'] \
               and Position(3, 3) in self.setup['A'] \
               and Position(5, 2) in self.setup['B'] \
               and Position(5, 3) in self.setup['B'] \
               and Position(7, 2) in self.setup['C'] \
               and Position(7, 3) in self.setup['C'] \
               and Position(9, 2) in self.setup['D'] \
               and Position(9, 3) in self.setup['D']

    def add(self, letter, position):
        self.setup[letter].append(position)

    def get_amphipod_at_position(self, position):
        for letter in self.setup.keys():
            for pos in self.setup[letter]:
                if position == pos:
                    return letter
        return None

    def get_neighbours(self):
        neighbours = []

        for letter in self.setup.keys():
            for position in self.setup[letter]:
                neighbours += self.get_neighbours_for_amphipod(letter, position)

        return neighbours

    def get_relevant_neighbours(self):
        if self.is_organized():
            return []

        neighbours = self.get_neighbours()

        relevant = []
        for neighbour in neighbours:
            if neighbour[1].is_organized():
                return [neighbour]

            if neighbour[1].get_number_of_amphipods_in_destination_room() \
                    > self.get_number_of_amphipods_in_destination_room():
                relevant.append(neighbour)

        if len(relevant) == 0:
            return neighbours

        return relevant

    def get_number_of_amphipods_in_destination_room(self):
        count = 0
        for letter in self.setup.keys():
            for position in self.setup[letter]:
                if position.is_in_destination_room(letter):
                    count += 1
        return count

    def get_neighbours_for_amphipod(self, letter, position):
        goto_positions_with_distance = self.get_goto_positions_with_distance(letter, position)

        neighbours = []
        for goto_position_with_distance in goto_positions_with_distance:
            goto_position, distance = goto_position_with_distance
            neighbours.append(self.get_neighbour_by_move(letter, position, goto_position, distance))
        return neighbours

    def get_goto_positions_with_distance(self, letter, position):
        # Get all positions that can be reached by travelling through open space (dots)
        # Filter these positions by validity:
        # - Cannot be 'right outside' room
        # - Cannot be in room unless destination room, and room contains no other amphipod letters
        # - If from_position is in hallway, then goto_position must be in destination room
        # - Extra filters for efficiency:
        #   - from_position cannot be goto_position
        #   - If in destination room, and room is empty, then must be lowest spot
        #   - If from_position is in destination room and in lowest spot, then all moves are invalid
        #   - If from_position is in destination room and in highest spot, and lowest spot contains same letter,
        #     then all moves are invalid

        goto_positions_with_distance = [[position, 0]]

        previous_length = None
        while previous_length is None or previous_length < len(goto_positions_with_distance):
            previous_length = len(goto_positions_with_distance)
            for goto_position_with_distance in goto_positions_with_distance:
                goto_position = goto_position_with_distance[0]
                open_space_neighbours = self.get_open_space_neighbours(goto_position)
                for open_space_neighbour in open_space_neighbours:
                    goto_positions = []
                    for gpwd in goto_positions_with_distance:
                        goto_positions.append(gpwd[0])

                    if open_space_neighbour not in goto_positions:
                        goto_positions_with_distance.append([
                            open_space_neighbour,
                            goto_position_with_distance[1] + get_energy(letter)
                        ])

        filtered = []
        for goto_position_with_distance in goto_positions_with_distance:
            goto_position = goto_position_with_distance[0]

            if position == goto_position:
                continue
            elif self.will_block(letter, position, goto_position):
                continue
            elif goto_position.is_right_outside_room():
                continue
            elif position.is_in_hallway() and not goto_position.is_in_destination_room(letter):
                continue
            elif position.is_in_destination_room(letter) and position.y == 3:
                continue
            elif position.is_in_destination_room(letter) and position.y == 2 \
                    and self.get_amphipod_at_position(Position(position.x, 3)) == letter:
                continue
            elif goto_position.is_in_room():
                if goto_position.is_in_destination_room(letter):
                    destination_room = get_destination_rooms()[letter]
                    if goto_position.y == 2:
                        bottom_position = destination_room.positions[1]
                        if self.get_amphipod_at_position(bottom_position) != letter:
                            continue
                else:
                    continue

            filtered.append(goto_position_with_distance)

        return filtered

    def will_block(self, letter, from_position, goto_position):
        if not isinstance(from_position, Position) or not isinstance(goto_position, Position):
            print('debug')

        _, neighbour = self.get_neighbour_by_move(letter, from_position, goto_position, 0)
        return neighbour.is_blocked()

    def is_blocked(self):
        # If a letter X is in hallway, and
        # if X is to right of destination room
        #   and if letters left of X have destination rooms right of X
        #     then room is blocked
        # if X is to left of destination room
        #   and if letters right of X have destination rooms left of X
        #     then room is blocked

        for letter in self.setup.keys():
            for position in self.setup[letter]:
                if isinstance(position, list):
                    print('debug')
                if position.is_in_hallway():
                    if position.x > get_destination_room_xs()[letter]:
                        for letter2 in self.setup.keys():
                            for position2 in self.setup[letter2]:
                                if letter != letter2:
                                    if get_destination_room_xs()[letter] < position2.x \
                                            < position.x < get_destination_room_xs()[letter2]:
                                        return True
                    elif position.x < get_destination_room_xs()[letter]:
                        for letter2 in self.setup.keys():
                            for position2 in self.setup[letter2]:
                                if letter != letter2:
                                    if get_destination_room_xs()[letter2] < position.x \
                                            < position2.x < get_destination_room_xs()[letter]:
                                        return True

        return False

    def get_open_space_neighbours(self, position):
        empty_burrow = [
            '#############',
            '#...........#',
            '###.#.#.#.###',
            '  #.#.#.#.#',
            '  #########'
        ]

        open_space_neighbours = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if abs(dx) + abs(dy) != 1:
                    continue

                neighbour = Position(position.x + dx, position.y + dy)

                if empty_burrow[neighbour.y][neighbour.x] == '.' and self.get_amphipod_at_position(neighbour) is None:
                    open_space_neighbours.append(neighbour)
        return open_space_neighbours

    def get_neighbour_by_move(self, letter, from_position, goto_position, distance):
        if not isinstance(from_position, Position) or not isinstance(goto_position, Position):
            print('debug')

        neighbour = Setup()

        for l in self.setup.keys():
            for position in self.setup[l]:
                if l == letter and position == from_position:
                    neighbour.add(l, copy(goto_position))
                else:
                    neighbour.add(l, copy(position))

        return [distance, neighbour]
