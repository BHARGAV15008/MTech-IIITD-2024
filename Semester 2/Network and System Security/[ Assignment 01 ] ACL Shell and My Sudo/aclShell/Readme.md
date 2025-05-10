# ACL Shell

The ACL Shell is a custom shell program that provides a secure way to manage files and directories using Access Control Lists (ACLs). It supports commands for file operations, directory operations, and ACL management.

## Table of Contents

- [Features](#features)
- [Building the Project](#building-the-project)
- [Running the ACL Shell](#running-the-acl-shell)
- [Supported Commands](#supported-commands)
  - [File Operations](#file-operations)
  - [Directory Operations](#directory-operations)
  - [ACL Management](#acl-management)
- [Examples](#examples)
- [Exit the Shell](#exit-the-shell)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **File Operations:** Read and append data to files.
- **Directory Operations:** List directory contents and change directories.
- **ACL Management:** Set and retrieve ACL permissions for files and directories.
- **Security:** Ensures only authorized users can perform operations based on ACLs.

## Building the Project

To build the project, follow these steps:

### Clone the Repository (if applicable)
```bash
git clone <repository-url>
cd ACL_Shell
```

### Build the Project
Run the following command to compile the project:
```bash
make
```

### Clean the Build (optional)
To remove compiled files, run:
```bash
make clean
```

## Running the ACL Shell

To start the ACL Shell, run the following command:
```bash
./aclShell
```

You will see the prompt:
```bash
ACLShell>
```

## Supported Commands

### File Operations

#### `fget <file>`
Read and display the contents of a file.
**Example:**
```bash
ACLShell> fget example.txt
```

#### `fput <file>`
Append data to a file.
**Example:**
```bash
ACLShell> fput example.txt
```

### Directory Operations

#### `my_ls <directory>`
List the contents of a directory.
**Example:**
```bash
ACLShell> my_ls .
```

#### `my_cd <directory>`
Change the current directory.
**Example:**
```bash
ACLShell> my_cd /home/user
```

#### `create_dir <directory>`
Create a new directory.
**Example:**
```bash
ACLShell> create_dir new_directory
```

### ACL Management

#### `setacl <file> <user> <permissions>`
Set ACL permissions for a file.
**Example:**
```bash
ACLShell> setacl example.txt user1,rw
```

#### `getacl <file>`
Get ACL permissions for a file.
**Example:**
```bash
ACLShell> getacl example.txt
```

## Exit the Shell

To exit the ACL Shell and return to the system shell, use the `exit` command.
**Example:**
```bash
ACLShell> exit
```

## Examples

### List Files in a Directory
```bash
ACLShell> my_ls .
file1.txt
file2.txt
directory1
```

### Read a File
```bash
ACLShell> fget file1.txt
This is the content of file1.txt.
```

### Append Data to a File
```bash
ACLShell> fput file1.txt
```

### Set ACL Permissions
```bash
ACLShell> setacl file1.txt user1,rw
ACL set successfully
```

### Get ACL Permissions
```bash
ACLShell> getacl file1.txt
ACL: user1,rw
```

### Create a Directory
```bash
ACLShell> create_dir new_directory
Directory created successfully
```

## Troubleshooting

### Command Not Found
Ensure you are using the supported commands listed above. Standard shell commands like `ls`, `cd`, and `mkdir` are not supported.

### Permission Denied
Ensure you have the necessary ACL and DAC permissions to perform the operation.

### Build Errors
- Ensure all required files (`aclManager.c`, `fileOperations.c`, etc.) are present in the directory.
- If you encounter errors related to `sys/xattr.h`, ensure you are on a system that supports it (e.g., Linux). For FreeBSD, use `sys/extattr.h`.

### File Not Found
Ensure the file or directory you are referencing exists.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

