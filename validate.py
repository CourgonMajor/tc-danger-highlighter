import math

from patterns import database

REQUIRED_KEYS = {"phrase", "danger", "keywords", "source", "meaning"}
VALID_DANGER = {"high", "medium", "low"}
#DUPLICATE FUNCTION FROM main.py
def required_matches(num_keywords):
    val = math.ceil(num_keywords * 0.4)
    val = max(val, 2)        
    val = min(val, num_keywords)
    return val

errors = []
total_phrases = 0
for category, data in database.items():
    if "phrases" not in data:
        errors.append(f"[{category}] missing 'phrases' key")
        continue
    for i, entry in enumerate(data["phrases"]):
        total_phrases += 1
        missing = REQUIRED_KEYS - entry.keys()
        if missing:
            errors.append(f"[{category}][{i}] missing keys: {missing}")
        if entry.get("danger") not in VALID_DANGER:
            errors.append(f"[{category}][{i}] bad danger value: {entry.get('danger')!r}")
        if not isinstance(entry.get("keywords"), list):
            errors.append(f"[{category}][{i}] 'keywords' is not a list: {type(entry.get('keywords'))}")
        keywords = entry.get("keywords", [])
        for a in range(len(keywords)):
            for b in range(a + 1,len(keywords)):
                copy1 = keywords[a].lower()
                copy2 = keywords[b].lower()
                if copy1 in copy2 or copy2 in copy1:
                    errors.append(f"[{category}][{entry.get('source') or i}] keywords '{keywords[a]}' and '{keywords[b]}' are too similar")
        counter = 0
        for keyword in keywords:
            if keyword.lower() in entry.get("phrase", "").lower():
                counter += 1
            if not keyword.strip():
                errors.append(f"[{category}][{entry.get('source') or i}] keyword '{keyword}' is empty or whitespace")
            if keyword != keyword.strip():
                errors.append(f"[{category}][{entry.get('source') or i}] keyword '{keyword}' has leading/trailing whitespace")
        if counter < required_matches(len(keywords)):
            errors.append(f"[{category}][{entry.get('source') or i}] is not found in its own phrase, has {counter} out of {len(keywords)} keywords, needs {required_matches(len(keywords))}")
print(f"Categories: {len(database)}")
print(f"Total phrases: {total_phrases}")
if errors:
    for e in errors:
        print(" -", e)
    print(f"\n{len(errors)} problem(s) found")
else:
    print("\nAll good — no structural or casing issues found.")
