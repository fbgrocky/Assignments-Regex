
import re
from typing import Iterable, List, Set

def extract_emails_excluding(text: str, exclude_domains: Iterable[str]) -> List[str]:

    excluded: Set[str] = {d.strip().lower() for d in exclude_domains if d.strip()}
    # Build domain alternation for negative lookahead after the '@'
    alt = "|".join(re.escape(d) for d in sorted(excluded))
    if alt:
        # Negative lookahead to block the exact domain(s) immediately after '@'
        # Example: ...(?!exclude\.com\b)....
        pattern = rf"\b[A-Za-z0-9._%+-]+@(?!(?:{alt})\b)[A-Za-z0-9.-]+\.[A-Za-z]{{2,}}\b"
    else:
        # No exclusions -> generic email pattern
        pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"

    regex = re.compile(pattern, re.IGNORECASE)
    return regex.findall(text)

def main():
    text = "Emails: user1@domain.com, user2@exclude.com, user3@domain.com, user4@sub.exclude.com"
    print("Original text:")
    print(text, "\n")

    # Exclude only 'exclude.com' (exact match). 'sub.exclude.com' is allowed.
    result = extract_emails_excluding(text, ["exclude.com"])
    print("Extracted (excluding 'exclude.com'):")
    print(result, "\n")  # Expected: ['user1@domain.com', 'user3@domain.com', 'user4@sub.exclude.com']

    # Exclude multiple domains
    result_multi = extract_emails_excluding(text, ["exclude.com", "domain.com"])
    print("Extracted (excluding 'exclude.com' and 'domain.com'):")
    print(result_multi)  # Expected: ['user4@sub.exclude.com']

if __name__ == "__main__":
    main()
