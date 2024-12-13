#ifndef PUBLICATION_H
#define PUBLICATION_H

#include <string>
#include <vector>
#include <optional>
#include "Author.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Publication {
private:
    std::string title;
    std::string venue;
    int year;
    std::optional<std::string> doi;
    std::vector<Author> authors;

public:
    Publication() : title(""), venue(""), year(0), doi(std::nullopt) {} // Default constructor
    Publication(const std::string& title, const std::string& venue, int year, const std::optional<std::string>& doi = std::nullopt);

    void addAuthor(const Author& author);
    bool hasInstituteAffiliation(const std::string& institute) const;

    const std::string& getTitle() const;
    const std::string& getVenue() const;
    int getYear() const;
    const std::optional<std::string>& getDOI() const;
    const std::vector<Author>& getAuthors() const;

    json toJson() const;
    static Publication fromJson(const json& j);

    void display() const;
};

#endif // PUBLICATION_H
