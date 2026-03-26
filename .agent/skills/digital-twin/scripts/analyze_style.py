"""
analyze_style.py — Automatic code style analysis for digital twin generation.

WHY: We want to extract patterns from existing code without relying solely
on self-reported preferences. Real code never lies about habits.

Usage:
    python analyze_style.py <directory> [--output report.json]
    python analyze_style.py ./src --output /tmp/style_report.json
"""

import ast
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path


SUPPORTED_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx"}


def analyze_directory(root_dir: str) -> dict:
    """Walk a directory and aggregate style metrics across all source files."""
    root = Path(root_dir)
    if not root.exists():
        raise FileNotFoundError(f"Directory not found: {root_dir}")

    all_files = [
        p for p in root.rglob("*")
        if p.suffix in SUPPORTED_EXTENSIONS
        and "node_modules" not in p.parts
        and ".git" not in p.parts
        and "__pycache__" not in p.parts
    ]

    if not all_files:
        raise ValueError(f"No supported source files found in: {root_dir}")

    file_reports = []
    for file_path in all_files:
        try:
            report = analyze_file(file_path)
            if report:
                file_reports.append(report)
        except Exception as exc:
            print(f"  [SKIP] {file_path.name}: {exc}", file=sys.stderr)

    return aggregate_reports(file_reports, total_files=len(all_files))


def analyze_file(file_path: Path) -> dict | None:
    """Extract style metrics from a single source file."""
    try:
        source = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None

    lines = source.splitlines()
    if not lines:
        return None

    return {
        "path": str(file_path),
        "extension": file_path.suffix,
        "total_lines": len(lines),
        "blank_lines": sum(1 for l in lines if not l.strip()),
        "comment_lines": count_comment_lines(lines, file_path.suffix),
        "max_line_length": max((len(l) for l in lines), default=0),
        "naming": extract_naming_patterns(source, file_path.suffix),
        "function_lengths": extract_function_lengths(source, file_path.suffix),
        "error_handling": extract_error_handling(source, file_path.suffix),
        "uses_early_return": detect_early_return(source),
        "uses_type_hints": detect_type_hints(source, file_path.suffix),
        "uses_ternary": bool(re.search(r"\?\s*\S+\s*:", source)),
        "import_count": len(re.findall(r"^(?:import|from|require)", source, re.MULTILINE)),
    }


def count_comment_lines(lines: list[str], ext: str) -> int:
    """Count lines that are purely comments (not inline)."""
    count = 0
    for line in lines:
        stripped = line.strip()
        if ext == ".py" and stripped.startswith("#"):
            count += 1
        elif ext in {".ts", ".tsx", ".js", ".jsx"} and (
            stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*")
        ):
            count += 1
    return count


def extract_naming_patterns(source: str, ext: str) -> dict:
    """Detect predominant naming style (snake_case vs camelCase vs PascalCase)."""
    identifiers = re.findall(r"\b([a-zA-Z_][a-zA-Z0-9_]{2,})\b", source)
    snake = sum(1 for i in identifiers if "_" in i and i == i.lower())
    camel = sum(1 for i in identifiers if re.match(r"^[a-z][a-zA-Z0-9]+$", i) and any(c.isupper() for c in i))
    pascal = sum(1 for i in identifiers if re.match(r"^[A-Z][a-zA-Z0-9]+$", i))
    total = snake + camel + pascal or 1
    return {
        "snake_case_pct": round(snake / total * 100),
        "camel_case_pct": round(camel / total * 100),
        "pascal_case_pct": round(pascal / total * 100),
        "dominant": max([("snake_case", snake), ("camelCase", camel), ("PascalCase", pascal)], key=lambda x: x[1])[0],
    }


def extract_function_lengths(source: str, ext: str) -> dict:
    """Estimate function lengths — works for Python (AST) and JS/TS (heuristic)."""
    lengths = []

    if ext == ".py":
        try:
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    length = (node.end_lineno or node.lineno) - node.lineno + 1
                    lengths.append(length)
        except SyntaxError:
            pass
    else:
        # WHY: JS/TS parsing with regex is imperfect but avoids a heavy dep like @babel/parser
        fn_starts = [m.start() for m in re.finditer(r"\bfunction\b|=>\s*{|(?:async\s+)?\(.*?\)\s*{", source)]
        lines = source.splitlines()
        for pos in fn_starts:
            line_num = source[:pos].count("\n")
            depth = 0
            end_line = line_num
            for i, line in enumerate(lines[line_num:], start=line_num):
                depth += line.count("{") - line.count("}")
                if i > line_num and depth <= 0:
                    end_line = i
                    break
            lengths.append(end_line - line_num + 1)

    if not lengths:
        return {"count": 0, "avg_lines": 0, "max_lines": 0, "short_pct": 0, "long_pct": 0}

    avg = sum(lengths) / len(lengths)
    return {
        "count": len(lengths),
        "avg_lines": round(avg, 1),
        "max_lines": max(lengths),
        "short_pct": round(sum(1 for l in lengths if l <= 15) / len(lengths) * 100),
        "long_pct": round(sum(1 for l in lengths if l > 40) / len(lengths) * 100),
    }


