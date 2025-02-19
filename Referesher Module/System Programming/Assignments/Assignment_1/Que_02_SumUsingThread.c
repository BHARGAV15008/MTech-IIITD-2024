#include <stdio.h>
#include <pthread.h>

typedef struct {
    int init;
    int final;
    int* arr;
    int sum;
} ArraySum;

void sumByParts(ArraySum *arg){
    arg->sum = 0;
    for (int i = arg->init; i <= arg->final; i++) {
        arg->sum += arg->arr[i];
    }
}

void* call(void* arg) {
    sumByParts((ArraySum*) arg);
    pthread_exit(NULL);
}

int main() {
    int sum = 0;
    int arr[16] = {23, 45, 56, 67, 89, 23, 12, 1, 34, 10, 11, 4, 6, 9, 55};
    pthread_t threads[4];   // Define four thread in array;
    ArraySum setPart[4];    // Assign each part to each threads;

    // Create threads
    for (int i = 0; i < 4; i++) {                 // Below we defined starting index or ending index of thread which perform tasks;
        setPart[i].init = i * (16/4);             // at 0: 0 start, at 1: 4 start, at 2: 8 start, at 3: 12 start;
        setPart[i].final = (i + 1) * (16/4) - 1;  // at 0: 3 end,   at 1: 7 end,   at 2: 11 end,  at 3: 15 end;
        setPart[i].arr = arr;
        pthread_create(&threads[i], NULL, call, (void*) &setPart[i]);
    }

    // Join threads and Sum of all partial results;
    for (int i = 0; i < 4; i++) {
        printf("Thread %d Result: %d\n", i, setPart[i].sum);
        pthread_join(threads[i], NULL);
        sum += setPart[i].sum;
    }

    printf("Total sum: %d\n", sum);

    return 0;
}
