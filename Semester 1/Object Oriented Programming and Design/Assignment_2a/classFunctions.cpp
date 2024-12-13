#include <pthread.h>
#include <string>
#include "Library.cpp"
using namespace std;
void Library ::searchBooksByAuthor(const string &bookAuthor, Book *matchingBooks[], int &matchingCount)
{
    matchingCount = 0;

    // Convert the search term to lowercase for case-insensitive matching
    string searchAuthorLower = bookAuthor;
    for (char &c : searchAuthorLower)
    {
        c = tolower(c);
    }

    for (int i = 0; i < itemCount; i++)
    {
        Book *book = dynamic_cast<Book *>(libraryItems[i]);
        if (book)
        {
            string bookAuthorLower = book->getAuthors();
            for (char &c : bookAuthorLower)
            {
                c = tolower(c);
            }
            if (bookAuthorLower.find(searchAuthorLower) != string::npos)
            {
                matchingBooks[matchingCount++] = book; // Found a book with a matching author name
            }
        }
    }
}

void Library ::searchBooksByTitle(const string &bookAuthor, Book *matchingBooks[], int &matchingCount)
{
    matchingCount = 0;

    // Convert the search term to lowercase for case-insensitive matching
    string searchAuthorLower = bookAuthor;
    for (char &c : searchAuthorLower)
    {
        c = tolower(c);
    }

    for (int i = 0; i < itemCount; i++)
    {
        Book *book = dynamic_cast<Book *>(libraryItems[i]);
        if (book)
        {
            string bookAuthorLower = book->getTitle();
            for (char &c : bookAuthorLower)
            {
                c = tolower(c);
            }
            if (bookAuthorLower.find(searchAuthorLower) != string::npos)
            {
                matchingBooks[matchingCount++] = book; // Found a book with a matching author name
            }
        }
    }
}
void Library ::searchPublication(const string &bookAuthor, PublicationRank *matchingBooks[], int &matchingCount)
{
    matchingCount = 0;

    // Convert the search term to lowercase for case-insensitive matching
    string searchAuthorLower = bookAuthor;
    for (char &c : searchAuthorLower)
    {
        c = tolower(c);
    }

    for (int i = 0; i < itemCount; i++)
    {
        PublicationRank *publicationRank = dynamic_cast<PublicationRank *>(libraryItems[i]);
        if (publicationRank)
        {
            string bookAuthorLower = publicationRank->getPublication();
            for (char &c : bookAuthorLower)
            {
                c = tolower(c);
            }
            if (bookAuthorLower.find(searchAuthorLower) != string::npos)
            {
                matchingBooks[matchingCount++] = publicationRank; // Found a magazine with a matching publication name
            }
        }
    }
}
void Library ::searchJournal(const string &bookAuthor, Journals *matchingBooks[], int &matchingCount)
{
    matchingCount = 0;

    // Convert the search term to lowercase for case-insensitive matching
    string searchAuthorLower = bookAuthor;
    for (char &c : searchAuthorLower)
    {
        c = tolower(c);
    }

    for (int i = 0; i < itemCount; i++)
    {
        Journals *journal = dynamic_cast<Journals *>(libraryItems[i]);
        if (journal)
        {
            string bookAuthorLower = journal->getTitle();
            for (char &c : bookAuthorLower)
            {
                c = tolower(c);
            }
            if (bookAuthorLower.find(searchAuthorLower) != string::npos)
            {
                matchingBooks[matchingCount++] = journal; // Found a journal with a matching name
            }
        }
    }
}

