# Read file
# Init depth increase counter = 0
# Iterate over lines
# if depth > previous depth -> counter++
# print counter

input = open('input.txt', 'r')
lines = input.readlines()

depth_increase_count = 0
previous_depth = None

for line in lines:
    depth = int(line)

    if previous_depth is not None and depth > previous_depth:
        depth_increase_count += 1

    previous_depth = depth

print(f'Depth increase count = {depth_increase_count}')