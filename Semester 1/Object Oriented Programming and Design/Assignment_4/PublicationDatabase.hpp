#ifndef PUBLICATION_DATABASE_H
#define PUBLICATION_DATABASE_H

#include <map>
#include <vector>
#include <string>
#include <mutex>
#include "Publication.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class PublicationDatabase {
private:
    std::map<std::string, Publication> database;
    mutable std::mutex dbMutex; // Ensure mutex is mutable

public:
    void addPublication(const std::string& citeKey, const Publication& publication, const std::string& institute);
    std::vector<Publication> searchByAuthor(const std::string& authorName) const;
    void displayAllPublications() const;

    json toJson() const;
    void fromJson(const json& j);
};

#endif // PUBLICATION_DATABASE_H
