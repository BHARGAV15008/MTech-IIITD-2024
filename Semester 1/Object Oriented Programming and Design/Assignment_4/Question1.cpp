#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <optional>
#include <stdexcept>
#include <mutex>
#include <algorithm>
#include <nlohmann/json.hpp> // JSON library for serialization/deserialization

// Alias for JSON
using json = nlohmann::json;

// Author Class
class Author {
private:
    std::string name;
    std::string affiliation;

public:
    Author(const std::string& name, const std::string& affiliation)
        : name(name), affiliation(affiliation) {
    }

    const std::string& getName() const { return name; }
    const std::string& getAffiliation() const { return affiliation; }

    json toJson() const {
        return { {"name", name}, {"affiliation", affiliation} };
    }

    static Author fromJson(const json& j) {
        return Author(j.at("name"), j.at("affiliation"));
    }

    void display() const {
        std::cout << "Author: " << name << ", Affiliation: " << affiliation << "\n";
    }
};

// Publication Class
class Publication {
private:
    std::string title;
    std::string venue;
    int year;
    std::optional<std::string> doi; // Optional DOI field
    std::vector<Author> authors;

public:
    Publication(const std::string& title, const std::string& venue, int year, const std::optional<std::string>& doi = std::nullopt)
        : title(title), venue(venue), year(year), doi(doi) {
    }

    void addAuthor(const Author& author) {
        authors.push_back(author);
    }

    bool hasInstituteAffiliation(const std::string& institute) const {
        return std::any_of(authors.begin(), authors.end(), [&institute](const Author& author) {
            return author.getAffiliation() == institute;
            });
    }

    const std::string& getTitle() const { return title; }
    const std::string& getVenue() const { return venue; }
    int getYear() const { return year; }
    const std::optional<std::string>& getDOI() const { return doi; }
    const std::vector<Author>& getAuthors() const { return authors; }

    json toJson() const {
        json jAuthors = json::array();
        for (const auto& author : authors) {
            jAuthors.push_back(author.toJson());
        }

        return {
            {"title", title},
            {"venue", venue},
            {"year", year},
            {"doi", doi.value_or("")},
            {"authors", jAuthors}
        };
    }

    static Publication fromJson(const json& j) {
        Publication pub(
            j.at("title"),
            j.at("venue"),
            j.at("year"),
            j.at("doi").get<std::string>().empty() ? std::nullopt : std::make_optional(j.at("doi").get<std::string>())
        );

        for (const auto& authorJson : j.at("authors")) {
            pub.addAuthor(Author::fromJson(authorJson));
        }

        return pub;
    }

    void display() const {
        std::cout << "Title: " << title << "\n"
            << "Venue: " << venue << "\n"
            << "Year: " << year << "\n";
        if (doi.has_value()) {
            std::cout << "DOI: " << doi.value() << "\n";
        }
        std::cout << "Authors:\n";
        for (const auto& author : authors) {
            author.display();
        }
        std::cout << "-----------------------------\n";
    }
};

// Publication Database Class
class PublicationDatabase {
private:
    std::map<std::string, Publication> database; // Map with citeKey as string and Publication as value
    std::mutex dbMutex; // Mutex for thread-safety

public:
    void addPublication(const std::string& citeKey, const Publication& publication, const std::string& institute) {
        if (citeKey.empty()) {
            throw std::invalid_argument("CiteKey cannot be empty");
        }
        if (!publication.hasInstituteAffiliation(institute)) {
            throw std::invalid_argument("At least one author must belong to the institute");
        }

        std::lock_guard<std::mutex> lock(dbMutex); // Ensure thread-safety
        database[citeKey] = publication;
    }

    std::vector<Publication> searchByAuthor(const std::string& authorName) const {
        std::vector<Publication> results;
        std::lock_guard<std::mutex> lock(dbMutex);

        for (const auto& [citeKey, publication] : database) {
            for (const auto& author : publication.getAuthors()) {
                if (author.getName() == authorName) {
                    results.push_back(publication);
                    break;
                }
            }
        }
        return results;
    }

    void displayAllPublications() const {
        std::lock_guard<std::mutex> lock(dbMutex);
        for (const auto& [citeKey, publication] : database) {
            std::cout << "CiteKey: " << citeKey << "\n";
            publication.display();
        }
    }

    json toJson() const {
        std::lock_guard<std::mutex> lock(dbMutex);
        json j;
        for (const auto& [citeKey, publication] : database) {
            j[citeKey] = publication.toJson();
        }
        return j;
    }

    void fromJson(const json& j) {
        std::lock_guard<std::mutex> lock(dbMutex);
        database.clear();
        for (auto it = j.begin(); it != j.end(); ++it) {
            database[it.key()] = Publication::fromJson(it.value());
        }
    }
};