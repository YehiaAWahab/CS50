from cs50 import get_int


def main():
    user_input = get_positive_int("Height: ")
    for i in range(1, user_input + 1):
        for j in range(1, (user_input - i) + 1):
            print(" ", end="")

        for k in range(i):
            print("#", end="")

        print("  ", end="")

        for l in range(i):
            print("#", end="")

        print()


def get_positive_int(prompt):
    while True:
        n = get_int(prompt)
        if n >= 1 and n <= 8:
            return n


if __name__ == "__main__":
    main()
