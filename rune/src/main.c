#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "rune.h"


int main(int argc, char *argv[])
{
#ifdef __DEBUG__
    for (int i = 1; i < argc; i++){
        if (strcmp(argv[i], "-t") == 0){
            return test_rune(argc, argv);
        }
    }
#endif /* __DEBUG__ */

    return rune_main(argc, argv);
}
