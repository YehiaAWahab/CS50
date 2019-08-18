from cs50 import get_string
from sys import argv


def main():
    if len(argv) != 2:
        print("Usage python caesar.py key")
        exit(1)
    key = int(argv[1])
    plaintext = get_string("plaintext: ")
    ciphertext = ""
    for p in plaintext:
        if p.isalpha():
            if p.isupper():
                ciphertext += chr(((ord(p) - ord('A')) + key) % 26 + ord('A'))
            elif p.islower():
                ciphertext += chr(((ord(p) - ord('a')) + key) % 26 + ord('a'))
        else:
            ciphertext += p

    print("ciphertext:", ciphertext)


if __name__ == "__main__":
    main()
