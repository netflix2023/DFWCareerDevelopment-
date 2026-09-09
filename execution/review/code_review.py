"""
Automated Code Quality & Security Reviewer (CodeRabbit / Copilot Style).
Performs static AST analysis, credential leak detection, and pipeline integrity checks
across all execution/ Python modules.
"""

import os
import ast
import re
from typing import List, Dict, Any


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
EXECUTION_DIR = os.path.join(ROOT_DIR, "execution")
LOG_PATH = os.path.join(ROOT_DIR, ".tmp", "code_review.log")


SUSPICIOUS_PATTERNS = [
    (r"AIzaSy[A-Za-z0-9_-]{33}", "Google Gemini API Key"),
    (r"sk-[A-Za-z0-9]{32,}", "OpenAI/Anthropic/OpenRouter API Key"),
    (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
    (r"re_[A-Za-z0-9]{32,}", "Resend API Key"),
    (r"tdp-swe-2027|123/ml-expert", "Synthetic Placeholder URL"),
]


def review_file(file_path: str) -> Dict[str, Any]:
    """Inspects a single Python file for code quality, security, and type safety."""
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    issues = []
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()
        lines = content.splitlines()

    # 1. Security & Canary C Credential Scan
    if not file_path.endswith("code_review.py"):
        for pattern, desc in SUSPICIOUS_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                issues.append({
                    "severity": "CRITICAL",
                    "rule": "Security / Leak Guard",
                    "message": f"Detected potential hardcoded secret or synthetic placeholder: {desc}."
                })


    # 2. AST Syntax & Structure Parsing
    try:
        tree = ast.parse(content, filename=file_path)
    except SyntaxError as e:
        return {
            "file": rel_path,
            "status": "FAILED",
            "issues": [{"severity": "BLOCKER", "rule": "SyntaxError", "message": f"Syntax error at line {e.lineno}: {e.msg}"}]
        }

    # 3. Code Standards & Deep Module Checks
    func_count = 0
    typed_func_count = 0
    docstring_count = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_count += 1
            if node.returns is not None:
                typed_func_count += 1
            if ast.get_docstring(node):
                docstring_count += 1

    if func_count > 0:
        type_coverage = (typed_func_count / func_count) * 100
        if type_coverage < 60:
            issues.append({
                "severity": "WARNING",
                "rule": "Type Hinting Coverage",
                "message": f"Low type hint coverage ({type_coverage:.0f}%). Add return annotations to public functions."
            })

    return {
        "file": rel_path,
        "total_lines": len(lines),
        "total_functions": func_count,
        "typed_functions": typed_func_count,
        "issues": issues,
        "status": "PASSED" if not any(i["severity"] in ("CRITICAL", "BLOCKER") for i in issues) else "FAILED"
    }


def run_code_review() -> str:
    """Runs automated static analysis over all Python modules in execution/."""
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    report_lines = []
    report_lines.append("# Code Review Audit Report (CodeRabbit Style)\n")
    report_lines.append(f"> **Target Directory**: `execution/`  \n> **Status**: Running static AST & security verification...\n\n---\n")

    total_files = 0
    passed_files = 0
    failed_files = 0

    for root, _, files in os.walk(EXECUTION_DIR):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(root, file)
                total_files += 1
                result = review_file(file_path)
                
                badge = "[PASS]" if result["status"] == "PASSED" else "[FAIL]"
                report_lines.append(f"### {badge} `{result['file']}` ({result['total_lines']} lines)")
                
                if result["issues"]:
                    for issue in result["issues"]:
                        report_lines.append(f"- **[{issue['severity']}]** {issue['rule']}: {issue['message']}")
                else:
                    report_lines.append("- *All static quality, AST, and credential guards passed cleanly.*")
                report_lines.append("")

                if result["status"] == "PASSED":
                    passed_files += 1
                else:
                    failed_files += 1

    report_lines.append("---\n")
    report_lines.append(f"**Summary**: {total_files} files analyzed. **{passed_files} Passed**, **{failed_files} Failed**.\n")
    
    report_text = "\n".join(report_lines)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(report_text)
    return report_text


if __name__ == "__main__":
    run_code_review()
