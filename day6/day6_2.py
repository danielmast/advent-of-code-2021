# Read file
# Store numbers in list
# For the number of given days:
#   fishes[9] = fishes[0]
#   fishes[7] += fishes[0]
#   fishes[0] = 0
# For age in range(0, 9):
#   fishes[age] = fishes[age + 1]


#   Iterate over fishes and if value = 0, set it to 7 and append a 9 to the list
#   Iterate over fishes and decrease all by 1
# Return len(fishes)

def main():
    fishes = read_file('input.txt')
    print(f'Initial state: {fishes}')

    days = 256
    for d in range(0, days):
        fishes[9] = fishes[0]
        fishes[7] += fishes[0]
        fishes[0] = 0

        for age in range(0, 9):
            fishes[age] = fishes[age + 1]
        fishes[9] = 0

        print(f'After {d+1} days: {fishes}')

    print(f'Number of fishes = {sum(fishes)}')


def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()
    numbers = list(map(int, file_lines[0].split(',')))

    fishes = [0] * 10

    for number in numbers:
        fishes[number] += 1

    return fishes

if __name__ == "__main__":
    main()
