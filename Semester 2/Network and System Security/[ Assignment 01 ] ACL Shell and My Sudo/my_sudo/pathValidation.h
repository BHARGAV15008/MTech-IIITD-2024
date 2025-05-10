#ifndef PATH_VALIDATION_H
#define PATH_VALIDATION_H

char* resolveSecurePath(const char *inputPath);
uid_t getFileOwnerUid(const char *path);

#endif
