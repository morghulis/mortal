#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <time.h>
#include <errno.h>
#include "../rune.h"

int runcases(int argc, char *argv[], int filelog)
{
    return 0;
}

int test_rune(int argc, char *argv[])
{
    time_t rawtime; 
    int f;
    int retval = 0;

    f = open(TEST_RUNE_LOG, O_CREAT|O_APPEND, 0644);
    if (f < 0){
        printf("Failed to open '%s'\n", TEST_RUNE_LOG);
        return errno;
    }    

    time(&rawtime);
    printf("@Start at %s >>>>>\n", asctime(localtime(&rawtime)));

    clock_t start_time = clock();
    retval = runcases(argc, argv, f);
    clock_t end_time = clock();

    time(&rawtime);
    printf("\n <<<<<\n@End at %s", asctime(localtime(&rawtime)));

    printf("Total time: %ld ticks\n", end_time - start_time);

    close(f);

    return retval;
}
