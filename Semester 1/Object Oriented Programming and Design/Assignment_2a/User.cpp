#include <string>
#include "LibraryItem.cpp"
#include "Journals.cpp"
#include "PublicationRank.cpp"
#include "Book.cpp"

class User
{
private:
    string name;
    bool isTeacher;
    static const int MAX_BORROWED_BOOKS = 3; // Maximum number of books a user can borrow
    int borrowedCount;

public:
    Book *borrowedBooks[MAX_BORROWED_BOOKS];
    PublicationRank *borrowedbooks[MAX_BORROWED_BOOKS];
    Journals *borrowedJournals[MAX_BORROWED_BOOKS];
    time_t borrowedDates[MAX_BORROWED_BOOKS];
    User() : name(""), isTeacher(false), borrowedCount(0)
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            borrowedBooks[i] = nullptr;
        }
    }
    User(const string &name, bool isTeacher) : name(name), isTeacher(isTeacher)
    {
        borrowedCount = 0;
    }
    // User(const string& name, bool isTeacher = false) : name(name), isTeacher(isTeacher) {}

    string getName() const
    {
        return name;
    }

    bool isTeacherUser() const
    {
        return isTeacher;
    }
    int getBorrowedCount() const
    {
        return borrowedCount;
    }
    int getMaxBorrowedBooks() const
    {
        return MAX_BORROWED_BOOKS;
    }
    void incrementBorrowedCount()
    {
        borrowedCount++;
    }
    // Function to check if a book is currently borrowed by the user
    bool isBookBorrowed(Book *book) const
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            if (borrowedBooks[i] == book)
            {
                return true;
            }
        }
        return false;
    }
    bool canBorrowMoreBooks() const
    {
        return getBorrowedCount() < MAX_BORROWED_BOOKS;
    }

    // Function to get the last borrow time for a specific book
    time_t getLastBorrowTime(const Book *book) const
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            if (borrowedBooks[i] == book)
            {
                return borrowedDates[i];
            }
        }
        return 0; // Return 0 if the book is not found in the user's borrowed books
    }
    // Function to set the last borrow time for a specific book
    void setLastBorrowTime(const Book *book, time_t borrowTime)
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            if (borrowedBooks[i] == book)
            {
                borrowedDates[i] = borrowTime;
                return; // Book found and last borrow time updated
            }
        }
    }
    time_t getLastBorrowPubTime(const PublicationRank *publicationRank) const
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            if (borrowedbooks[i] == publicationRank)
            {
                return borrowedDates[i];
            }
        }
        return 0; // Return 0 if the book is not found in the user's borrowed books
    }
    void setLastBorrowPubTime(const PublicationRank *publicationRank, time_t borrowTime)
    {
        for (int i = 0; i < MAX_BORROWED_BOOKS; ++i)
        {
            if (borrowedbooks[i] == publicationRank)
            {
                borrowedDates[i] = borrowTime;
                return; // Book found and last borrow time updated
            }
        }
    }
};
