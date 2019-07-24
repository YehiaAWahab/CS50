#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int intlen(long x);

int main(void)
{
    long credit_card = get_long("Number: ");
    if(intlen(credit_card) < 13 || intlen(credit_card) > 16)
    {
        printf("INVALID\n");
        return 0;
    }
    int total = 0;
    for(int i = 1; i <= intlen(credit_card); i += 2)
    {
        double divide = pow(10, i);
        long current_digit = (long) (credit_card / divide) % 10;
        current_digit *= 2;
        if(current_digit > 9)
        {
            for (int j = 0; j < intlen(current_digit); j++)
            {
                long divide2 = pow(10, j);
                long x = (long) (current_digit / divide2) % 10;
                total += x;
            }   
        }
        else
        {
            total += current_digit;
        }
    }

    for(int i = 0; i < intlen(credit_card); i += 2)
    {
        double divide = pow(10, i);
        long current_digit = (long) (credit_card / divide) % 10;
        total += current_digit;
    }

    
    if((total % 10) == 0)
    {

        double divide_first = pow(10, intlen(credit_card) - 1);
        double divide_second = pow(10, intlen(credit_card) - 2);
        long first_digit = (long) (credit_card / divide_first) % 10;
        long second_digit = (long) (credit_card / divide_second) % 10;

        if(first_digit == 4 && intlen(credit_card) >= 13 && intlen(credit_card) <= 16)
        {
            printf("VISA\n");
        }
        else if((second_digit == 1 || second_digit == 2
                || second_digit == 3
                || second_digit == 4
                || second_digit == 5) && first_digit == 5 && intlen(credit_card) == 16)
        {
            printf("MASTERCARD\n");
        }
        else if((second_digit == 4 || second_digit == 7) && first_digit == 3 && intlen(credit_card) == 15)
        {
            printf("AMEX\n");
        }
        else
        {
            printf("INVALID\n");
        }
        
    }
    else
    {
        printf("INVALID\n");
    }
    
}

int intlen(long x)
{
    char str[sizeof(int) * 16 + 1];
    sprintf(str, "%ld", x);
    return strlen(str);
}
