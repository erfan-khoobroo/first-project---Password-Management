"""Pytest tests for the CS50P Password Management final project.

Expected project layout:
    project.py
    test_project.py
    requirements.txt

Run from the project root:
    python -m pip install -r requirements.txt
    python -m pip install pytest
    python -m pytest -v

Tests use temporary directories, so they do not modify the user's real CSV files.
"""

import csv
import string
from pathlib import Path

import pytest

import project as app


HEADERS = ["web/app", "email", "username", "password"]


def write_category(directory: Path, filename: str, rows=()) -> Path:
    """Create a CSV category with this project's current column order."""
    path = directory / filename
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(HEADERS)
        writer.writerows(rows)
    return path


def feed_inputs(monkeypatch, values):
    """Feed a sequence of responses to calls of input()."""
    responses = iter(values)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(responses))


# The following tests use the exact test_<function_name> naming convention
# required by the CS50P final-project instructions.


def test_select_home_options(monkeypatch, capsys):
    """Reject invalid choices and return a valid menu selection."""
    feed_inputs(monkeypatch, ["abc", "9", " 2 "])

    assert app.select_home_options(["one", "two", "three"]) == "2"
    assert "Invalid" in capsys.readouterr().out


def test_get_pass(monkeypatch, capsys):
    """Retry invalid difficulty/length inputs and generate the requested length."""
    feed_inputs(monkeypatch, ["extreme", "normal", "0", "not-a-number", "12"])

    password = app.get_pass()

    allowed = string.digits + string.ascii_lowercase + string.ascii_uppercase
    assert isinstance(password, str)
    assert len(password) == 12
    assert all(character in allowed for character in password)
    assert "Invalid input" in capsys.readouterr().out


def test_dir_verify(monkeypatch, tmp_path, capsys):
    """Accept valid paths, use cwd for blank input, retry, and fall back safely."""
    assert app.dir_verify("") == Path.cwd()
    assert app.dir_verify(tmp_path) == tmp_path

    feed_inputs(monkeypatch, [str(tmp_path)])
    assert app.dir_verify("path-that-does-not-exist-for-this-test", n_try=2) == tmp_path

    feed_inputs(monkeypatch, ["still-invalid-path-one", "still-invalid-path-two"])
    assert app.dir_verify("invalid-starting-path-for-this-test", n_try=2) == Path.cwd()
    assert "default program execution path" in capsys.readouterr().out


def test_y_or_n():
    """Recognize affirmative inputs; other values return False."""
    for answer in ["y", "Y", "yes", " YES "]:
        assert app.y_or_n(answer) is True

    for answer in ["n", "no", "maybe", "", "  "]:
        assert app.y_or_n(answer) is False


def test_vc_cat(tmp_path, monkeypatch, capsys):
    """Create a category in an empty directory and display an existing category."""
    feed_inputs(monkeypatch, ["1", "new-category", "n"])
    app.vc_cat(tmp_path)

    created_file = tmp_path / "new-category.csv"
    assert created_file.exists()
    with created_file.open(newline="", encoding="utf-8") as file:
        assert next(csv.reader(file)) == HEADERS

    existing_dir = tmp_path / "existing-category-test"
    existing_dir.mkdir()
    write_category(
        existing_dir,
        "work.csv",
        [["GitHub", "alice@example.com", "alice", "DemoPass123"]],
    )
    feed_inputs(monkeypatch, ["1", "n"])
    app.vc_cat(existing_dir)
    output = capsys.readouterr().out
    assert "GitHub" in output
    assert "alice@example.com" in output


def test_add_ap(tmp_path, monkeypatch, capsys):
    """Handle an empty directory and add a generated-password record."""
    assert app.add_ap(tmp_path) is None
    assert "haven't created any categories" in capsys.readouterr().out

    write_category(tmp_path, "work.csv")
    feed_inputs(monkeypatch, ["1", "GitHub", "alice@example.com", "alice", "y", "n"])
    monkeypatch.setattr(app, "get_pass", lambda: "Generated123")

    app.add_ap(tmp_path)

    with (tmp_path / "work.csv").open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
    assert rows[0] == HEADERS
    assert rows[1] == ["GitHub", "alice@example.com", "alice", "Generated123"]


def test_main(monkeypatch):
    """Exit cleanly when the user selects option 6."""
    feed_inputs(monkeypatch, ["", "6"])

    with pytest.raises(SystemExit) as exc_info:
        app.main()

    assert "Thank you for using the app" in str(exc_info.value)


# Tests for the CsvFile class. These are additional to the required top-level
# function tests above.


def test_create_cat(tmp_path, capsys):
    category = app.CsvFile("work", tmp_path)

    assert category.create_cat() is True
    assert category.path_file.exists()
    with category.path_file.open(newline="", encoding="utf-8") as file:
        assert next(csv.reader(file)) == HEADERS
    assert "work.csv" in capsys.readouterr().out

    original_content = category.path_file.read_text(encoding="utf-8")
    assert app.CsvFile("work", tmp_path).create_cat() is False
    assert category.path_file.read_text(encoding="utf-8") == original_content


