from cs50 import get_string
from sys import argv


def main():
    if len(argv) != 2:
        print("Usage: python bleep.py dictionary")
        exit(1)

    dictionary_set = set(line.strip() for line in open(argv[1], "r"))
    user_input = get_string("What message would you like to censor?\n")
    user_input_list = user_input.split(" ")
    censored_list = []
    for word_user in user_input_list:
        censored_word = ""
        if word_user.lower() in dictionary_set:
            for c in word_user:
                censored_word += "*"
            censored_list.append(censored_word)
        else:
            censored_list.append(word_user)

    censored_output = " ".join(censored_list)
    print(censored_output)


if __name__ == "__main__":
    main()
