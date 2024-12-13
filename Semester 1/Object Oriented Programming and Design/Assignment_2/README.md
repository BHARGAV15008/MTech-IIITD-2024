# Academic Departments Information System
## Overview
> The Academic Departments Information System is a C++ program that manages information about faculty members across various academic departments. The system allows users to search for faculty members based on their names and retrieves detailed information about them, including their department, email ID, telephone number, and room number.

## Features
> Department Management: Supports multiple academic departments, including:
> - Computational Biology
> - Computer Science & Engineering
> - Electronics & Communications Engineering
> - Social Sciences & Humanities
> - Human Centered Design
> - Faculty Information Retrieval:

> Search for faculty members by name.
> Displays detailed information about the faculty member, including:
> - Name
> - Position
> - Department
> - Email ID
> - Telephone Number
> - Room Number

> Case-Insensitive Search: The search functionality is case-insensitive, making it user-friendly.

> Classes

>> PersonInformation:

>>> Base class containing common attributes and methods for faculty members.

>> AcademicDepartments:

>>> *Derived class that represents an academic department and extends the PersonInformation class.*

>>Specific Department Classes:

>>>ComputationBiology

>>>ComputerScience

>>>ElectronicsCommunications

>>>SocialSciencesAndHumanities

>>>HumanCenteredDesign

>> These classes inherit from AcademicDepartments and set the specific department name.

> Academics:
 - Manages a collection of academic departments and provides methods to add departments and fetch faculty information.

    ```bash
    g++ -o academic_departments academic_departments.cpp
    ```
Run the compiled program:

    ```bash
    ./academic_departments
    ```
Input the name of the person whose information you wish to retrieve when prompted.

Example
When the program is executed, it will prompt for the name:

    ```python
    Enter the name of the person who is present in any department:
    ```
If a matching faculty member is found, their information will be displayed as follows:

    ```mathematica
    Arjun Ray  ( Assistant Professor )
    -----------------------------------------------------------
    Department          : Computational Biology
    Email Id            : arjun@iiitd.ac.in
    Telephone Number    : 011-26907438
    Room Number         : A-310 (R&D Block)
    ```
Input Validation
    The program checks for valid name inputs, ensuring only alphabetical characters and spaces are allowed. If an invalid name is entered, the ```program will display an error message:
    Invalid Name...
    ```