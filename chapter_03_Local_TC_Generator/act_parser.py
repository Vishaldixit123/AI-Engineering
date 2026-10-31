"""Parse EtQ .act test scripts into structured test cases."""

import re

TC_HEADER_RE = re.compile(r"^#\s*(TC_[A-Za-z0-9_.]+)\s*:\s*(.*)$")
PRECONDITION_RE = re.compile(r"^#\s*Precondition\(s?\)\s*:", re.IGNORECASE)
EXPECTED_RE = re.compile(r"^#\s*Expected\s+Result\(s?\)\s*:", re.IGNORECASE)
COMMAND_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\s|$)")
SEPARATOR_RE = re.compile(r"^#\s*[#\s-]*$")
BULLET_RE = re.compile(r"^(?:[-*]|\d+[.)])\s+(.*)$")


def _clean(text: str) -> str:
    """Collapse any run of whitespace to a single space."""
    return re.sub(r"\s+", " ", text).strip()


def parse_act(text: str) -> list[dict]:
    """Convert .act script text into a list of test case rows.

    Each row has: test_id, source_id, description, preconditions,
    steps, expected_result, actual_result.
    """
    cases = []
    current = None
    section = None  # "preconditions" | "expected" | None
    saw_command = False

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue

        header = TC_HEADER_RE.match(line)
        if header:
            if current is not None:
                cases.append(current)
            current = {
                "source_id": header.group(1),
                "description": _clean(header.group(2)),
                "preconditions": [],
                "steps": [],
                "expected_result": [],
            }
            section = None
            saw_command = False
            continue

        if current is None:
            continue  # skip global setup before the first TC block

        if line.startswith("#"):
            if SEPARATOR_RE.match(line):
                continue
            comment = line[1:].strip()
            if not comment:
                continue
            if PRECONDITION_RE.match(line):
                section = "preconditions"
                continue
            if EXPECTED_RE.match(line):
                section = "expected"
                continue
            if section == "preconditions":
                bullet = BULLET_RE.match(comment)
                if bullet:
                    current[section].append(_clean(bullet.group(1)))
                elif current[section]:
                    current[section][-1] = f"{current[section][-1]} {_clean(comment)}"
                else:
                    current[section].append(_clean(comment))
                continue
            if section == "expected":
                bullet = BULLET_RE.match(comment)
                target = current["expected_result"]
                if bullet:
                    target.append(_clean(bullet.group(1)))
                elif target:
                    target[-1] = f"{target[-1]} {_clean(comment)}"
                else:
                    target.append(_clean(comment))
                continue
            # Description continuation lines directly under the TC header.
            if not saw_command and current["description"]:
                current["description"] = f"{current['description']} {_clean(comment)}"
            continue

        if COMMAND_RE.match(line):
            section = None
            saw_command = True
            current["steps"].append(_clean(line))

    if current is not None:
        cases.append(current)

    rows = []
    for index, case in enumerate(cases, start=1):
        rows.append({
            "test_id": f"TC-{index:03d}",
            "source_id": case["source_id"],
            "description": case["description"] or "Not specified",
            "preconditions": case["preconditions"] or ["Not specified"],
            "steps": case["steps"] or ["Not specified"],
            "expected_result": case["expected_result"] or ["Not specified"],
            "actual_result": "",
        })
    return rows


def render_table(rows: list[dict]) -> str:
    """Render test case rows as a markdown table with the expected pattern."""
    lines = [
        "| Test ID | Description | Pre-conditions | Steps | Expected Result | actual result |",
        "|---|---|---|---|---|---|",
    ]
    for row in rows:
        pre = "<br>".join(f"{i}. {item}" for i, item in enumerate(row["preconditions"], 1))
        steps = "<br>".join(f"{i}. {item}" for i, item in enumerate(row["steps"], 1))
        expected = "<br>".join(f"{i}. {item}" for i, item in enumerate(row["expected_result"], 1))
        cells = [row["test_id"], row["description"], pre, steps, expected, row["actual_result"]]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
