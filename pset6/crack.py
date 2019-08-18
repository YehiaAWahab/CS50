from cs50 import get_string
from sys import argv
import crypt


def main():
    alphabet = ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    if len(argv) != 2:
        print("Usage crack.py hash")
        exit(1)

    salt = argv[1][:2]
    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            for k in range(len(alphabet)):
                for l in range(len(alphabet)):
                    for m in range(1, len(alphabet), 1):
                        password = ""
                        password += alphabet[m]
                        password += alphabet[l]
                        password += alphabet[k]
                        password += alphabet[j]
                        password += alphabet[i]
                        if crypt.crypt(password, salt) == argv[1]:
                            print(password)
                            exit(0)


if __name__ == "__main__":
    main()
