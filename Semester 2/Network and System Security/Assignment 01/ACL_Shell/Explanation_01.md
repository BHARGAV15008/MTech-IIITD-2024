#### **1. aclManager.c**
- **Purpose**: Core ACL management functions.
- **Functions**:
  - `checkAcl(const char *path, const char *user, char mode)`: Checks if a user has the specified permission (`r`, `w`, `x`) via ACL or standard permissions.
    - Uses `getxattr` (Linux) or `extattr_get_file` (FreeBSD) to read the `user.acl` extended attribute.
    - Parses the ACL string (e.g., `user1,rwx user2,r`) and checks for user and permission matches.
    - Returns `1` if allowed, `0` if denied.
- **Key Inbuilt Functions**:
  - `getxattr`/`extattr_get_file`: Retrieve extended attributes (platform-specific).
  - `strtok_r`: Safely tokenizes the ACL string.
  - `strchr`: Splits username and permissions in ACL entries.

---

#### **2. create_dir.c**
- **Purpose**: Create directories with ACL and standard permission checks.
- **Workflow**:
  1. Checks write (`w`) permission on the parent directory using `checkAcl` and `access()`.
  2. Allows creation if either check passes.
- **Inbuilt Functions**:
  - `getpwuid`: Retrieves current user info.
  - `access`: Checks standard filesystem permissions.
  - `mkdir`: Creates the directory.

---

#### **3. fileOperations.c**
- **Purpose**: Read file contents securely.
- **Functions**:
  - `fget(const char *path)`: Reads and prints a file.
    - Checks read (`r`) permission via ACL and `access()`.
    - Drops privileges to the file owner’s UID if running as root (security measure).
    - Uses `O_NOFOLLOW` to prevent symlink attacks.
- **Inbuilt Functions**:
  - `open`/`read`/`write`: File I/O operations.
  - `setresuid`: Drops/restores privileges.

---

#### **4. fput.c**
- **Purpose**: Append data to a file.
- **Workflow**:
  - Checks write (`w`) permission via ACL or `access()`.
  - Opens the file in append mode (`O_APPEND`).
- **Inbuilt Functions**:
  - `open` with `O_APPEND`: Ensures atomic appends.
  - `write`: Adds data to the file.

---

#### **5. getacl.c**
- **Purpose**: Retrieve and display ACLs.
- **Workflow**:
  - Uses `getxattr` or `extattr_get_file` to fetch the `user.acl` attribute.
  - Prints "No ACL" if not found.
- **Inbuilt Functions**:
  - `printf`: Outputs the ACL string.

---

#### **6. main.c**
- **Purpose**: Shell interface for executing ACL-related commands.
- **Functions**:
  - `aclShell()`: A loop that parses commands like `fget`, `fput`, `my_ls`, etc.
  - Uses `fork` and `exec` to run external binaries (e.g., `my_ls`, `setacl`).
- **Inbuilt Functions**:
  - `fork`/`exec`: Spawns child processes.
  - `waitpid`: Waits for command completion.

---

#### **7. my_cd.c**
- **Purpose**: Change directory with ACL checks.
- **Workflow**:
  - Checks execute (`x`) permission on the target directory.
  - Uses `chdir` if allowed.
- **Inbuilt Functions**:
  - `chdir`: Changes the working directory.

---

#### **8. my_ls.c**
- **Purpose**: List directory contents.
- **Workflow**:
  - Checks read (`r`) permission via ACL or `access()`.
  - Uses `opendir`/`readdir` to list files.
- **Inbuilt Functions**:
  - `opendir`/`readdir`: Directory handling.

---

#### **9. setacl.c**
- **Purpose**: Set ACLs on files/directories.
- **Workflow**:
  - Validates that the caller is the file owner or root.
  - Writes the ACL string (e.g., `user1,rwx`) to the `user.acl` extended attribute.
- **Inbuilt Functions**:
  - `setxattr`/`extattr_set_file`: Sets extended attributes (platform-specific).

---

### Key Inbuilt Functions and Their Roles
1. **Extended Attribute Functions** (`getxattr`, `setxattr`, etc.):
   - **Why**: Platform-specific methods to read/write custom ACL metadata.
2. **Permission Checks** (`access`, `stat`):
   - **Why**: Validate standard filesystem permissions (DAC).
3. **User/Group Functions** (`getpwuid`, `getuid`):
   - **Why**: Identify the current user for ACL checks.
4. **File I/O** (`open`, `read`, `mkdir`, etc.):
   - **Why**: Perform file/directory operations securely.
5. **Process Control** (`fork`, `exec`, `waitpid`):
   - **Why**: Execute external commands in the shell safely.

---

### User-Defined Functions
- `checkAcl()` (aclManager.c):
  - **Why**: Centralizes ACL validation logic for reuse across programs.
- `fget()` (fileOperations.c):
  - **Why**: Encapsulates secure file reading with privilege management.

---

### Security Measures
- **Privilege Dropping**: In `fget`, root temporarily switches to the file owner’s UID.
- **Symlink Protection**: `O_NOFOLLOW` prevents symlink-based attacks.
- **Input Validation**: All programs check argument counts and paths.
- **ACL + DAC Hybrid**: Combines custom ACLs with traditional Unix permissions for flexibility.

---

### Summary
This codebase implements a hybrid permission system using extended attributes for ACLs. Each utility (e.g., `create_dir`, `my_ls`) integrates ACL checks alongside standard permissions, providing fine-grained access control. The shell (`main.c`) acts as a frontend, executing these utilities securely. Platform-specific code (Linux/FreeBSD) ensures compatibility, while security features like privilege dropping and symlink protection mitigate risks.