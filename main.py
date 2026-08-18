import os
import re
import patterns
import pprint

debug = False
# pprint.pprint(patterns.database) this will print the entire database in a pretty format

# Inputing the filename, only used in testing
print("Enter the filename")
filename = input().strip()


with open(f"data/sample_policies/{filename}", "rt") as f:
    file = f.read()
found = False

#This code adjusts the threshold for a match depending on the number of keywords in the pattern
def get_threshold(num_keywords):
    if num_keywords <= 5:
        return num_keywords / 2
    else:
        return num_keywords / 4

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
#Splitting into windows
window = ""
windows = []

matches = 0
findings = []
count = 0
for i in range(0,len(splited) - 1):
    window = splited[i] + " " + splited[i+1]
    windows.append(window)
tracker = set()
#Matching algorithm
for window in windows:
    for category, data in patterns.database.items():
        for pattern in data['phrases']:
            matches = 0
            for keyword in pattern['keywords']:
                if keyword.lower() in window.lower():
                    matches += 1
            threshold = get_threshold(len(pattern['keywords']))
            if matches > threshold:
                if pattern['phrase'] not in tracker:
                    if debug: 
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
            # if matches > 0: debug code to see how many keywords matched for each pattern
            #     print(f"  [debug] {matches}/{len(pattern['keywords'])} in {category} - {pattern['phrase'][:50]}")

#Final report
for clause in findings:
    print(f"[{clause['danger'].upper()}] {clause['source']}- {clause['category']} ")
    print(f"The meaning: {clause['meaning']}")
#Score calculation
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
if debug:
    print(os.getcwd())
    print(f"windows: {len(windows)}")
    if matches > 0:
        print(f"  [debug] {matches}/{len(pattern['keywords'])} in {category} - {pattern['phrase'][:50]}")