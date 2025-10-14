import json
from pathlib import Path
from typing import Tuple
import frontmatter
from jsonschema import Draft202012Validator, FormatChecker

import sys


def check_submission_md(path_to_submission_md: str) -> Tuple[int, str]:
    submission_frontmatter = frontmatter.load(path_to_submission_md)
    current_dir = Path(__file__).parent
    with open(current_dir / "submission-md-schema.json") as schema_open:
        submission_schema = json.load(schema_open)
    validator = Draft202012Validator(submission_schema, format_checker=FormatChecker())

    errors = sorted(
        validator.iter_errors(submission_frontmatter.metadata), key=lambda e: e.path
    )

    if errors:
        header = "`submission.md` validation failed with the following issues:\n"
        lines = []
        for error in errors:
            path = ".".join(str(p) for p in error.path) or "<root>"
            lines.append(f"- `{path}`: {error.message}")
        message = header + "\n".join(lines) + "\n"
        return 1, message

    return 0, "`submission.md` validation passed"


if __name__ == "__main__":
    code, message = check_submission_md(sys.argv[1])
    print(message)
    raise SystemExit(code)
