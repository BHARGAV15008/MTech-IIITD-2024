#include <iostream>
using namespace std;
class Book : public LibraryItem
{
private:
    int ID;
    int book_id;
    int isbn;
    string title;
    string authors;
    int original_publication_year;
    bool borrowed;
    // double average_rating;
    // int  ratings_count;
public:
    // Constructor
    Book() : book_id(0), isbn(0), title(""), authors(""), original_publication_year(0) {}
    Book(int ID, int book_id, int isbn, const string &title, const string &authors, int original_publication_year)
        : ID(ID), book_id(book_id), isbn(isbn), title(title), authors(authors), original_publication_year(original_publication_year)
    {
    }

    // Getter functions
    int getID() const
    {
        return ID;
    }
    void setID(int id)
    {
        ID = id;
    }

    int getBookID() const
    {
        return book_id;
    }

    void setBookID(int bookid)
    {
        book_id = bookid;
    }

    int getISBN() const
    {
        return isbn;
    }
    void setISBN(int Isbn)
    {
        isbn = Isbn;
    }

    string getTitle() const
    {
        return title;
    }

    void setTitle(const string &newTitle)
    {
        title = newTitle;
    }

    string getAuthors() const
    {
        return authors;
    }
    void setAuthors(const string &newAuthor)
    {
        authors = newAuthor;
    }
    int getPublicationYear() const
    {
        return original_publication_year;
    }
    void setPublicationYear(int year)
    {
        original_publication_year = year;
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
        cout << "ID: " << ID << "\nBook_id: " << book_id << "\nISBN: " << isbn << "\nTitle: " << title << "\nAuthors: " << authors << "\nPublication Year: "
             << original_publication_year << "\n";
    }
};
