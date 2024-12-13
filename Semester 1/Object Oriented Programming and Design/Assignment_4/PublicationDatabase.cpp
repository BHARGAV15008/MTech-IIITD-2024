#include "PublicationDatabase.hpp"
#include <iostream>
#include <mutex>
#include <algorithm> // For transform

void PublicationDatabase::addPublication(const std::string& citeKey, const Publication& publication, const std::string& institute) {
    if (citeKey.empty()) {
        throw std::invalid_argument("CiteKey cannot be empty");
    }

    std::lock_guard<std::mutex> lock(dbMutex);
    database[citeKey] = publication;
}

std::vector<Publication> PublicationDatabase::searchByAuthor(const std::string& authorName) const {
    std::vector<Publication> results;
    std::lock_guard<std::mutex> lock(dbMutex);

    // Convert authorName to lowercase for case-insensitive comparison
    std::string searchName = authorName;
    std::transform(searchName.begin(), searchName.end(), searchName.begin(), ::tolower);

    for (const auto& [citeKey, publication] : database) {
        for (const auto& author : publication.getAuthors()) {
            std::string authorNameLower = author.getName();
            std::transform(authorNameLower.begin(), authorNameLower.end(), authorNameLower.begin(), ::tolower);

            if (authorNameLower == searchName) {
                results.push_back(publication);
                break;
            }
        }
    }
    return results;
}

void PublicationDatabase::displayAllPublications() const {
    std::lock_guard<std::mutex> lock(dbMutex);
    for (const auto& [citeKey, publication] : database) {
        publication.display();
    }
}
