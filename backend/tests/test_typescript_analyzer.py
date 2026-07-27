"""Tests for TypeScript static analyzer."""

from app.analyzers.typescript.typescript_analyzer import TypeScriptAnalyzer


def test_typescript_analyzer_parse() -> None:
    """Test analyzing TypeScript source code."""
    code = """
import React from 'react';
import { useState } from 'react';

export interface User {
    id: string;
}

export class UserService extends BaseService {
    getUser(): User {
        return { id: '1' };
    }
}

export function calculateTotal(items: number[]): number {
    if (items.length === 0) return 0;
    return items.reduce((a, b) => a + b, 0);
}

export const helper = (x: number) => x * 2;
"""
    analyzer = TypeScriptAnalyzer()
    res = analyzer.analyze_file("src/service.ts", code, file_size=len(code))

    assert res.language == "TypeScript"
    assert res.function_count >= 2
    assert res.class_count >= 1
    assert res.classes[0].name == "UserService"
    assert "react" in res.imports
