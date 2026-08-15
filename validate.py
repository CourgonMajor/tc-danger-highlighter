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

print(f"Categories: {len(database)}")
print(f"Total phrases: {total_phrases}")
if errors:
    print(f"\n{len(errors)} problem(s) found:")
    for e in errors:
        print(" -", e)
else:
    print("\nAll good — no structural or casing issues found.")
