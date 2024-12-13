#ifndef AUTHOR_H
#define AUTHOR_H

#include <string>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class Author {
private:
    std::string name;
    std::string affiliation;

public:
    Author(const std::string& name, const std::string& affiliation = "");
    const std::string& getName() const;
    const std::string& getAffiliation() const;

    json toJson() const;
    static Author fromJson(const json& j);
    void display() const;
};

#endif // AUTHOR_H
