"""Unit tests for preprocess json scripts."""

# pylint: disable=W0621,C1803
import json
from pathlib import Path
from unittest.mock import patch

from _pytest.capture import CaptureFixture
import pytest

from recruitair.data.preprocess_json import find_target_json_files, process_file


def test_find_target_json_files(tmp_path: Path):
    """
    Test that find_target_json_files correctly finds matching files.
    """
    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()

    (tmp_path / "match_1.json").touch()
    (tmp_path / "mismatch_123.json").touch()
    (sub_dir / "match_2.json").touch()
    (tmp_path / "MATCH_3.json").touch()

    (tmp_path / "other.json").touch()
    (tmp_path / "match_4.txt").touch()
    (tmp_path / "mismatch_abc.json").touch()

    found_files = find_target_json_files(tmp_path)

    assert len(found_files) == 4
    assert found_files == sorted(
        [
            tmp_path / "MATCH_3.json",
            tmp_path / "match_1.json",
            tmp_path / "mismatch_123.json",
            sub_dir / "match_2.json",
        ]
    )


def test_find_target_json_files_empty(tmp_path: Path):
    """
    Test find_target_json_files returns an empty list for a directory with no matching files.
    """
    (tmp_path / "other.json").touch()
    (tmp_path / "data.txt").touch()

    found_files = find_target_json_files(tmp_path)

    assert found_files == []


@pytest.fixture
def valid_json_content():
    """Fixture for a valid json resume."""
    return {
        "input": {
            "job_description": "This is the job description.",
            "macro_dict": {"experience": 0.5},
            "micro_dict": {"python": 0.4},
        },
    }


def test_process_file_success(tmp_path: Path, valid_json_content: dict):
    """
    Test successful processing of a valid JSON file.
    """
    file_path = tmp_path / "test.json"
    file_path.write_text(json.dumps(valid_json_content))

    result = process_file(file_path)
    expected = {
        "job_description": "This is the job description.",
        "criteria": [
            {"name": "experience", "importance": 0.5},
            {"name": "python", "importance": 0.4},
        ],
    }
    assert result == expected


def test_process_file_not_found(capsys: CaptureFixture):
    """
    Test process_file handles a non-existent file gracefully.
    """
    result = process_file(Path("non_existent_file.json"))
    assert result == None
    captured = capsys.readouterr()
    assert "WARNING: Failed to parse non_existent_file.json: " in captured.err


def test_process_file_invalid_json(tmp_path: Path, capsys: CaptureFixture):
    """
    Test process_file handles a file with invalid JSON.
    """
    file_path = tmp_path / "invalid.json"
    file_path.write_text("{ not json }")

    result = process_file(file_path)

    assert result == None
    captured = capsys.readouterr()
    assert f"WARNING: Failed to parse {file_path}: " in captured.err


def test_process_file_no_job_description(tmp_path: Path, valid_json_content: dict, capsys: CaptureFixture):
    """
    Test process_file handles a file with no job description.
    """
    del valid_json_content["input"]["job_description"]
    file_path = tmp_path / "no_job_description.json"
    file_path.write_text(json.dumps(valid_json_content))

    result = process_file(file_path)

    assert result == None
    captured = capsys.readouterr()
    assert f"WARNING: No job description found in {file_path}" in captured.err


def test_process_file_missing_criteria(tmp_path: Path, valid_json_content: dict):
    """
    Test process_file handles a file with missing scores gracefully.
    """
    del valid_json_content["input"]["macro_dict"]
    del valid_json_content["input"]["micro_dict"]
    file_path = tmp_path / "no_criteria.json"
    file_path.write_text(json.dumps(valid_json_content))

    result = process_file(file_path)

    assert result == None
