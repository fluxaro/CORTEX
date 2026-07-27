"""Tests for Go static analyzer."""

from app.analyzers.go.go_analyzer import GoAnalyzer


def test_go_analyzer_parse() -> None:
    """Test analyzing Go source code."""
    code = """
package main

import (
    "fmt"
    "net/http"
)

type Server struct {
    Port int
}

func (s *Server) Start() error {
    if s.Port == 0 {
        return fmt.Errorf("invalid port")
    }
    return nil
}

func unexportedHelper(msg string) {
    fmt.Println(msg)
}
"""
    analyzer = GoAnalyzer()
    res = analyzer.analyze_file("main.go", code, file_size=len(code))

    assert res.language == "Go"
    assert res.class_count == 1
    assert res.classes[0].name == "Server"
    assert res.function_count == 2
    assert "fmt" in res.imports

    pub_fn = next(f for f in res.functions if f.name == "Start")
    assert pub_fn.visibility == "public"
    assert pub_fn.class_name == "Server"

    priv_fn = next(f for f in res.functions if f.name == "unexportedHelper")
    assert priv_fn.visibility == "private"
