# ADR 0001: Architecture Intelligence Engine Static AST Parsing

## Context
Evaluating software architecture often requires dynamic code execution or runtime tracing, which poses severe security risks when analyzing arbitrary GitHub repositories.

## Decision
ProjectIQ implements a pure **Static Application Analysis Engine** utilizing Abstract Syntax Tree (AST) parsing (Python `ast`, Babel/TypeScript AST, tree-sitter) without executing repository code.

## Consequences
- **Security**: Complete isolation against arbitrary code execution.
- **Speed**: Analysis runs in seconds rather than requiring containerized runtime sandboxes.
- **Explainability**: Architectural findings cite exact AST node locations and file lines.
