# Password Management CLI

<!-- #### Video Demo: <video URL> -->

### Description

Password Management CLI is a Python command-line application created as a CS50P final project. It provides a simple way to organize account records in CSV files, add account details, search saved records, and generate passwords. The application is designed as a learning project that demonstrates Python classes, functions, loops, conditional logic, exception handling, file I/O, CSV processing, path handling, and the use of a third-party package.

The program starts by asking which directory should be used for account categories. Pressing Enter selects the current working directory. Each CSV file directly inside that directory is treated as a category, so a user can separate records by purpose, such as personal accounts or work accounts. The main menu offers six actions: view or create a category, add account records, generate a password, search the selected directory, change the directory, and exit the program.

A category file stores four fields per record in this order: website or application, email, username, and password. New category files are created with the header `web/app,email,username,password`. The application uses Python's `csv` module to write and read records, rather than manually joining values with commas; this allows the CSV writer to handle fields that contain CSV-special characters. The `tabulate` package is used to display category contents and search results as readable tables.

The search feature scans CSV files in the selected directory. Users can search by website/application, username, email, or a combination of those fields. Pressing Enter skips a criterion, but at least one criterion must be supplied. Matching is case-insensitive and uses partial-text matching. When more than one criterion is supplied, all entered criteria must match the same record. Search results include the category filename and the matching record, including its password.

The password generator offers three levels. **Easy** allows digits and lowercase letters. **Normal** allows digits, lowercase letters, and uppercase letters. **Hard** allows digits, lowercase letters, uppercase letters, and punctuation symbols. It uses Python's `secrets` module to make random selections. In the current implementation, the selected level determines which character groups are available, but the generator does not guarantee that every enabled group appears in every generated password. The generator also selects a group before selecting a character, so characters are not selected uniformly from one combined character set.

## Requirements and Installation

Python 3.12 or newer is recommended because the source uses an f-string expression that relies on modern Python parsing behavior. The required third-party packages are listed in `requirements.txt`.

From the project directory, install the dependencies with:

```bash
python -m pip install -r requirements.txt
```

Start the application with:

```bash
python project.py
```

To run the automated tests, use:

```bash
python -m pytest -v
```

## Project Files

- **`project.py`** contains the application. The `CsvFile` class handles category paths, creation, display, record addition, and search. The `PassGen` class generates passwords. Top-level functions manage the interactive menu, user input, directory selection, and password-generation settings.
- **`test_project.py`** contains the `pytest` test suite. It follows the CS50P naming convention by naming tests with the `test_` prefix. Tests use temporary directories and controlled input so they can exercise features without intentionally editing the user's actual category files.
- **`requirements.txt`** lists the external packages required by the project: `tabulate` for table formatting and `pytest` for automated tests. Other imported modules, including `csv`, `pathlib`, `sys`, `string`, and `secrets`, belong to Python's standard library.
- **`README.md`** documents the purpose, setup, functionality, and limitations of the project.
- **Category CSV files** hold the account records. They are created by the program or may be supplied in the selected directory, provided that they follow the expected four-column format.

## Design Choices

CSV was chosen because it is built into Python, easy to inspect, and suitable for demonstrating file handling without requiring a database server. Using one CSV file per category keeps the organization simple and makes it possible to find categories by scanning the selected directory. `pathlib.Path` is used to build and inspect paths, `csv.reader` and `csv.writer` handle CSV data, and `secrets` is used instead of the general-purpose `random` module for password generation. `tabulate` improves readability by presenting records as tables in the terminal.

The application remains command-line based to keep the project focused on Python fundamentals rather than a graphical interface. Its features are intentionally limited: records can be viewed, created, added, searched, and passwords can be generated, but the current menu does not provide dedicated record-editing or record-deletion operations.

## Limitations and Security

This project is a programming demonstration and **is not a secure password manager for real credentials**. Passwords are stored in CSV files as plain text, so anyone who can access a category file can read the saved passwords. The application has no master password, authentication, encryption, or access-control layer. Generated and searched passwords are displayed in the terminal, which can expose them to people nearby or to screen recording and logging tools.

The program expects each account row to contain exactly four fields in the documented order. Manually modified or malformed CSV files can cause records to be skipped during search or can trigger errors in display operations. Input validation and file-error handling are not comprehensive, and filename/path edge cases are not fully restricted. Search checks only the CSV files directly within the selected directory; it does not recursively scan subdirectories or search the password field. Category files are not explicitly sorted before being shown in the menus.

Use dummy credentials when demonstrating or testing this project. Do not commit real credential CSV files to a public Git repository or upload them to an untrusted service. Adding CSV files to `.gitignore` can help prevent accidental commits, but it does not encrypt files or remove copies that have already been committed. For real accounts, use a reputable password manager designed to protect credentials.
