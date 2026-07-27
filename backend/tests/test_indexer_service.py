"""Tests for FileIndexerService."""

from pathlib import Path

from app.services.indexer_service import FileIndexerService


def test_index_directory(tmp_path: Path) -> None:
    """Test directory indexing with sample directory structure."""
    repo_dir = tmp_path / "mock_repo"
    repo_dir.mkdir()

    # Create subfolders
    src_dir = repo_dir / "src"
    src_dir.mkdir()
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir()
    git_dir = repo_dir / ".git"
    git_dir.mkdir()

    # Create files
    (repo_dir / "README.md").write_text("# Mock Repo", encoding="utf-8")
    (src_dir / "main.py").write_text("print('hello world')", encoding="utf-8")
    (src_dir / "utils.py").write_text("def add(a, b): return a + b", encoding="utf-8")
    (docs_dir / "info.txt").write_text("some docs", encoding="utf-8")
    (git_dir / "config").write_text(
        "git config here", encoding="utf-8"
    )  # should be ignored

    index_data = FileIndexerService.index_directory(str(repo_dir))

    assert index_data["file_count"] == 4  # README.md, main.py, utils.py, info.txt
    assert index_data["folder_count"] == 2  # src, docs (.git is ignored)
    assert index_data["max_depth"] == 1
    assert index_data["file_extensions"][".py"] == 2
    assert index_data["file_extensions"][".md"] == 1
    assert index_data["language_distribution"]["Python"]["files"] == 2
    assert len(index_data["largest_files"]) <= 10
