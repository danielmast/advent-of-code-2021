# Read file
# Store numbers in list
# For the number of given days:
#   Iterate over fishes and if value = 0, set it to 7 and append a 9 to the list
#   Iterate over fishes and decrease all by 1
# Return len(fishes)

def main():
    fishes = read_file('input.txt')

    days = 80
    for d in range(0, days):
        for f in range(0, len(fishes)):
            fish = fishes[f]
            if fish == 0:
                fishes[f] = 7
                fishes.append(9)

        for f in range(0, len(fishes)):
            fishes[f] -= 1

    print(f'Fishes = {fishes}')
    print(f'Length = {len(fishes)}')


def read_file(input_file):
    input = open(input_file, 'r')
    file_lines = input.readlines()
    return list(map(int, file_lines[0].split(',')))


if __name__ == "__main__":
    main()
