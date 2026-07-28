"""Registry for security scanners."""

from typing import ClassVar

from app.analyzers.security.base_scanner import BaseSecurityScanner


class SecurityScannerRegistry:
    """Registry managing active security scanners."""

    _scanners: ClassVar[dict[str, BaseSecurityScanner]] = {}

    @classmethod
    def register(cls, scanner: BaseSecurityScanner) -> None:
        """Register a security scanner."""
        cls._scanners[scanner.scanner_name.lower()] = scanner

    @classmethod
    def get_all_scanners(cls) -> list[BaseSecurityScanner]:
        """Retrieve all registered scanners."""
        return list(cls._scanners.values())

    @classmethod
    def clear(cls) -> None:
        """Clear registered scanners."""
        cls._scanners.clear()