def test_all_cat(tmp_path):
    write_category(tmp_path, "one.csv")
    (tmp_path / "notes.txt").write_text("not a category", encoding="utf-8")
    (tmp_path / "folder.csv").mkdir()

    files = app.CsvFile.all_cat(tmp_path)
    assert {path.name for path in files} == {"one.csv"}


def test_str_for_empty_and_populated_category(tmp_path):
    empty = app.CsvFile("empty", tmp_path)
    assert empty.create_cat() is True
    assert "haven't added an account" in str(empty)

    write_category(
        tmp_path,
        "work.csv",
        [["GitHub", "alice@example.com", "alice", "DemoPass123"]],
    )
    rendered = str(app.CsvFile("work", tmp_path))
    for value in ["GitHub", "alice@example.com", "alice", "DemoPass123"]:
        assert value in rendered


def test_add_data_to_cat_with_generated_password(tmp_path, monkeypatch, capsys):
    category = app.CsvFile("work", tmp_path)
    assert category.create_cat() is True
    feed_inputs(monkeypatch, ["GitHub", "alice@example.com", "alice", "y"])
    monkeypatch.setattr(app, "get_pass", lambda: "Generated123")

    assert category.add_data_to_cat() is True
    with category.path_file.open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
    assert rows[0] == HEADERS
    assert rows[1] == ["GitHub", "alice@example.com", "alice", "Generated123"]
    assert "Successfully added" in capsys.readouterr().out


def test_add_data_to_cat_with_manual_password(tmp_path, monkeypatch):
    category = app.CsvFile("work", tmp_path)
    category.create_cat()
    feed_inputs(
        monkeypatch,
        ["GitHub", "alice@example.com", "alice", "n", "ManualPass123"],
    )

    assert category.add_data_to_cat() is True
    with category.path_file.open(newline="", encoding="utf-8") as file:
        rows = list(csv.reader(file))
    assert rows[1] == ["GitHub", "alice@example.com", "alice", "ManualPass123"]


@pytest.mark.parametrize(
    ("level", "allowed_characters"),
    [
        (1, string.digits + string.ascii_lowercase),
        (2, string.digits + string.ascii_lowercase + string.ascii_uppercase),
        (
            3,
            string.digits
            + string.ascii_lowercase
            + string.ascii_uppercase
            + string.punctuation,
        ),
    ],
)
@pytest.mark.parametrize("length", [1, 8, 24])
def test_generate(level, allowed_characters, length):
    """Ensure PassGen produces the requested length and allowed character set."""
    password = app.PassGen(level, length).generate()

    assert isinstance(password, str)
    assert len(password) == length
    assert all(character in allowed_characters for character in password)


def test_search(tmp_path, monkeypatch, capsys):
    """Test no-files, blank criteria, matching, case-insensitivity, and bad rows."""
    assert app.CsvFile.search(tmp_path) is False
    assert "No CSV files" in capsys.readouterr().out

    write_category(
        tmp_path,
        "work.csv",
        [
            ["GitHub", "alice@example.com", "alice", "AlphaPass"],
            ["GitLab", "alice@example.com", "bob", "BetaPass"],
            ["GitHub", "bob@example.com", "alice", "GammaPass"],
        ],
    )

    feed_inputs(monkeypatch, ["", "", ""])
    assert app.CsvFile.search(tmp_path) is False
    assert "at least one search criterion" in capsys.readouterr().out

    feed_inputs(monkeypatch, ["gIt", "ALICE", "alice@example.com"])
    assert app.CsvFile.search(tmp_path) is True
    output = capsys.readouterr().out
    assert "Found 1 matching account" in output
    assert "AlphaPass" in output
    assert "BetaPass" not in output
    assert "GammaPass" not in output
    assert "work" in output


def test_search_multiple_categories_and_malformed_rows(tmp_path, monkeypatch, capsys):
    write_category(tmp_path, "work.csv", [["GitHub", "a@example.com", "alice", "Pass1"]])
    write_category(tmp_path, "personal.csv", [["GitHub", "b@example.com", "bob", "Pass2"]])
    feed_inputs(monkeypatch, ["github", "", ""])

    assert app.CsvFile.search(tmp_path) is True
    output = capsys.readouterr().out
    assert "Found 2 matching account" in output
    assert "work" in output and "personal" in output
    assert "Pass1" in output and "Pass2" in output

    malformed = tmp_path / "broken.csv"
    malformed.write_text(
        "web/app,email,username,password\nGitHub,a@example.com,alice\n",
        encoding="utf-8",
    )
    feed_inputs(monkeypatch, ["not-found", "", ""])
    assert app.CsvFile.search(tmp_path) is False
    output = capsys.readouterr().out
    assert "Value count error" in output
    assert "No matching accounts found" in output
