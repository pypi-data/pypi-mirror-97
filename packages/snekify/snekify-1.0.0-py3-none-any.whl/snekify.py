"""Convert text to snake case"""
import fileinput
import re


def main() -> None:
    """Snekify CLI interface"""
    snekified_lines: list[str] = []
    for line in fileinput.input():
        snekified_lines.append(snekify(line))
    print('\n'.join(snekified_lines))


def snekify(line: str) -> str:
    """Snekify text"""
    words = re.findall(r'[A-Za-z0-9]+', line)
    return '_'.join(word.lower() for word in words)
