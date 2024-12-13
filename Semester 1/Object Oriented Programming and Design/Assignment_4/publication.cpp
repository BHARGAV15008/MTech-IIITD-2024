#include "Publication.hpp"
#include <iostream>
#include <algorithm>

Publication::Publication(const std::string& title, const std::string& venue, int year, const std::optional<std::string>& doi)
    : title(title), venue(venue), year(year), doi(doi) {}

void Publication::addAuthor(const Author& author) {
    authors.push_back(author);
}

bool Publication::hasInstituteAffiliation(const std::string& institute) const {
    return std::any_of(authors.begin(), authors.end(), [&institute](const Author& author) {
        return author.getAffiliation() == institute;
    });
}

const std::string& Publication::getTitle() const {
    return title;
}

const std::string& Publication::getVenue() const {
    return venue;
}

int Publication::getYear() const {
    return year;
}

const std::optional<std::string>& Publication::getDOI() const {
    return doi;
}

const std::vector<Author>& Publication::getAuthors() const {
    return authors;
}

json Publication::toJson() const {
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

Publication Publication::fromJson(const json& j) {
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

void Publication::display() const {
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