bool Library::borrowBook(const string &userName, int bookIdToBorrow)
{
    User *user = nullptr;
    // Find the user by name (case-insensitive)
    for (int i = 0; i < studentCount; ++i)
    {
        if (isEqualIgnoreCase(students[i].getName(), userName))
        {
            user = &students[i];
            cout << "Registered as a Student." << endl;
            cout << "-----------------------------" << endl;
            break;
        }
    }

    if (!user)
    {
        for (int i = 0; i < teacherCount; ++i)
        {
            if (isEqualIgnoreCase(teachers[i].getName(), userName))
            {
                user = &teachers[i];
                cout << "Registered as a Teacher." << endl;
                cout << "-----------------------------" << endl;
                break;
            }
        }
    }

    if (!user)
    {
        cout << "User not found." << endl;
        return false;
    }

    Book *bookToBorrow = nullptr;

    // Find the book by book ID
    for (int i = 0; i < itemCount; ++i)
    {
        Book *book = dynamic_cast<Book *>(libraryItems[i]);
        if (book && book->getBookID() == bookIdToBorrow)
        {
            bookToBorrow = book;
            break;
        }
    }

    if (!bookToBorrow)
    {
        cout << "Book not found." << endl;
        return false;
    }

    if (user->getBorrowedCount() >= user->getMaxBorrowedBooks())
    {
        cout << userName << " has reached the maximum number of borrowed books." << endl;
        return false;
    }

    time_t now = time(nullptr);
    struct tm *timeinfo = localtime(&now);

    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);

    cout << "Current local time: " << buffer << endl;

    int returnPeriod = (user->isTeacherUser()) ? 180 : 30; //(assume 1 day=1 sec)

    // Check if the book is available for borrowing (not borrowed within the return period)
    if (now - user->getLastBorrowTime(bookToBorrow) >= returnPeriod || !bookToBorrow->isBorrowed())
    {
        // Check if there are available copies of the book to borrow
        if (totalCopies > 0)
        {
            user->borrowedBooks[user->getBorrowedCount()] = bookToBorrow;
            user->borrowedDates[user->getBorrowedCount()] = now;
            user->setLastBorrowTime(bookToBorrow, now);
            user->incrementBorrowedCount();

            bookToBorrow->setBorrowed(true);

            totalCopies--;

            cout << userName << " has borrowed the book: " << bookToBorrow->getTitle() << endl;
            // Schedule the book to be returned after the return period
            thread returnThread([this, bookToBorrow, returnPeriod]()
                                {
                                    this_thread::sleep_for(chrono::seconds(returnPeriod));
                                    returnBook(bookToBorrow); // Call the returnBook function after the return period
                                });
            returnThread.detach(); // Detach the thread to run in the background
            return true;
        }
        else
        {
            cout << "No available copies of the book." << endl;
            return false;
        }
    }
    else
    {
        cout << "The book is not available for borrowing yet." << endl;
        return false;
    }
}
bool Library::returnBook(Book *book)
{
    if (book->isBorrowed())
    {
        book->setBorrowed(false);
        totalCopies++;
        cout << "\nBook returned: " << book->getTitle() << endl;
        time_t now = time(nullptr);
        struct tm *timeinfo = localtime(&now);

        char buffer[80];
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);
        cout << "Current local time: " << buffer << endl;
        return true;
    }
    else
    {
        cout << "\nBook not borrowed or not found." << endl;
        return false;
    }
}

