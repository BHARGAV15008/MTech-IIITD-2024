#include <iostream>
#include "User.cpp"
class Library
{
private:
    LibraryItem *libraryItems[MAX_ITEMS];
    int itemCount;
    int nextBookId;
    int totalCopies;

    User students[100]; // Assuming a maximum of 100 students
    int studentCount = 0;

    User teachers[50]; // Assuming a maximum of 50 teachers
    int teacherCount = 0;

public:
    Library() : itemCount(0), studentCount(0), teacherCount(0)
    {
        nextBookId = 100;
        totalCopies = 1;
    }
    // Library() : libraryItems{}, itemCount(0), students{}, studentCount(0), teachers{}, teacherCount(0), nextBookId(100) {}

    int getStudentCount() const
    {
        return studentCount;
    }
    int getTeacherCount() const
    {
        return teacherCount;
    }
    int getTotalUsers() const
    {
        return studentCount + teacherCount;
    }

    int getTotalItems() const
    {
        return itemCount;
    }

    void addItem(LibraryItem *item)
    {
        if (itemCount < MAX_ITEMS)
        {
            libraryItems[itemCount] = item;
            itemCount++;
        }
        else
        {
            cout << "Library is full. Cannot add more items." << endl;
        }
    }

    void printAllItems() const
    {
        for (int i = 0; i < itemCount; ++i)
        {
            if (libraryItems[i])
            {
                libraryItems[i]->printDetails();
                cout << "------------------------\n";
            }
        }
    }

    Book *getBookByID(int bookID) const
    {
        for (int i = 0; i < itemCount; i++)
        {
            Book *book = dynamic_cast<Book *>(libraryItems[i]);
            if (book && book->getBookID() == bookID)
            {
                return book; // Found the book with the specified ID
            }
        }
        return nullptr; // Book with the specified ID not found
    }
    Book *getBookByIsbn(int bookIsbn) const
    {
        for (int i = 0; i < itemCount; i++)
        {
            Book *book = dynamic_cast<Book *>(libraryItems[i]);
            if (book && book->getISBN() == bookIsbn)
            {
                return book; // Found the book with the specified Isbn
            }
        }
        return nullptr; // Book with the specified Isbn not found
    }
    void searchBooksByAuthor(const string &bookAuthor, Book *matchingBooks[], int &matchingCount);
    void searchBooksByTitle(const string &bookAuthor, Book *matchingBooks[], int &matchingCount);
    void searchPublication(const string &bookAuthor, PublicationRank *matchingBooks[], int &matchingCount);
    void searchJournal(const string &bookAuthor, Journals *matchingBooks[], int &matchingCount);

    void registerUser(const string &name, bool isTeacher)
    {
        if (isTeacher)
        {
            teachers[teacherCount++] = User(name, true);
            cout << "Registered as a Teacher." << endl;
        }
        else
        {
            students[studentCount++] = User(name, false);
            cout << "Registered as a Student." << endl;
        }
        cout << "-------------------------" << endl;
    }

    void showAllRegisteredUsers()
    {
        cout << "Registered Students:" << endl;
        for (int i = 0; i < studentCount; ++i)
        {
            cout << students[i].getName() << endl;
        }

        cout << "Registered Teachers:" << endl;
        for (int i = 0; i < teacherCount; ++i)
        {
            cout << teachers[i].getName() << endl;
        }
        cout << "-------------------------" << endl;
    }

    bool isEqualIgnoreCase(const string &str1, const string &str2)
    {
        // Compare two strings case-insensitively
        if (str1.size() != str2.size())
        {
            return false;
        }

        for (size_t i = 0; i < str1.size(); ++i)
        {
            if (tolower(str1[i]) != tolower(str2[i]))
            {
                return false;
            }
        }

        return true;
    }
    bool isEqualIgnore(const std::string &str1, const std::string &str2)
    {
        // Check if the lengths of the strings are equal
        if (str1.length() != str2.length())
        {
            return false;
        }

        // Compare characters case-insensitively
        for (size_t i = 0; i < str1.length(); ++i)
        {
            if (tolower(str1[i]) != tolower(str2[i]))
            {
                return false;
            }
        }

        return true;
    }
    // Function to add a new book to the library
    void addBook(int isbn, const string &author, const string &title, int originalPublicationYear)
    {
        if (itemCount >= MAX_ITEMS)
        {
            cout << "The library is full. Cannot add more books." << endl;
            return;
        }

        // Create a new Book object with the next available book ID
        Book *newBook = new Book();
        newBook->setID(ID++);
        newBook->setBookID(nextBookId++);
        newBook->setISBN(isbn);
        newBook->setAuthors(author);
        newBook->setTitle(title);
        newBook->setPublicationYear(originalPublicationYear);

        // Add the new book to the library
        // libraryItems[itemCount++] = newBook;
        addItem(newBook);

        cout << "Added book with ID " << newBook->getBookID() << " to the library." << endl;
    }

    bool borrowBook(const string &userName, int bookIdToBorrow);
    bool returnBook(Book *book);
    bool borrowPublication(const string &userName, int publication);
    bool returnPub(PublicationRank *publicationRank);
    bool borrowJournal(const string &userName, int title);

    virtual ~Library() {} // Virtual destructor
};
