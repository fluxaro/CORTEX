"""Tests for ReadmeAnalyzer markdown section parser."""

from app.analyzers.maintainability.analyzers.readme_analyzer import ReadmeAnalyzer


def test_readme_analyzer_sections() -> None:
    """Test detecting README sections, completeness %, and badges."""
    readme_content = """# My Project
## Description
An awesome software platform.

## Installation
```bash
pip install mypkg
```

## Quick Start
Run `python main.py`.

## Features
- Scalable
- Fast

## License
MIT License
"""

    file_contents = {"README.md": readme_content}
    res = ReadmeAnalyzer.analyze(file_contents)

    assert res.completeness_percentage > 20.0
    assert "Title" in res.detected_sections
    assert "Installation" in res.detected_sections
    assert "Features" in res.detected_sections
    assert "License" in res.detected_sections
    assert "Architecture" in res.missing_sections