bool Library::borrowPublication(const string &userName, int publication)
{
    User *user = nullptr;
    for (int i = 0; i < studentCount; ++i)
    {
        if (isEqualIgnoreCase(students[i].getName(), userName))
        {
            user = &students[i];
            cout << "Registered as a Student." << endl;
            cout << "-----------------------------" << endl;
            break;
        }
    }

    if (!user)
    {
        for (int i = 0; i < teacherCount; ++i)
        {
            if (isEqualIgnoreCase(teachers[i].getName(), userName))
            {
                user = &teachers[i];
                cout << "Registered as a Teacher." << endl;
                cout << "-----------------------------" << endl;
                break;
            }
        }
    }

    if (!user)
    {
        cout << "User not found." << endl;
        return false;
    }

    PublicationRank *pubToBorrow = nullptr;

    for (int i = 0; i < itemCount; ++i)
    {
        PublicationRank *publicationRank = dynamic_cast<PublicationRank *>(libraryItems[i]);
        if (publicationRank && publicationRank->getID()==publication)
        {
            pubToBorrow = publicationRank;
            break;
        }
    }

    if (!pubToBorrow)
    {
        cout << "Publication not found." << endl;
        return false;
    }

    if (user->getBorrowedCount() >= user->getMaxBorrowedBooks())
    {
        cout << userName << " has reached the maximum number of borrowed books." << endl;
        return false;
    }
    time_t now = time(nullptr);
    struct tm *timeinfo = localtime(&now);

    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);

    cout << "Current local time: " << buffer << endl;

    int returnPeriod = (user->isTeacherUser()) ? 180 : 30;

    if (now - user->getLastBorrowPubTime(pubToBorrow) >= returnPeriod || !pubToBorrow->isBorrowed())
    {
        if (totalCopies > 0)
        {
            user->borrowedbooks[user->getBorrowedCount()] = pubToBorrow;
            user->borrowedDates[user->getBorrowedCount()] = now;
            user->setLastBorrowPubTime(pubToBorrow, now);
            user->incrementBorrowedCount();

            pubToBorrow->setBorrowed(true);

            totalCopies--;

            cout << userName << " has borrowed the magazine: " << pubToBorrow->getPublication() << endl;
            thread returnThread([this, pubToBorrow, returnPeriod]()
                                {
                                    this_thread::sleep_for(chrono::seconds(returnPeriod));
                                    returnPub(pubToBorrow); 
                                });
            returnThread.detach();
            return true;
        }
        else
        {
            cout << "No available copies of the book." << endl;
            return false;
        }
    }
    else
    {
        cout << "The magazine is not available for borrowing yet." << endl;
        return false;
    }
}
bool Library::returnPub(PublicationRank *publicationRank)
{
    if (publicationRank->isBorrowed())
    {
        publicationRank->setBorrowed(false);
        totalCopies++;
        cout << "\nBook returned: " << publicationRank->getPublication() << endl;
        time_t now = time(nullptr);
        struct tm *timeinfo = localtime(&now);

        char buffer[80];
        strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);
        cout << "Current local time: " << buffer << endl;
        return true;
    }
    else
    {
        cout << "\nBook not borrowed or not found." << endl;
        return false;
    }
}

bool Library::borrowJournal(const string &userName, int title)
{
    User *user = nullptr;
    for (int i = 0; i < studentCount; ++i)
    {
        if (isEqualIgnoreCase(students[i].getName(), userName))
        {
            user = &students[i];
            cout << "Registered as a Student." << endl;
            cout << "-----------------------------" << endl;
            break;
        }
    }

    if (!user)
    {
        for (int i = 0; i < teacherCount; ++i)
        {
            if (isEqualIgnoreCase(teachers[i].getName(), userName))
            {
                user = &teachers[i];
                cout << "Registered as a Teacher." << endl;
                cout << "-----------------------------" << endl;
                break;
            }
        }
    }

    if (!user)
    {
        cout << "User not found." << endl;
        return false;
    }

    Journals *journalToBorrow = nullptr;
    for (int i = 0; i < itemCount; ++i)
    {
        Journals *journals = dynamic_cast<Journals *>(libraryItems[i]);
        if (journals && journals->getID()== title)
        {
            journalToBorrow = journals;
            break;
        }
    }

    if (!journalToBorrow)
    {
        cout << "Journals not found." << endl;
        return false;
    }


    time_t now = time(nullptr);
    struct tm *timeinfo = localtime(&now);

    char buffer[80];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeinfo);

    cout << "Current local time: " << buffer << endl;

    // if (user->getBorrowedCount() < user->getMaxBorrowedBooks())
    // {
        user->borrowedJournals[user->getBorrowedCount()] = journalToBorrow;
        user->borrowedDates[user->getBorrowedCount()] = time(nullptr);
        //user->incrementBorrowedCount();
        cout << userName << " has borrowed the book: " << journalToBorrow->getTitle() << endl;
        return true;
    // }
    // else
    // {
    //     cout << userName << " has reached the maximum number of borrowed Journal." << endl;
    //     return false;
    // }
}
