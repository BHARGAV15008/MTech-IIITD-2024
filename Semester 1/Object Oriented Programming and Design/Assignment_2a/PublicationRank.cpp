#include <iostream>
using namespace std;

class PublicationRank : public LibraryItem
{
private:
    int ID;
    string publication;
    int rank;
    double totalPaid;
    bool borrowed;

public:
    // Constructor
    PublicationRank(int ID, const string &publication, int rank, double totalPaid)
        : ID(ID), publication(publication), rank(rank), totalPaid(totalPaid) {}

    int getID() const
    {
        return ID;
    }
    string getPublication() const
    {
        return publication;
    }
    int getrank() const
    {
        return rank;
    }
    double gettotalPaid() const
    {
        return totalPaid;
    }
    bool isBorrowed() const
    {
        return borrowed;
    }
    void setBorrowed(bool status)
    {
        borrowed = status;
    }
    void printDetails() const override
    {
        cout << "ID: " << ID << "\nPublication Name: " << publication << "\nRank: " << rank << "\nTotal Paid: " << totalPaid << "\n";
    }
};
