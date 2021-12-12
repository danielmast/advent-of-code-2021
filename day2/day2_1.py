# Read file
# Init horizontal position and depth
# Iterate over lines
# Split line by instruction and amount
# Decide on instruction which counter to modify
# In the end: print counters

input = open('input.txt', 'r')
lines = input.readlines()

horizontal_position = 0
depth = 0

for line in lines:
    instruction, amount = line.split()
    amount = int(amount)

    if instruction == 'forward':
        horizontal_position += amount
    elif instruction == 'up':
        depth -= amount
    else:
        depth += amount


print(f'Horizontal position = {horizontal_position}, depth = {depth}')