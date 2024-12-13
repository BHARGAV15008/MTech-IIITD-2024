#include <iostream>
#include <ctype.h>
#include <string>
#include <sstream>
using namespace std;
bool isNumeric(const string &str)
{
    for (char c : str)
    {
        if (!isdigit(c))
        {
            return false;
        }
    }
    return true;
}

// Function to split a CSV line into fields based on commas
void splitCSVLine(const string &line, string fields[], int fieldCount)
{
    stringstream ss(line);
    for (int i = 0; i < fieldCount; i++)
    {
        getline(ss, fields[i], ',');
    }
}
void splitLine(const string &line, string fields[], int fieldCount)
{
    stringstream ss(line);
    for (int i = 0; i < fieldCount; i++)
    {
        getline(ss, fields[i]);
    }
}

void splitString(const string &input, string fields[], int fieldCount)
{
    istringstream ss(input);
    string field;
    int index = 0;

    while (index < fieldCount && getline(ss, field, ','))
    {
        fields[index++] = field;
    }

    while (index < fieldCount)
    {
        fields[index++] = ""; // Fill remaining fields with empty strings
    }
}

bool isValidUserName(const string &userName)
{
    if (userName.empty())
    {
        return false;
    }

    for (char ch : userName)
    {
        if (!isalpha(ch) && !isspace(ch))
        {
            return false;
        }
    }
    return true;
}
 string getField(const string& line, int fieldIndex) {
    string field;
    istringstream ss(line);
    string token;

    for (int i = 0; i <= fieldIndex; i++) {
        if (!std::getline(ss, token, ',')) {
            break;  // Handle incomplete lines
        }

        // Remove quotes if the field is enclosed in them
        if (!token.empty() && token.front() == '"' && token.back() == '"') {
            token = token.substr(1, token.length() - 2);
        }

        if (i == fieldIndex) {
            field = token;
        }
    }

    return field;
}

