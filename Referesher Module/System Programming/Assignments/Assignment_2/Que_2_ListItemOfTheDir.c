#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/types.h>


int main(int argc, char* argv[])
{
    char* dirPath;
    if (argc < 2)
        dirPath="./";
    else
        dirPath=argv[1];
    
    DIR *dir;
    struct dirent *dirElement;

    dir = opendir(dirPath);
    if (dir == NULL){
        printf("Unable to Open Directory");
        exit(0);
    }

    while ((dirElement = readdir(dir)) != NULL)
        printf("%s\n", dirElement->d_name);

    closedir(dir);
    
    return 0;
}
