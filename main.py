import os
import re
import patterns
import pprint


print(os.getcwd())
with open("data/sample_policies/crunchyroll.txt", "rt") as f:
    file = f.read()
found = False

#Old matching code, kept for reference
# for category, data in patterns.database.items():
#     for pattern in data["phrases"]:
#         words = pattern["phrase"].split()
#         escaped_words = [re.escape(w) for w in words]
#         flexible_pattern = r"\W*".join(escaped_words)
#         if re.search(flexible_pattern, file, re.IGNORECASE):
#             values = {
#                 "category": category,
#                 "source": pattern["source"],
#                 "meaning": pattern["meaning"],
#                 "danger": pattern["danger"],
#             }
#             count += 1
#             findings.append(values)


splited = re.split(r'(?<=[.!?])\s+', file)

window = ""
windows = []

matches = 0
findings = []
count = 0
for i in range(0,len(splited) - 1):
    window = splited[i] + " " + splited[i+1]
    windows.append(window)
tracker = set()
for window in windows:
    for category, data in patterns.database.items():
        for pattern in data['phrases']:
            matches = 0
            for keyword in pattern['keywords']:
                if keyword.lower() in window.lower():
                    matches += 1
            if matches > len(pattern['keywords']) / 2:
                if pattern['phrase'] not in tracker:
                    print(f"matches: {matches}, in {category} - {pattern['phrase']}")
                    print(f"  Found in policy: {window}")
                    tracker.add(pattern['phrase'])
                    values = {
                        "category": category,
                        "source": pattern["source"],
                        "meaning": pattern["meaning"],
                        "danger": pattern["danger"],
                    }
                    count += 1
                    findings.append(values)
print(f"windows: {len(windows)}")

score = 0
for i in findings:
    if i['danger'] == "high":
        score += 3
    elif i['danger'] == "medium":
        score += 2
    elif i['danger'] == "low":
        score += 1
score = min(score, 10)
print(f"Total findings: {count}, Score: {score}/10")
# pprint.pprint(patterns.database) this will print the entire database in a pretty format
