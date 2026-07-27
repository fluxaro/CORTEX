"""Tests for duplication detection engine."""

from app.analyzers.shared.duplication import DuplicationDetector


def test_duplicate_code_detection() -> None:
    """Test detecting duplicated blocks across multiple files."""
    duplicated_block = """
def common_logic_function(val):
    x = val * 2
    y = x + 10
    z = y / 2
    print("processing", z)
    return z
"""

    file1 = "file1.py\n" + duplicated_block
    file2 = "file2.py\n" + duplicated_block

    file_map = {
        "file1.py": file1,
        "file2.py": file2,
        "unique.py": "def unique():\n    return 42\n",
    }

    groups, dup_pct = DuplicationDetector.detect_duplicates(file_map, min_lines=5)

    assert len(groups) >= 1
    assert dup_pct > 0.0
    assert groups[0].instance_count == 2
