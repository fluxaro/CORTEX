"""Tests for SASTRules static security rule scanner."""

from app.analyzers.security.scanners.sast_rules import SASTRules


def test_sast_rules_dangerous_functions() -> None:
    """Test detecting eval(), exec(), pickle, and SQL injection risks."""
    file_map = {
        "app.py": "eval('print(1)')\nimport pickle\npickle.loads(user_data)\nimport os\nos.system('rm -rf /')\n",
        "db.py": "query = 'SELECT * FROM users WHERE id = ' + user_id\n",
    }

    scanner = SASTRules()
    res = scanner.scan("/tmp", file_map)

    assert len(res.findings) >= 4
    rule_ids = {f.rule_id for f in res.findings}
    assert "SEC-001" in rule_ids  # eval
    assert "SEC-003" in rule_ids  # pickle
    assert "SEC-005" in rule_ids  # os.system
    assert "SEC-012" in rule_ids  # SQL Injection
