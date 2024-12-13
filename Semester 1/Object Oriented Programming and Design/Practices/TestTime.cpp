#include <iostream>
#include <chrono>

int main() {
    float z[100], x[100], y[100];
    int zx[200], xx[200], yx[200];
    for (int i = 0; i < 200; i++){
        xx[i] = i;
        yx[i] = i;
    }
    
    for (int i = 0; i < 100; i++){
        x[i] = i;
        y[i] = i;
    }

    auto start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 100; ++i) {
        z[i] = x[i] + y[i];
    }
    auto end = std::chrono::high_resolution_clock::now();

    std::chrono::duration<double, std::milli> elapsed_milliseconds = end - start;
    std::cout << "Elapsed time (float) : " << elapsed_milliseconds.count() << " milliseconds" << std::endl;

    start = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < 200; ++i) {
        zx[i] = xx[i] + yx[i];
    }
    end = std::chrono::high_resolution_clock::now();

    elapsed_milliseconds = end - start;
    std::cout << "Elapsed time (int) : " << elapsed_milliseconds.count() << " milliseconds" << std::endl;


    return 0;
}