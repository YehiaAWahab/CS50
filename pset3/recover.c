#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        fprintf(stderr, "Usage ./recover filename\n");
        return 1;
    }
    FILE *cardptr = fopen(argv[1], "r");
    if (cardptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    uint8_t buffer[512];
    int counter = 0;
    char filename[8];
    FILE *jpg = NULL;
    bool found_a_jpg = false;

    while(fread(buffer, 512, 1, cardptr))
    {
        // Start of a new JPG?
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (found_a_jpg)
            {
                fclose(jpg);
                counter++;
            }

            sprintf(filename, "%03i.jpg", counter);
            jpg = fopen(filename, "w");
            fwrite(buffer, 512, 1, jpg);
            found_a_jpg = true;
        }
        else if (found_a_jpg)
        {
            fwrite(buffer, 512, 1, jpg);
        }
    }

}
