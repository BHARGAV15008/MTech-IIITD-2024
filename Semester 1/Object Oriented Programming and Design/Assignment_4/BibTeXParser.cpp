#include "BibTeXParser.hpp"
#include <fstream>
#include <regex>
#include <iostream>
#include <sstream>
#include <algorithm> // For transform

#define ANSI_RED "\033[31m" // Red color for terminal
#define ANSI_RESET "\033[0m" // Reset color

void BibTeXParser::parseBibFile(const std::string& fileName, PublicationDatabase& db, const std::string& institute) {
    std::ifstream file(fileName);
    if (!file.is_open()) {
        throw std::runtime_error("Unable to open BibTeX file");
    }

    std::string line;
    std::string currentEntry;
    std::regex entryRegex(R"(@(\w+)\{(.+),)");
    std::regex fieldRegex(R"((\w+)\s*=\s*[\{\"](.+)[\}\"])");

    while (std::getline(file, line)) {
        if (line.find("@") != std::string::npos) {
            if (!currentEntry.empty()) {
                processEntry(currentEntry, db, institute, entryRegex, fieldRegex);
                currentEntry.clear();
            }
        }
        currentEntry += line + "\n";
    }
    if (!currentEntry.empty()) {
        processEntry(currentEntry, db, institute, entryRegex, fieldRegex);
    }
}

void BibTeXParser::processEntry(const std::string& entry, PublicationDatabase& db, const std::string& institute,
                                const std::regex& entryRegex, const std::regex& fieldRegex) {
    std::smatch match;
    if (!std::regex_search(entry, match, entryRegex)) {
        std::cerr << ANSI_RED << "Assertion failed: Invalid BibTeX entry format" << ANSI_RESET << std::endl;
        return;
    }

    std::string citeKey = match[2];
    std::string title, venue;
    int year = 0;
    std::optional<std::string> doi = std::nullopt;
    std::vector<Author> authors;

    auto it = std::sregex_iterator(entry.begin(), entry.end(), fieldRegex);
    for (; it != std::sregex_iterator(); ++it) {
        std::string field = (*it)[1];
        std::string value = (*it)[2];

        if (field == "author") {
            parseAuthors(value, authors);
        } else if (field == "title") {
            title = value;
        } else if (field == "venue" || field == "journal") {
            venue = value;
        } else if (field == "year") {
            year = std::stoi(value);
        } else if (field == "doi") {
            doi = value;
        }
    }

    Publication pub(title, venue, year, doi);
    for (const auto& author : authors) {
        pub.addAuthor(author);
    }

    // Debugging output: print parsed authors
    std::cout << "Parsed authors for entry " << citeKey << ":\n";
    for (const auto& author : authors) {
        author.display();
    }

    // Relaxed affiliation validation
    if (!pub.hasInstituteAffiliation(institute)) {
        std::cerr << ANSI_RED << "Warning: No authors belong to the institute for entry: " << citeKey << ANSI_RESET << std::endl;
    }

    db.addPublication(citeKey, pub, institute);
}

void BibTeXParser::parseAuthors(const std::string& value, std::vector<Author>& authors) {
    std::istringstream stream(value);
    std::string author;
    while (std::getline(stream, author, ',')) {
        size_t pos = author.find("[");
        std::string name = author.substr(0, pos);
        std::string affiliation = (pos != std::string::npos) ? author.substr(pos + 1, author.length() - pos - 2) : "";
        // Trim spaces
        name.erase(name.find_last_not_of(" \n\r\t") + 1);
        name.erase(0, name.find_first_not_of(" \n\r\t"));
        authors.emplace_back(name, affiliation);
    }
}
