#include <iostream>
#include <string>
#include "BibTeXParser.hpp"
#include "PublicationDatabase.hpp"

void displayAuthorPublications(const std::string& authorName, const PublicationDatabase& db) {
    auto publications = db.searchByAuthor(authorName);

    if (publications.empty()) {
        std::cout << "No publications found for author: " << authorName << std::endl;
        return;
    }

    int totalCoAuthors = 0;
    std::cout << "Publications for author: " << authorName << "\n";
    for (const auto& pub : publications) {
        pub.display();
        totalCoAuthors += pub.getAuthors().size() - 1; // Exclude the author themselves
    }

    double averageCoAuthors = static_cast<double>(totalCoAuthors) / publications.size();
    std::cout << "Average number of co-authors: " << averageCoAuthors << "\n";
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./program <BibTeX file> <Author Name>" << std::endl;
        return 1;
    }

    std::string bibFile = argv[1];
    std::string authorName = argv[2];

    PublicationDatabase db;
    try {
        BibTeXParser::parseBibFile(bibFile, db, "IIIT-Delhi");
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << std::endl;
        return 1;
    }

    displayAuthorPublications(authorName, db);
    return 0;
}
