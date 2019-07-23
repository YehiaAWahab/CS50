#include <cs50.h>
#include <stdio.h>

int get_positive_int_between_1_and_8(string prompt);

int main(void)
{
    int user_input = get_positive_int_between_1_and_8("Height: ");
    for(int i = 1; i <= user_input; i++)
    {
        for(int j = 1; j <= user_input - i; j++)
        {
            printf(" ");
        }
        for(int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for(int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

int get_positive_int_between_1_and_8(string prompt)
{
    int n;
    do
    {
        n = get_int("%s", prompt);
    }
    while(n < 1 || n > 8);
    return n;
}
