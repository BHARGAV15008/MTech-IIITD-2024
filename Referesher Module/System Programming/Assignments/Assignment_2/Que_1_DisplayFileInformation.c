#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/stat.h>

void printFileInformation(char * fileName) {
    struct stat stats;
    
    if (stat(fileName, &stats) == -1) {
        printf("File Does Not Exists...\n");
        exit(EXIT_FAILURE);
    }
    
    // File Name: The name of the file;
    printf("\nFile Name             : %s", fileName);
    
    // Size: The size of the file in bytes;
    printf("\nSize                  : %d Bytes", (int)stats.st_size);
    
    // Blocks: The number of blocks allocated to the file;
    printf("\nBlocks                : %d", (int)stats.st_blocks);
    
    // IO Block: The size of the file system's block;
    printf("\nIO Blocks             : %d Bytes", (int)stats.st_size);
    
    // File Type: The type of the file (e.g., regular file, directory, character device, block device, FIFO, symbolic link, or socket);
    if(S_ISREG(stats.st_mode))
        printf("\nFile Type               : Regular File");
    else if (S_ISDIR(stats.st_mode))
        printf("\nFile Type               : Directory");
    else if (S_ISCHR(stats.st_mode))
        printf("\nFile Type               : Character Device");
    else if (S_ISBLK(stats.st_mode))
        printf("\nFile Type               : Block Device");
    else if (S_ISFIFO(stats.st_mode))
        printf("\nFile Type               : FIFO");
    else if (S_ISLNK(stats.st_mode))
        printf("\nFile Type               : Symbolic link");
    else if (S_ISSOCK(stats.st_mode))
        printf("\nFile Type               : Socket");
    else
        printf("\nFile Type               : Unknown");
    
    // Device ID: The ID of the device on which the file resides;
    printf("\nDevice ID             : %d", (int)stats.st_dev);
    
    // Inode Number: The unique identifier of the file within the file system;
    printf("\nInode Number          : %d", (int)stats.st_ino);
    
    // Number of Links: The number of hard links to the file;
    printf("\nNumber of Links       : %d", (int)stats.st_nlink);
    
    // Access Permissions: The permission settings of the file;
    printf("\nAccess Permissions    : %d", (int)stats.st_dev);
    
    // Owner and Group: The user ID (UID) and group ID (GID) of the file's owner and group;
    printf("\nOwner and Group       : (UID) %d,   (GID) %d", (int)stats.st_uid, (int)stats.st_gid);
    
    // Modification Times: The access, modification, and change times of the file;
    printf("\nAccess Time           : %s", asctime(gmtime(&stats.st_atime)));
    printf("\nModification Time     : %s", asctime(gmtime(&stats.st_mtime)));
    printf("\nChange Timee          : %s", asctime(gmtime(&stats.st_ctime)));
}

int main(int argc, char* argv[])
{
    char* fileName="DisplayFileInformation.c";
    if (argc < 2)
        printf("Please give the filename as Arguments...");
    else
        fileName=argv[1];
    
    printFileInformation(fileName);
    
    return 0;
}
