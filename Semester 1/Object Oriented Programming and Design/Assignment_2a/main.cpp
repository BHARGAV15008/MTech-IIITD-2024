#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstring>
#include <cctype>
#include <limits>
#include <chrono>
#include <thread>
#include <iomanip>
#include "functions.cpp"
#include "classFunctions.cpp"
using namespace std;

int main()
{
    Library library;
    // int ID = 1;

    // Opening journal.csv
    ifstream journalFile("journals.csv");
    if (journalFile.is_open())
    {
        string line;
        // Read and discard the header line
        // getline(journalFile, line);

        while (getline(journalFile, line))
        {
            // Define an array to store fields

            const int fieldCount = 2;
            string fields[fieldCount];

            // Parse CSV line into fields
            splitLine(line, fields, fieldCount);

            if (fieldCount >= 2)
            {
                string title = fields[0];

                Journals *journal = new Journals(ID, title);
                // journal-> printDetails();
                // cout << "------------------------\n";
                library.addItem(journal);
                ID++;
            }
        }

        journalFile.close();
    }
    else
    {
        cerr << "Failed to open journals.csv\n";
    }
    //  Opening book.csv
    ifstream bookFile("books.csv");
    if (bookFile.is_open())
    {
        string line;
        // Read and discard the header line
        getline(bookFile, line);
        while (getline(bookFile, line))
        {
            const int fieldCount = 24;
            string fields[fieldCount];
            if (fieldCount >= 24) {
            int book_id, isbn;
            string title, authors;
            double original_publication_year;
            
            istringstream ss(line);
            ss >> book_id; 
            for (int i = 0; i < 5; ++i)
            {
                ss.ignore(256, ','); // Ignore fields until the next comma
            }
            ss >> isbn; // Read isbn until the next comma
            ss.ignore(256, ',');
            ss.ignore(256, ',');
            if (line.find("\"") != string::npos)
            {
                ss >> quoted(authors);
            }
            else
            {

                getline(ss, authors, ',');
            }
            ss.ignore(256, ',');
            ss >> original_publication_year;
            ss.ignore(256, ',');
            ss.ignore(256, ',');
            //getline(ss, title, ',');
            if (fields[9].find("\"") != string::npos)
            {
                ss >> quoted(title);
            }
            else
            {

                getline(ss, title, ',');
                ss.ignore(256, ',');
            }

            Book *book = new Book(ID, book_id, isbn, title, authors, original_publication_year);
            // book->printDetails();
            // cout << "------------------------\n";
            library.addItem(book);
            ID++;
         }

        }
        bookFile.close();
    }
    else
    {
        cerr << "Failed to open books.csv\n";
    }

    // opening publicatin_rank.csv

    ifstream publicationFile("publications_rank.csv");
    if (publicationFile.is_open())
    {
        string line;
        // Read and discard the header line
        getline(publicationFile, line);

        while (getline(publicationFile, line))
        {
            // Define an array to store fields
            const int fieldCount = 11;
            string fields[fieldCount];

            // Parse CSV line into fields
            splitCSVLine(line, fields, fieldCount);

            if (fieldCount >= 11)
            {
                string publication = fields[0];
                int rank = stoi(fields[1]);
                double totalPaid = stod(fields[2]);

                PublicationRank *publicationRank = new PublicationRank(ID, publication, rank, totalPaid);

                // publicationRank-> printDetails();
                // cout << "------------------------\n";
                library.addItem(publicationRank);
                ID++;
            }
        }
        publicationFile.close();
    }
    else
    {
        cerr << "Failed to open publications_rank.csv\n";
    }
    
    // library.printAllItems();

    int choice;
    do
    {
        cout << "Menu:" << endl;
        cout << "1. Register as a Student" << endl;
        cout << "2. Register as a Teacher" << endl;
        cout << "3. Search any item" << endl;
        cout << "4. Borrow any item" << endl;
        cout << "5. Purchase a book" << endl;
        cout << "6. Show all item lists" << endl;
        cout << "7. Exit" << endl;
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice)
        {
        case 1:
        {
            // Register as a Student
            string userName;
            do
            {
                cout << "Enter your name: ";
                cin.ignore();
                getline(cin, userName);

                if (!isValidUserName(userName))
                {
                    cout << "Invalid input. Please enter a valid name." << endl;
                }
            } while (!isValidUserName(userName));

            library.registerUser(userName, false); // Register as a student
            library.showAllRegisteredUsers();
            break;
        }
        case 2:
        {
            // Register as a Teacher
            string userName;
            do
            {
                cout << "Enter your name: ";
                cin.ignore();
                getline(cin, userName);

                if (!isValidUserName(userName))
                {
                    cout << "Invalid input. Please enter a valid name." << endl;
                }
            } while (!isValidUserName(userName));

            library.registerUser(userName, true); // Register as a teacher
            library.showAllRegisteredUsers();
            break;
        }
        case 3:
        {
            int choice;
            char phy, book;
            cout << "For physical items, press 'Y' or 'y' otherwise for electronic items:" << endl;
            cin >> phy;
            if (phy == 'Y' || phy == 'y')
            {
                cout << "For book, type 'Y' or 'y', otherwise for magazines :" << endl;
                cin >> book;
                if (book == 'Y' || book == 'y')
                {
                    cout << "Book can be search by:  \n1. Book ID \n2. ISBN \n3. Author's Name \n4. Title \nEnter your choice:";
                    cin >> choice;
                    switch (choice)
                    {
                    case 1:
                    {
                        // Search for a Book by book_id
                        int bookIdToSearch;
                        bool validInput = false;
                        do
                        {
                            cout << "Enter the book_id to search: ";

                            // Try to read the input as an integer
                            if (cin >> bookIdToSearch)
                            {
                                validInput = true;
                            }
                            else
                            {
                                cout << "Invalid input. Please enter a valid integer." << endl;
                                // Clear the input buffer to handle invalid input
                                cin.clear();
                                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                            }
                        } while (!validInput);

                        Book *foundBook = library.getBookByID(bookIdToSearch);
                        if (foundBook != nullptr)
                        {
                            cout << "Book Found!!!!!!!!!!!!:\nID: "<<foundBook->getID()<<"\nTitle: " << foundBook->getTitle() << "\nISBN: " << foundBook->getISBN() << "\nAuthours: "
                                 << foundBook->getAuthors() << "\nPublication Year: " << foundBook->getPublicationYear() << endl;
                            cout << "-----------------------\n";
                        }
                        else
                        {
                            cout << "Book not found." << endl;
                        }
                        break;
                    }
                    case 2:
                    {
                        // Search for a Book by ISBN
                        int ISBNToSearch;
                        bool validInput = false;
                        do
                        {
                            cout << "Enter the ISBN to search: ";

                            // Try to read the input as an integer
                            if (cin >> ISBNToSearch)
                            {
                                validInput = true;
                            }
                            else
                            {
                                cout << "Invalid input. Please enter a valid integer." << endl;
                                // Clear the input buffer to handle invalid input
                                cin.clear();
                                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                            }
                        } while (!validInput);

                        Book *foundBook = library.getBookByIsbn(ISBNToSearch);
                        if (foundBook != nullptr)
                        {
                            cout << "Book Found!!!!!!!!!!!!:\nID: "<<foundBook->getID()<<"\nTitle: " << foundBook->getTitle() << "\nISBN: " << foundBook->getISBN() << "\nAuthours: "
                                 << foundBook->getAuthors() << "\nPublication Year: " << foundBook->getPublicationYear() << endl;
                            cout << "-----------------------\n";
                        }
                        else
                        {
                            cout << "Book not found." << endl;
                        }
                        break;
                    }
                    case 3:
                    {
                        // Search for a Book by Author's Name
                        string authorNameToSearch;
                        do
                        {
                            cout << "Enter the author name to search: ";
                            cin.ignore();
                            getline(cin, authorNameToSearch);

                            if (!isValidUserName(authorNameToSearch))
                            {
                                cout << "Invalid input. Please enter a valid name." << endl;
                            }
                        } while (!isValidUserName(authorNameToSearch));

                        const int maxMatchingBooks = 100; // Define a maximum limit for matching books
                        Book *matchingBooks[maxMatchingBooks];
                        int matchingCount = 0;

                        library.searchBooksByAuthor(authorNameToSearch, matchingBooks, matchingCount);

                        if (matchingCount > 0)
                        {
                            cout << "Books by " << authorNameToSearch << ":" << endl;
                            cout << "--------------------------------\n";
                            for (int i = 0; i < matchingCount; i++)
                            {   cout <<"Id: "<<matchingBooks[i]->getID()<<endl;
                                cout << "BookID: " << matchingBooks[i]->getBookID() << "\nTitle: " << matchingBooks[i]->getTitle() << "\nISBN: " << matchingBooks[i]->getISBN() << endl;
                                cout << "Author Name: " << matchingBooks[i]->getAuthors() << endl;
                                cout << "--------------------------------\n";
                            }
                        }
                        else
                        {
                            cout << "No books by " << authorNameToSearch << " found." << endl;
                        }
                        break;
                    }
                    case 4:
                    {
                        // Search for a Book by its Title
                        string Title;
                        do
                        {
                            cout << "Enter the Title to search: ";
                            cin.ignore();
                            getline(cin, Title);

                            if (!isValidUserName(Title))
                            {
                                cout << "Invalid input. Please enter a valid name." << endl;
                            }
                        } while (!isValidUserName(Title));

                        const int maxMatchingBooks = 100; // Define a maximum limit for matching books
                        Book *matchingBooks[maxMatchingBooks];
                        int matchingCount = 0;

                        library.searchBooksByTitle(Title, matchingBooks, matchingCount);

                        if (matchingCount > 0)
                        {
                            cout << "Books by " << Title << ":" << endl;
                            cout << "--------------------------------\n";
                            for (int i = 0; i < matchingCount; i++)
                            {   cout <<"Id: "<<matchingBooks[i]->getID()<<endl;
                                cout << "BookID: " << matchingBooks[i]->getBookID() << "\nTitle: " << matchingBooks[i]->getTitle() << "\nISBN: " << matchingBooks[i]->getISBN() << endl;
                                cout << "Author Name: " << matchingBooks[i]->getAuthors() << endl;
                                cout << "--------------------------------\n";
                            }
                        }
                        else
                        {
                            cout << "No books by " << Title << " found." << endl;
                        }
                        break;
                    }
                    }
                }
                else
                {
                    string magazine;
                    do
                    {
                        cout << "Enter the name of magzine you want to search:";
                        cin.ignore();
                        getline(cin, magazine);

                        if (!isValidUserName(magazine))
                        {
                            cout << "Invalid input. Please enter a valid name." << endl;
                        }
                    } while (!isValidUserName(magazine));

                    const int maxMatchingBooks = 100; // Define a maximum limit for matching books
                    PublicationRank *matchingBooks[maxMatchingBooks];
                    int matchingCount = 0;

                    library.searchPublication(magazine, matchingBooks, matchingCount);

                    if (matchingCount > 0)
                    {
                        cout << "Magazine by " << magazine << ":" << endl;
                        cout << "--------------------------------\n";
                        for (int i = 0; i < matchingCount; i++)
                        {   cout <<"Id: "<<matchingBooks[i]->getID() <<endl;
                            cout << "Publication: " << matchingBooks[i]->getPublication() << "\nRank: " << matchingBooks[i]->getrank() << "\nTotal Paid: " << matchingBooks[i]->gettotalPaid() << endl;
                            cout << "--------------------------------\n";
                        }
                    }
                    else
                    {
                        cout << "No Publication by " << magazine << " found." << endl;
                    }
                    break;
                }
            } // to check physical item
            else
            {
                cout << "Electronic items" << endl;
                string magazine;
                do
                {
                    cout << "Enter the name of journal you want to search: ";
                    cin.ignore();
                    getline(cin, magazine);

                    if (!isValidUserName(magazine))
                    {
                        cout << "Invalid input. Please enter a valid name." << endl;
                    }
                } while (!isValidUserName(magazine));

                const int maxMatchingBooks = 100; // Define a maximum limit for matching books
                Journals *matchingBooks[maxMatchingBooks];
                int matchingCount = 0;

                library.searchJournal(magazine, matchingBooks, matchingCount);

                if (matchingCount > 0)
                {
                    cout << "Journal by " << magazine << ":" << endl;
                    cout << "--------------------------------\n";
                    for (int i = 0; i < matchingCount; i++)
                    {
                        cout << "ID: " << matchingBooks[i]->getID() << "\nTitle: " << matchingBooks[i]->getTitle() << endl;
                        cout << "--------------------------------\n";
                    }
                }
                else
                {
                    cout << "No Journal by " << magazine << " found." << endl;
                }
                break;
            }
            break;
        } // case 3 to search items
        case 4:
        {
            char phy, book;
            cout << "For physical items, press 'Y' or 'y' otherwise for electronic items:" << endl;
            cin >> phy;
            if (phy == 'Y' || phy == 'y')
            {
                cout << "For book, type 'Y' or 'y', otherwise for magazines :" << endl;
                cin >> book;
                if (book == 'Y' || book == 'y')
                {

                    string userNameToBorrow;
                    int bookIdToBorrow;
                    do
                    {
                        cout << "Enter your name: ";
                        cin.ignore();
                        getline(cin, userNameToBorrow);

                        if (!isValidUserName(userNameToBorrow))
                        {
                            cout << "Invalid input. Please enter a valid name." << endl;
                        }
                    } while (!isValidUserName(userNameToBorrow));

                    bool validInput = false;
                    do
                    {
                        cout << "Enter the book_id to borrow: ";

                        // Try to read the input as an integer
                        if (cin >> bookIdToBorrow)
                        {
                            validInput = true;
                        }
                        else
                        {
                            cout << "Invalid input. Please enter a valid integer." << endl;
                            // Clear the input buffer to handle invalid input
                            cin.clear();
                            cin.ignore(numeric_limits<streamsize>::max(), '\n');
                        }
                    } while (!validInput);

                    if (library.borrowBook(userNameToBorrow, bookIdToBorrow))
                    {
                        // Book successfully borrowed
                    }
                    else
                    {
                        // Error message already printed in the borrowBook function
                    }
                    break;
                }

                else
                {

                    string userNameToBorrow;
                    int publication;
                    do
                    {
                        cout << "Enter your name: ";
                        cin.ignore();
                        getline(cin, userNameToBorrow);

                        if (!isValidUserName(userNameToBorrow))
                        {
                            cout << "Invalid input. Please enter a valid name." << endl;
                        }
                    } while (!isValidUserName(userNameToBorrow));

                    bool validInput = false;
                    do
                    {
                        cout << "Enter the id to borrow magazine: ";

                        // Try to read the input as an integer
                        if (cin >> publication)
                        {
                            validInput = true;
                        }
                        else
                        {
                            cout << "Invalid input. Please enter a valid integer." << endl;
                            // Clear the input buffer to handle invalid input
                            cin.clear();
                            cin.ignore(numeric_limits<streamsize>::max(), '\n');
                        }
                    } while (!validInput);

                    if (library.borrowPublication(userNameToBorrow, publication))
                    {
                        // Book successfully borrowed
                    }
                    else
                    {
                        // Error message already printed in the borrowBook function
                    }
                    break;
                }
            }
            else
            {
                string userNameToBorrow;
                int title;
                do
                {
                    cout << "Enter your name: ";
                    cin.ignore();
                    getline(cin, userNameToBorrow);

                    if (!isValidUserName(userNameToBorrow))
                    {
                        cout << "Invalid input. Please enter a valid name." << endl;
                    }
                } while (!isValidUserName(userNameToBorrow));

               bool validInput = false;
                    do
                    {
                        cout << "Enter the id to borrow journal: ";

                        // Try to read the input as an integer
                        if (cin >> title)
                        {
                            validInput = true;
                        }
                        else
                        {
                            cout << "Invalid input. Please enter a valid integer." << endl;
                            // Clear the input buffer to handle invalid input
                            cin.clear();
                            cin.ignore(numeric_limits<streamsize>::max(), '\n');
                        }
                    } while (!validInput);

                if (library.borrowJournal(userNameToBorrow, title))
                {
                    // Book successfully borrowed
                }
                else
                {
                    // Error message already printed in the borrowBook function
                }
                break;
            }
            break;
        } // case 4 ends
        case 5:
        {

            string author, title;
            int originalPublicationYear;

            int isbn;
            bool validInput = false;
            do
            {
                cout << "Enter the ISBN : ";

                // Try to read the input as an integer
                if (cin >> isbn)
                {
                    validInput = true;
                }
                else
                {
                    cout << "Invalid input. Please enter a valid integer." << endl;
                    // Clear the input buffer to handle invalid input
                    cin.clear();
                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                }
            } while (!validInput);

            do
            {
                cout << "Enter the author name : ";
                cin.ignore();
                getline(cin, author);

                if (!isValidUserName(author))
                {
                    cout << "Invalid input. Please enter a valid name." << endl;
                }
            } while (!isValidUserName(author));

            do
            {
                cout << "Enter the title of book: ";
                cin.ignore();
                getline(cin, title);

                if (!isValidUserName(title))
                {
                    cout << "Invalid input. Please enter a valid name." << endl;
                }
            } while (!isValidUserName(title));

            while (true)
            {
                cout << "Enter the year of publication: ";
                if (cin >> originalPublicationYear && originalPublicationYear >= 1900 && originalPublicationYear <= 2023)
                {
                    if (cin.peek() == '\n')
                    {
                        // Valid input
                        break;
                    }
                }

                cout << "Invalid input. Please enter an integer originalPublicationYear between 1990 to 2023." << endl;
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
            }
            library.addBook(isbn, author, title, originalPublicationYear);
            break;
        }
        case 6:
            library.printAllItems();
            // cout << "To print journal:" << endl;
            // Journals *journal = new Journals(ID, title);
            // journal->printDetails();
            break;
        case 7:
            cout << "Exiting program." << endl;
            break;
        default:
            cout << "Invalid choice. Please try again." << endl;
        }
    } while (choice != 7);
    return 0;
}
