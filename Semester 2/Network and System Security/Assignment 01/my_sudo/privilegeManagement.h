#ifndef PRIVILEGE_MANAGEMENT_H
#define PRIVILEGE_MANAGEMENT_H

void executeCommand(char *command[], uid_t targetUid);
void dropPrivileges();

#endif
