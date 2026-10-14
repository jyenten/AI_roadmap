numbers = [4, 9, 1, 7, 3]

def find_max(numbers):
    maximum = numbers[0]
    comparisons = 0

    for i in range(1, len(numbers)):
        comparisons += 1

        if numbers[i] > maximum:
            maximum = numbers[i]

    return maximum, comparisons

result, comparisons = find_max(numbers)

print("Nejvetsi cislo: ", result)
print("Pocet porovnani: ", comparisons)


def linear_count(numbers):
    operations = 0

    for number in numbers:
        operations += 1

    return operations

def quadratic_count(numbers):
    operations = 0

    for a in numbers:
        for b in numbers:
            operations += 1

    return operations

for n in [10, 100, 1000]:
    numbers = list(range(n))

    print("n =", n)
    print("O(n):", linear_count(numbers))
    print("O(n2): ", quadratic_count(numbers))
    print()
