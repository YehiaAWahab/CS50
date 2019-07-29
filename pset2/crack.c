#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <crypt.h>
#include <string.h>


int main(int argc, string argv[])
{
    char alphabet[53] = {'\0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' };
    int alphabetc = 26 + 26 + 1;
    if (argc != 2)
    {
        printf("Usage: ./crack hash\n");
        return 1;
    }
    char salt[3];
    memcpy(salt, argv[1], 2);
    salt[2] = '\0';

    char password[6] = {'\0', '\0', '\0', '\0', '\0', '\0'};
    for (int i = 0; i < alphabetc; i++)
    {
        for (int j = 0; j < alphabetc; j++)
        {
            for (int k = 0; k < alphabetc; k++)
            {
                for (int l = 0; l < alphabetc; l++)
                {
                    for (int m = 1; m < alphabetc; m++)
                    {
                        password[0] = alphabet[m];
                        password[1] = alphabet[l];
                        password[2] = alphabet[k];
                        password[3] = alphabet[j];
                        password[4] = alphabet[j];
                        if (strcmp(crypt(password, salt), argv[1]) == 0)
                        {
                            printf("%s\n", password);
                            return 0;
                        }
                    }
                }
            }
        }
    }
}
