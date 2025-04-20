import re

# Basic patterns often found in SQL injection attempts, fulfilling the assignment's requirement for a basic check.
# NOTE: This pattern matching is illustrative and does not guarantee protection against all SQL injection vulnerabilities.
# For production-level security, parameterized queries (prepared statements) are the standard practice that can be used.

UNSANITIZED_PATTERNS = [
    r"['\";]",              
    r"(?i)\s*(--|\#|\/\*).*", 
    r"(?i)\b(UNION|SELECT|INSERT|UPDATE|DELETE|DROP|EXEC|ALTER|CREATE|TRUNCATE)\b", 
    # Add more complex patterns if required
]

COMPILED_PATTERNS = [re.compile(pattern) for pattern in UNSANITIZED_PATTERNS]

def is_potentially_unsanitized(input_string: str) -> bool:
    # This performs a basic check for SQL injection queries and returns True if a potentially unsanitized pattern is found, False otherwise.
    if not isinstance(input_string, str):
        return True # or raise typeerror

    for pattern in COMPILED_PATTERNS:
        if pattern.search(input_string):
            return True
    return False