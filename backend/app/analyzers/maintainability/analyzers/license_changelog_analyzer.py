"""License identification and CHANGELOG analyzer."""

import re

from app.analyzers.maintainability.models import LicenseResult


class LicenseChangelogAnalyzer:
    """Analyzes open source licenses and CHANGELOG release histories."""

    LICENSE_PATTERNS = [
        ("MIT", r"MIT License|Permission is hereby granted, free of charge", True),
        ("Apache-2.0", r"Apache License.*Version 2\.0", True),
        ("GPL-3.0", r"GNU GENERAL PUBLIC LICENSE.*Version 3", True),
        ("BSD-3-Clause", r"Redistribution and use in source and binary forms", True),
        ("MPL-2.0", r"Mozilla Public License.*v\. 2\.0", True),
        ("AGPL-3.0", r"GNU AFFERO GENERAL PUBLIC LICENSE", True),
        ("LGPL-3.0", r"GNU LESSER GENERAL PUBLIC LICENSE", True),
        (
            "Unlicense",
            r"This is free and unencumbered software released into the public domain",
            True,
        ),
    ]

    @classmethod
    def analyze_license(cls, file_contents: dict[str, str]) -> LicenseResult:
        """Identify repository license and OSI approval."""
        lic_content = ""
        has_file = False
        for path, content in file_contents.items():
            if "license" in path.lower():
                lic_content = content
                has_file = True
                break

        if not has_file or not lic_content:
            return LicenseResult(
                spdx_identifier="NOASSERTION",
                is_osi_approved=False,
                has_license_file=False,
                is_consistent=False,
            )

        for spdx, pattern, osi in cls.LICENSE_PATTERNS:
            if re.search(pattern, lic_content, re.IGNORECASE):
                return LicenseResult(
                    spdx_identifier=spdx,
                    is_osi_approved=osi,
                    has_license_file=True,
                    is_consistent=True,
                )

        return LicenseResult(
            spdx_identifier="Custom",
            is_osi_approved=False,
            has_license_file=True,
            is_consistent=True,
        )

    @classmethod
    def analyze_changelog(cls, file_contents: dict[str, str]) -> tuple[bool, bool]:
        """Check for CHANGELOG.md and Semantic Versioning compliance."""
        has_changelog = False
        uses_semver = False

        for path, content in file_contents.items():
            if (
                "changelog" in path.lower()
                or "history" in path.lower()
                or "release" in path.lower()
            ):
                has_changelog = True
                if re.search(r"v?\d+\.\d+\.\d+", content):
                    uses_semver = True
                break

        return has_changelog, uses_semver
