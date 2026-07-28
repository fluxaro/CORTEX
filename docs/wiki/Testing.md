# Testing Guide

ProjectIQ maintains a comprehensive test suite with **61 tests** organized across multiple test files.

---

## Running Tests

```bash
# Full test suite
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests

# With verbose output
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests -v

# Run specific test file
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests/test_enterprise.py

# Run specific test
$env:PYTHONPATH="backend"; .venv\Scripts\pytest.exe backend/tests/test_enterprise.py::test_user_registration
```

---

## Test Organization

| File | Tests | Coverage Area |
| :--- | :--- | :--- |
| `test_repositories.py` | ~10 | Repository ingestion, file indexing, CRUD |
| `test_analysis.py` | ~10 | Static code analysis metrics, smells, duplication |
| `test_architecture.py` | ~8 | Architecture style detection, pattern finding |
| `test_security.py` | ~8 | SAST findings, secret scanner, config audit |
| `test_maintainability.py` | ~8 | Docs, testing, CI, Git history analysis |
| `test_iq.py` | ~8 | IQ scoring, debt estimation, benchmarking |
| `test_enterprise.py` | ~9 | Auth, RBAC, workspaces, git sync, notifications |

---

## Test Patterns

All tests use `pytest-asyncio` with an in-memory SQLite database for complete isolation:

```python
@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Create an isolated in-memory SQLite database per test."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSession(engine) as session:
        yield session
    await engine.dispose()
```

---

## Writing New Tests

```python
@pytest.mark.asyncio
async def test_your_feature(db: AsyncSession) -> None:
    """Test description."""
    # Arrange
    service = YourService(db)
    request = YourCreateRequest(field="value")

    # Act
    result = await service.create(request)

    # Assert
    assert result.field == "value"
    assert result.id is not None
```
