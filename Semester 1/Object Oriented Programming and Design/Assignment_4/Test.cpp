#include <iostream>
#include <string>
#include <vector>
#include "BibTeXParser.hpp"
#include "PublicationDatabase.hpp"

void displayAuthorStats(const std::vector<std::string>& authors, const PublicationDatabase& db) {
    for (const auto& authorName : authors) {
        auto publications = db.searchByAuthor(authorName);

        if (publications.empty()) {
            std::cout << "No publications found for author: " << authorName << "\n";
            continue;
        }

        std::cout << "Publications for author: " << authorName << "\n";
        int totalCoAuthors = 0;
        for (const auto& pub : publications) {
            pub.display();
            totalCoAuthors += pub.getAuthors().size() - 1; // Exclude the author themselves
        }

        double avgCoAuthors = static_cast<double>(totalCoAuthors) / publications.size();
        std::cout << "Average number of co-authors for " << authorName << ": " << avgCoAuthors << "\n\n";
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./program <BibTeX file> <Author Name 1> [<Author Name 2> ...]\n";
        return 1;
    }

    std::string bibFile = argv[1];
    std::vector<std::string> authorNames;
    for (int i = 2; i < argc; ++i) {
        authorNames.emplace_back(argv[i]);
    }

    PublicationDatabase db;
    try {
        BibTeXParser::parseBibFile(bibFile, db, "IIIT-Delhi");
    } catch (const std::exception& ex) {
        std::cerr << "Error: " << ex.what() << "\n";
        return 1;
    }

    displayAuthorStats(authorNames, db);

    return 0;
}
