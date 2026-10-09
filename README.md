# Password Management CLI

A small command-line password management project written in Python. It stores account records in CSV files, lets users organize those records into categories, search saved accounts, and generate passwords at three difficulty levels.

> **Security warning:** This is a learning project, not a secure production password manager. Passwords are stored in CSV files as plain text. Anyone who can read those files can read the saved passwords. Use only dummy or non-sensitive credentials unless you understand and accept this risk.

## Features

- **CSV categories:** Each `.csv` file in the selected directory acts as a category, such as `personal.csv` or `work.csv`.
- **View or create categories:** Select an existing CSV category to display its records, or create a new category.
- **Add account records:** Save a website/app name, email, username, and password.
- **Password generator:** Generate a password using one of three character sets:
  - **Easy:** digits and lowercase letters.
  - **Normal:** digits, lowercase letters, and uppercase letters.
  - **Hard:** digits, lowercase letters, uppercase letters, and punctuation symbols.
- **Search records:** Search all CSV files in the selected directory by website/app, email, and/or username. Leave a field blank to skip it. Searches are case-insensitive and use partial-text matching; all supplied criteria must match the same record.
- **Change directory:** Switch to another existing directory containing CSV categories.
- **Tabular output:** Display category records and search results in tables using `tabulate`.

## Requirements

- Python **3.12 or newer** is recommended for the source as currently written.
- The third-party Python package [`tabulate`](https://pypi.org/project/tabulate/).
- All other imported modules (`csv`, `pathlib`, `sys`, `string`, and `secrets`) are part of Python's standard library.

## Installation

1. Make sure Python is installed.
2. Install the dependency:

   ```bash
   python -m pip install tabulate
   ```

3. Save the program in a Python file. The examples below use `project.py`; replace that name with the actual filename if yours is different.

## Run

From a terminal, navigate to the directory containing the Python file and run:

```bash
python project.py
```

At startup, enter a directory containing the CSV categories you want to use. Press **Enter** to use the current working directory. The program validates the directory and falls back to the current working directory after repeated invalid paths.

## Main menu

1. **View or create account and password categories** — choose an existing CSV file to view its records, or create a new category in the selected directory.
2. **Add account-password** — choose a category and add one or more records.
3. **Password generation** — generate and display a password without saving it to a category.
4. **Search this directory** — search the CSV categories in the selected directory.
5. **Change directory** — select a different directory.
6. **Exit** — leave the program.

## CSV format

The program creates category files with this header and column order:

```csv
web/app,email,username,password
```

Each account record uses the same order:

```csv
Example Service,person@example.com,example_user,example_password
```

Keep this four-column order when editing files manually. Search and display functions assume that each record contains exactly four fields. Rows with a different number of fields may be skipped during search or may cause display problems.

## Search behavior

- You can enter one, two, or all three search criteria: website/app, username, and email.
- Pressing **Enter** for a criterion skips that field.
- At least one criterion must be provided.
- Matching is case-insensitive and looks for the entered text anywhere inside the corresponding field.
- When multiple criteria are supplied, all of them must match the same row.
- Search results include the category name and the saved password.

## Password generation notes

The generator uses Python's `secrets` module to make random choices, which is preferable to the general-purpose `random` module for password generation. However, the current implementation chooses a character group for each position and then chooses a character from that group. As a result, characters are not uniformly selected from the combined character set, and the generator does **not** guarantee that every character group for a selected level appears in each generated password. A level describes the available character groups, not a guaranteed composition rule.

## Limitations and known shortcomings

- **No encryption:** CSV files contain passwords in plain text.
- **No master password or access control:** The program does not authenticate users or restrict access to saved files.
- **No secure deletion or editing workflow:** The current menu supports viewing, creating categories, adding records, searching, and generating passwords; it does not provide dedicated operations to edit or delete individual records.
- **Search is limited:** Search checks website/app, email, and username, not the password field. It searches only CSV files directly inside the selected directory, not subdirectories.
- **CSV files must follow the expected schema:** The program assumes the four columns are in the documented order. Manually altered headers or malformed rows can lead to skipped results or display errors.
- **Password composition is not guaranteed:** The generator does not guarantee at least one digit, uppercase letter, lowercase letter, or symbol from each enabled group.
- **Generated and saved passwords are shown in the terminal:** Be aware of screen sharing, terminal history/recording tools, and anyone looking at your screen.
- **Limited data validation:** The program does not fully validate website names, email addresses, usernames, or every possible filename/path edge case.
- **File-operation errors are not handled uniformly:** Some file errors are reported, but others may still interrupt an operation with a Python error message.
- **Category order is not guaranteed:** CSV categories are not explicitly sorted before being shown in menus.

## Advantages

- Small, straightforward command-line interface.
- Uses Python standard-library tools for CSV handling, paths, and secure random selection.
- CSV data is human-readable and can be inspected with a text editor or spreadsheet application.
- Supports multiple categories without requiring a database server.
- Search supports partial matches and case-insensitive matching.
- The code demonstrates classes, functions, loops, pattern matching, file handling, exception handling, and interaction with a third-party package.

## Privacy and safe use

Treat every category CSV file as sensitive. Store it only in a location you control, avoid committing real credential files to Git, and do not upload them to public repositories or share them through untrusted services. Adding a CSV file to `.gitignore` can reduce the chance of accidentally committing it, but it does not encrypt the file or protect copies already committed or shared.

For real accounts, use a reputable password manager designed to protect credentials. This project is best treated as a small Python learning/demo application.

## License

No license is specified in the source provided with this project. Add a `LICENSE` file if you want to publish the project with explicit reuse terms.