def extract_error_handling(source: str, ext: str) -> dict:
    """Count error handling patterns to understand defensive vs fail-fast style."""
    if ext == ".py":
        return {
            "try_count": len(re.findall(r"\btry\b\s*:", source)),
            "bare_except": len(re.findall(r"\bexcept\s*:", source)),
            "typed_except": len(re.findall(r"\bexcept\s+\w", source)),
            "raise_count": len(re.findall(r"\braise\b", source)),
        }
    else:
        return {
            "try_count": len(re.findall(r"\btry\s*{", source)),
            "catch_count": len(re.findall(r"\bcatch\s*\(", source)),
            "throw_count": len(re.findall(r"\bthrow\b", source)),
            "promise_catch": len(re.findall(r"\.catch\(", source)),
        }


def detect_early_return(source: str) -> bool:
    """Check if the codebase uses early return / guard clause patterns."""
    guard_patterns = [
        r"if\s*\(.*\)\s*{\s*\n?\s*return",  # JS guard
        r"if\s+.*:\s*\n\s+return",           # Python guard
        r"if\s*\(!",                          # negation guard
    ]
    return any(re.search(p, source) for p in guard_patterns)


def detect_type_hints(source: str, ext: str) -> bool:
    """Check if file uses type annotations."""
    if ext == ".py":
        return bool(re.search(r"def \w+\(.*:.*\)\s*->", source) or re.search(r":\s*(str|int|float|bool|list|dict)\b", source))
    elif ext in {".ts", ".tsx"}:
        return True  # WHY: TypeScript files inherently use types
    return False


def aggregate_reports(reports: list[dict], total_files: int) -> dict:
    """Merge per-file metrics into a global coding style fingerprint."""
    if not reports:
        return {}

    fn_avg_pool = [r["function_lengths"]["avg_lines"] for r in reports if r["function_lengths"]["count"] > 0]
    fn_max_pool = [r["function_lengths"]["max_lines"] for r in reports if r["function_lengths"]["count"] > 0]
    short_pct_pool = [r["function_lengths"]["short_pct"] for r in reports if r["function_lengths"]["count"] > 0]

    dominant_naming = Counter(r["naming"]["dominant"] for r in reports).most_common(1)[0][0]
    total_lines_all = sum(r["total_lines"] for r in reports)
    total_comments = sum(r["comment_lines"] for r in reports)
    total_blanks = sum(r["blank_lines"] for r in reports)

    error_keys = set()
    for r in reports:
        error_keys.update(r["error_handling"].keys())
    error_totals = {k: sum(r["error_handling"].get(k, 0) for r in reports) for k in error_keys}

    return {
        "meta": {
            "analyzed_files": len(reports),
            "total_files_found": total_files,
            "extensions": Counter(r["extension"] for r in reports),
        },
        "code_density": {
            "total_lines": total_lines_all,
            "comment_ratio_pct": round(total_comments / total_lines_all * 100, 1) if total_lines_all else 0,
            "blank_ratio_pct": round(total_blanks / total_lines_all * 100, 1) if total_lines_all else 0,
        },
        "naming": {
            "dominant_style": dominant_naming,
            "breakdown": {
                "snake_case_pct": round(sum(r["naming"]["snake_case_pct"] for r in reports) / len(reports)),
                "camel_case_pct": round(sum(r["naming"]["camel_case_pct"] for r in reports) / len(reports)),
                "pascal_case_pct": round(sum(r["naming"]["pascal_case_pct"] for r in reports) / len(reports)),
            },
        },
        "functions": {
            "avg_length_lines": round(sum(fn_avg_pool) / len(fn_avg_pool), 1) if fn_avg_pool else 0,
            "max_length_lines": max(fn_max_pool) if fn_max_pool else 0,
            "short_functions_pct": round(sum(short_pct_pool) / len(short_pct_pool)) if short_pct_pool else 0,
        },
        "patterns": {
            "early_return_usage_pct": round(sum(1 for r in reports if r["uses_early_return"]) / len(reports) * 100),
            "type_hints_usage_pct": round(sum(1 for r in reports if r["uses_type_hints"]) / len(reports) * 100),
            "ternary_usage_pct": round(sum(1 for r in reports if r["uses_ternary"]) / len(reports) * 100),
        },
        "error_handling": error_totals,
    }


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze code style for digital twin generation")
    parser.add_argument("directory", help="Directory to analyze")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    try:
        print(f"Analyzing {args.directory}...", file=sys.stderr)
        report = analyze_directory(args.directory)
        output = json.dumps(report, indent=2, default=str)

        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"Report saved to {args.output}", file=sys.stderr)
        else:
            print(output)

    except (FileNotFoundError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
