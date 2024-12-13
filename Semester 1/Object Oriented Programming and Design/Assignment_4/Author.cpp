#include "Author.hpp"
#include <iostream>

Author::Author(const std::string& name, const std::string& affiliation)
    : name(name), affiliation(affiliation) {}

const std::string& Author::getName() const {
    return name;
}

const std::string& Author::getAffiliation() const {
    return affiliation;
}

json Author::toJson() const {
    return { {"name", name}, {"affiliation", affiliation} };
}

Author Author::fromJson(const json& j) {
    return Author(j.at("name"), j.at("affiliation"));
}

void Author::display() const {
    std::cout << "Author: " << name << ", Affiliation: " << affiliation << "\n";
}
