#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

void handleChildAndExitIt(int ChkId){
    if (ChkId == 0){
        printf("\nChild Process Exit...");
        exit(0);
    } else {
        printf("Parent Process Still running...");
    }
}

void getProcessIds(int chkId){    
    // Let's Print Process Ids and their Parent Process Ids;
    printf("Current Process Id - %d\n", getpid());
    printf("Parent of current Process Id - %d\n", getppid());
    
    // Here we have to check running process is child or not;
    if (chkId == 0){
        printf("Now in child Process\n");

        // ---------------  CASE I  -------------------------------------

        // If child process in running state then kill the parent process by their ids;
        // After 5 seconds;
        sleep(5);
        kill(getppid(), 9);
    } else {
        // Wait until child Process wasnt killed parent Process;
        wait(0);

        // ---------------  CASE II  -------------------------------------

        // // Also this alternate option 
        // // Here wait option to parent process like:
        // sleep(5);
        // exit(0);  // We use to exit process;
        // kill(getpid(), 9);  // We use to kill process itself;
    }
}

int main(){
    int chkId = fork();
    getProcessIds(chkId);
    
    // Its run once because of parent process kill or exit;
    // Its run by child process;
    printf("Current Process Id - %d\n", getpid());
    printf("Parent of current Process Id - %d\n", getppid());

    handleChildAndExitIt(chkId);
    return 0;
}