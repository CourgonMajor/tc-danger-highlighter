from patterns import database

REQUIRED_KEYS = {"phrase", "danger", "keywords", "source", "meaning"}
VALID_DANGER = {"high", "medium", "low"}

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
        for keyword in keywords:
            if not keyword.strip():
                errors.append(f"[{category}][{entry.get('source') or i}] keyword '{keyword}' is empty or whitespace")
            if keyword != keyword.strip():
                errors.append(f"[{category}][{entry.get('source') or i}] keyword '{keyword}' has leading/trailing whitespace")

print(f"Categories: {len(database)}")
print(f"Total phrases: {total_phrases}")
if errors:
    print(f"\n{len(errors)} problem(s) found:")
    for e in errors:
        print(" -", e)
else:
    print("\nAll good — no structural or casing issues found.")
