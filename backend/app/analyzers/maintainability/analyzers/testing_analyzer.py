"""Testing framework and test suite maturity analyzer."""

import re

from app.analyzers.maintainability.models import TestingResult


class TestingAnalyzer:
    """Detects test runners, test suite file structures, mock usage, and testing maturity."""

    @classmethod
    def analyze(  # noqa: C901
        cls, file_paths: list[str], file_contents: dict[str, str]
    ) -> TestingResult:
        """Analyze testing structure and frameworks."""
        paths_lower = [p.lower() for p in file_paths]

        frameworks = []
        if any("pytest" in c or "import pytest" in c for c in file_contents.values()):
            frameworks.append("Pytest")
        if any(
            "unittest" in c or "import unittest" in c for c in file_contents.values()
        ):
            frameworks.append("Unittest")
        if any(
            "jest" in c or "describe(" in c or "it(" in c
            for c in file_contents.values()
        ):
            frameworks.append("Jest")
        if any("vitest" in c for c in file_contents.values()):
            frameworks.append("Vitest")
        if any("mocha" in c for c in file_contents.values()):
            frameworks.append("Mocha")
        if any("_test.go" in p for p in paths_lower):
            frameworks.append("Go Test")
        if any("junit" in c or "@Test" in c for c in file_contents.values()):
            frameworks.append("JUnit")
        if any("[test]" in c or "#[test]" in c for c in file_contents.values()):
            frameworks.append("Cargo Test")

        test_files = [
            p
            for p in file_paths
            if "test" in p.lower()
            or "spec" in p.lower()
            or p.lower().endswith("_test.go")
        ]
        test_file_count = len(test_files)

        estimated_tests = 0
        has_mocks = False
        has_unit = False
        has_integration = False
        has_e2e = False

        for path, content in file_contents.items():
            path_lower = path.lower()
            if "test" not in path_lower and "spec" not in path_lower:
                continue

            test_matches = len(
                re.findall(
                    r"(?i)\b(def test_|it\(|test\(|void test|@Test|fn test_)", content
                )
            )
            estimated_tests += test_matches

            if (
                "mock" in content.lower()
                or "fixture" in content.lower()
                or "jest.fn" in content.lower()
            ):
                has_mocks = True

            if "integration" in path_lower:
                has_integration = True
            elif (
                "e2e" in path_lower
                or "cypress" in path_lower
                or "playwright" in path_lower
            ):
                has_e2e = True
            else:
                has_unit = True

        # Compute testing maturity score (0-100)
        score = 0.0
        if test_file_count > 0:
            score += min(test_file_count * 5.0, 40.0)
        if len(frameworks) > 0:
            score += 20.0
        if has_unit:
            score += 15.0
        if has_integration:
            score += 15.0
        if has_e2e:
            score += 5.0
        if has_mocks:
            score += 5.0

        return TestingResult(
            testing_score=round(min(score, 100.0), 1),
            frameworks=list(set(frameworks)),
            test_file_count=test_file_count,
            estimated_test_count=max(estimated_tests, test_file_count),
            has_unit_tests=has_unit,
            has_integration_tests=has_integration,
            has_e2e_tests=has_e2e,
            has_mocks=has_mocks,
        )
