"""Reject unreviewed dependency names, versions, hashes and pip directives."""
import difflib
import re
import sys
from pathlib import Path

candidate = Path(sys.argv[1]).read_text(encoding="utf-8")
approved = Path(sys.argv[2]).read_text(encoding="utf-8")

def canonical(text):
    return "\n".join(line.strip() for line in text.splitlines()
                     if line.strip() and not line.lstrip().startswith("#"))

known = re.findall(r"^([a-zA-Z0-9_-]+)==", approved, re.M)
if canonical(candidate) != canonical(approved):
    print("DEPENDENCY POLICY: FAIL - manifest differs from reviewed baseline")
    for name in re.findall(r"^([a-zA-Z0-9_-]+)==", candidate, re.M):
        if name not in known:
            hint = difflib.get_close_matches(name, known, n=1, cutoff=0.6)
            print(f"Unapproved package: {name}; similar approved package: {hint}")
    sys.exit(1)
print("DEPENDENCY POLICY: PASS - exact reviewed names, versions and hashes")
