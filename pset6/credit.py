from cs50 import get_int


def main():
    credit_card = get_int("Number: ")

    if len(str(credit_card)) < 13 or len(str(credit_card)) > 16:
        print("INVALID")
        exit(0)

    total = 0
    for i in range(1, len(str(credit_card)) + 1, 2):
        divide = 10 ** i
        current_digit = (credit_card // divide) % 10
        current_digit *= 2
        if current_digit > 9:
            for j in range(len(str(current_digit))):
                divide2 = 10 ** j
                x = (current_digit // divide2) % 10
                total += x
        else:
            total += current_digit

    for k in range(0, len(str(credit_card)), 2):
        divide3 = 10 ** k
        current_digit = (credit_card // divide3) % 10
        total += current_digit

    if (total % 10) == 0:
        divide_first = 10 ** (len(str(credit_card)) - 1)
        divide_second = 10 ** (len(str(credit_card)) - 2)
        first_digit = (credit_card // divide_first) % 10
        second_digit = (credit_card // divide_second) % 10

        if first_digit == 4 and len(str(credit_card)) >= 13 and len(str(credit_card)) <= 16:
            print("VISA")

        elif first_digit == 5 and (second_digit == 1 or second_digit == 2 or second_digit == 3 or second_digit == 4 or second_digit == 5) and len(str(credit_card)) == 16:
            print("MASTERCARD")

        elif first_digit == 3 and (second_digit == 4 or second_digit == 7) and len(str(credit_card)) == 15:
            print("AMEX")

        else:
            print("INVALID")
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
