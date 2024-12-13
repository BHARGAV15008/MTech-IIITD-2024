#ifndef BIBTEX_PARSER_H
#define BIBTEX_PARSER_H

#include <string>
#include <regex> // Include the regex header
#include "PublicationDatabase.hpp"

class BibTeXParser {
public:
    static void parseBibFile(const std::string& fileName, PublicationDatabase& db, const std::string& institute);

private:
    static void processEntry(const std::string& entry, PublicationDatabase& db, const std::string& institute,
                             const std::regex& entryRegex, const std::regex& fieldRegex);
    static void parseAuthors(const std::string& value, std::vector<Author>& authors);
};

#endif // BIBTEX_PARSER_H
