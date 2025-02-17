#include <iostream>
using namespace std;

/*
    Two way to define Tower of Honoi but time complexity almost equal but moves will be different;
    1. O(2^n): We moves one disk at a time;
        towerofhonoi (nDisk, source, tempPeg1, tempPeg2, destnation):
            check nDisk is 0:
                return

            check nDisk is 1:
                show source --> destination
                return
            othherwise
                towerofhonoi (nDisk-1, source, tempPeg2, destnation, tempPeg1)
                show source --> destination
                towerofhonoi (nDisk-1, tempPeg1, source, tempPeg2, destnation)
    
    2. O(2^(n/2)): We moves two disk at a time;
        towerofhonoi (nDisk, source, tempPeg1, tempPeg2, destnation):
            check nDisk is 0:
                return

            check nDisk is 1:
                show source --> destination
                return
            othherwise
                towerofhonoi (nDisk-2, source, destnation, tempPeg2, tempPeg1)
                show source --> tempPeg2
                show source --> destination
                show tempPeg2 --> destination
                towerofhonoi (nDisk-2, tempPeg1, source, tempPeg2, destnation)

*/

// Tower of Honoi with two temporary pegs;
void fourPegTowerOfHonoi(int nDisk, char* srcPeg, char* pegT1, char* pegT2, char* destPeg) {
    if (nDisk == 0) return;
    if (nDisk == 1){ 
        cout << srcPeg << " --> " << destPeg << "\n"; 
        return;
    }

    fourPegTowerOfHonoi(nDisk - 2, srcPeg, pegT2, destPeg, pegT1); // Rotate or Disk moves in Increasing order
    cout << srcPeg << " --> " << pegT2 << "\n";
    cout << srcPeg << " --> " << destPeg << "\n";
    cout << pegT2 << " --> " << destPeg << "\n";
    fourPegTowerOfHonoi(nDisk - 2, pegT1, srcPeg, pegT2, destPeg);  // Reverse Moves disk;
}

// Tower of Honoi with one temporary pegs;
/*
    O(2^(n)): We moves one disk at a time;
    towerofhonoi (nDisk, source, tempPeg, destnation):
        check nDisk is 0:
            return

        check nDisk is 1:
            show source --> destination
            return
        othherwise
            towerofhonoi (nDisk-1, source, destnation, tempPeg)
            show source --> destination
            towerofhonoi (nDisk-1, destnation, tempPeg, source)
*/
void threePegTowerOfHonoi(int n, char* srcPeg, char* pegT, char* destPeg) {
    if (n == 0) return;

    threePegTowerOfHonoi(n - 1, srcPeg, destPeg, pegT);
    cout << srcPeg << " --> " << destPeg << "\n";
    threePegTowerOfHonoi(n - 1, destPeg, pegT, srcPeg);
}

int main() {
    int noOfDisk;
    cout << "Enter the number of disks: ";
    cin >> noOfDisk;
    
    //  Assigned Name of the Rods/Pegs;
    char srcPeg[] = "T1";
    char pegT1[] = "T2";
    char pegT2[] = "T3";
    char destPeg[] = "T4";
    fourPegTowerOfHonoi(noOfDisk, srcPeg, pegT1, pegT2, destPeg);
    cout << endl << endl;
    threePegTowerOfHonoi(noOfDisk, srcPeg, pegT2, destPeg);
    return 0;
}
