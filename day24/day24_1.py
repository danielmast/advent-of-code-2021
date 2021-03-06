from math import floor


def main():
    program = read_file('input.txt')

    input = find_largest_model_number(program)
    print('Largest input:', input)
    state = run(program, input)
    print('State:', state)


def read_file(input_file):
    input = open(input_file, 'r')
    lines = input.readlines()

    program = []
    for line in lines:
        program.append(line.strip().split())

    return program


def find_largest_model_number(program):
    subprograms = get_subprograms(program)
    memo = {
        14: {0: []}
    }

    for i in range(0, len(subprograms)):
        sp = len(subprograms) - 1 - i
        print('sp', sp)
        subprogram = subprograms[sp]
        for w in range(1, 10):
            for z in get_z_range(subprogram, sp, w, memo):
                for z_goal in memo[sp + 1].keys():
                    state = {
                        'i': 0,
                        'w': w,
                        'x': 0,
                        'y': 0,
                        'z': z
                    }
                    state = run(subprogram, w, state)
                    if state['z'] == z_goal:
                        insert(memo, sp, z, w, state['z'])

    return get_largest_input(memo)


def recursive(program, subprograms, input_thus_far, z_range):
    if len(input_thus_far) == 14:
        state = run(program, input_thus_far)
        if state['z'] == 0:
            print(input_thus_far)
            return input_thus_far
        else:
            return None

    sp = 13 - len(input_thus_far)
    if sp < 0 or sp >= len(subprograms):
        print('sp', sp, 'input_thus_far', input_thus_far, 'z_range', z_range)

    subprogram = subprograms[sp]
    for w_rev in range(1, 10):
        w = 10 - w_rev
        if sp == 0:
            new_z_range = [0]
        else:
            new_z_range = get_z_range_rec(subprogram, w, z_range)
        if len(new_z_range) > 0:
            result = recursive(program, subprograms, str(w) + input_thus_far, new_z_range)
            if result is not None:
                return result
    return None


def find_largest_model_number_recursive(program):
    subprograms = get_subprograms(program)
    return recursive(program, subprograms, '', [0])


def get_z_range(subprogram, sp, w, memo):
    z_range = memo[sp + 1].keys()
    early_addition = int(subprogram[5][2])
    addition = int(subprogram[15][2])
    filtered = []

    if int(subprogram[4][2]) == 1:
        for z in z_range:
            if (z - w - addition) % 26 == 0:
                filtered.append(int((z - w - addition) / 26))
    else:
        for z in z_range:
            if not z * 26 + w - early_addition in filtered:
                filtered.append(z * 26 + w - early_addition)
            if (z - w - addition) % 26 == 0:
                for a in range(0, 26):
                    q = int((z - w - addition) / 26) * 26 + a
                    if not q in filtered:
                        filtered.append(q)

    return filtered


def get_z_range_rec(subprogram, w, z_range):
    early_addition = int(subprogram[5][2])
    addition = int(subprogram[15][2])
    filtered = []

    if int(subprogram[4][2]) == 1:
        for z in z_range:
            if (z - w - addition) % 26 == 0:
                filtered.append(int((z - w - addition) / 26))
    else:
        for z in z_range:
            if not z * 26 + w - early_addition in filtered:
                filtered.append(z * 26 + w - early_addition)
            if (z - w - addition) % 26 == 0:
                for a in range(0, 26):
                    q = int((z - w - addition) / 26) * 26 + a
                    if not q in filtered:
                        filtered.append(q)

    return filtered


def insert(memo, sp, z, w, state_z):
    if sp not in memo.keys():
        memo[sp] = {}
    if z not in memo[sp].keys():
        memo[sp][z] = []
    memo[sp][z].append([w, state_z])


def get_largest_input(memo):
    input = ''

    prev_z = 0
    for sp in range(0, 14):
        found_w = False
        for w_rev in range(1, 10):
            if found_w:
                break
            w = 10 - w_rev
            for wz in memo[sp][prev_z]:
                if found_w:
                    break
                if w == wz[0]:
                    input += str(w)
                    prev_z = wz[1]
                    found_w = True
    return int(input)


def get_subprograms(program):
    subprograms = []
    subprogram = None
    for instruction in program:
        if instruction[0] == 'inp':
            subprograms.append(subprogram)
            subprogram = []
        subprogram.append(instruction)
    subprograms.append(subprogram)
    subprograms = subprograms[1:]
    return subprograms


def run(program, input, state=None):
    if state is None:
        state = {
            'i': 0,
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

    for instruction in program:
        if instruction[0] == 'inp':
            inp(instruction[1], input, state)
        elif len(instruction) == 3:
            if instruction[2].isalpha():
                argument2 = state[instruction[2]]
            else:
                argument2 = int(instruction[2])

            if instruction[0] == 'add':
                add(instruction[1], argument2, state)
            elif instruction[0] == 'mul':
                mul(instruction[1], argument2, state)
            elif instruction[0] == 'div':
                div(instruction[1], argument2, state)
            elif instruction[0] == 'mod':
                mod(instruction[1], argument2, state)
            elif instruction[0] == 'eql':
                eql(instruction[1], argument2, state)

        # print(f'{instruction} -> {state}')

    return state


def inp(variable, input, state):
    state[variable] = int(str(input)[state['i']])
    state['i'] += 1


def add(variable1, argument2, state):
    state[variable1] += argument2


def mul(variable1, argument2, state):
    state[variable1] *= argument2


def div(variable1, argument2, state):
    state[variable1] = floor(state[variable1] / argument2)


def mod(variable1, argument2, state):
    if state[variable1] < 0 or argument2 <= 0:
        raise ValueError('Invalid modulo input')

    state[variable1] %= argument2


def eql(variable1, argument2, state):
    if state[variable1] == argument2:
        state[variable1] = 1
    else:
        state[variable1] = 0


if __name__ == "__main__":
    main()
