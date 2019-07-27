#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    int key_index = 1;
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    int key = atoi(argv[key_index]);
    printf("Key: %i\n", key);
    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (islower(plaintext[i]))
        {

            printf("%c", ((plaintext[i] - 'a') + key) % 26 + 'a');
        }
        else if (isupper(plaintext[i]))
        {
            printf("%c", ((plaintext[i] - 'A') + key) % 26 + 'A');
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}
