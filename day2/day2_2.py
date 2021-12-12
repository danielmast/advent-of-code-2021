
input = open('input.txt', 'r')
lines = input.readlines()

horizontal_position = 0
depth = 0
aim = 0

for line in lines:
    instruction, amount = line.split()
    amount = int(amount)

    if instruction == 'forward':
        horizontal_position += amount
        depth += aim * amount
    elif instruction == 'up':
        aim -= amount
    else:
        aim += amount

result = horizontal_position * depth
print(f'Horizontal position = {horizontal_position}, depth = {depth}, result = {result}')