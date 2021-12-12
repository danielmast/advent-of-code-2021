# Read file
# Init list of counters per digit
# Iterate over lines
#   Split line in digits and add to counters per digit
#   Also keep track of total line count
# In the end: construct gamma rate (list of digits)
#   Compute for each digit if count > 50%
#     If yes: set digit 1, if no: set digit 0
# Compute epsilon rate by inverting gamma rate
# Convert digit lists of gamma rate and epsilon rate to decimals: int('000001010000', 2) = 80
# Multiply rates (= power consumption)
# Print power consumption

def digits(binary_number):
    return [int(char) for char in binary_number.strip()]


input = open('input.txt', 'r')
lines = input.readlines()

width = 12
counts = [0] * width

for line in lines:
    current_digits = digits(line)
    for i in range(0, width):
        counts[i] += current_digits[i]

gamma_rate_binary = [0] * width
epsilon_rate_binary = [1] * width
for i in range(0, width):
    if counts[i] > 0.5 * len(lines):
        gamma_rate_binary[i] = 1
        epsilon_rate_binary[i] = 0

gamma_rate = int(''.join(map(str, gamma_rate_binary)), 2)
epsilon_rate = int(''.join(map(str, epsilon_rate_binary)), 2)
power_consumption = gamma_rate * epsilon_rate

print(f'Gamma rate = {gamma_rate}, epsilon rate = {epsilon_rate}, power consumption = {power_consumption}')
