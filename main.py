#This code is used to analyze a privacy policy and identify potential risks based on a predefined set of patterns. 
# It reads a policy text file, splits it into windows of sentences, and checks for matches against the patterns defined in the `patterns` module. 
# The findings are then reported along with a score indicating the level of risk.
import os
import re
import patterns
# import pprint
debug = False
#This list contains pairs of American and British English variants for certain keywords. 
VARIANT_PAIRS = [
    ("analyz", "analys"),
    ("monetiz", "monetis"),
    ("anonymiz", "anonymis"),
    ("pseudonymiz", "pseudonymis"),
    ("organiz", "organis"),
    ("personaliz", "personalis"),
    ("customiz", "customis"),
    ("utiliz", "utilis"),
    ("recogniz", "recognis"),
    ("categoriz", "categoris"),
    ("authoriz", "authoris"),
    ("minimiz", "minimis"),
    ("maximiz", "maximis"),
    ("optimiz", "optimis"),
    ("summariz", "summaris"),
    ("sanitiz", "sanitis"),
    ("normaliz", "normalis"),
    ("generaliz", "generalis"),
    ("standardiz", "standardis"),
    ("centraliz", "centralis"),
    ("synchroniz", "synchronis"),
    ("characteriz", "characteris"),
    ("finaliz", "finalis"),
    ("apologiz", "apologis"),
    ("criticiz", "criticis"),
    ("behaviour", "behavior"),
    ("favour", "favor"),
    ("honour", "honor"),
    ("labour", "labor"),
    ("licenc", "licens"),
    ("defenc", "defens"),
    ("offenc", "offens"),
    ("centre", "center"),
    ("catalogue", "catalog"),
    ("dialogue", "dialog"),
    ("programme", "program"),
    ("acknowledgement", "acknowledgment"),
    ("enquir", "inquir"),
]

#This function generates all possible forms of a given keyword by replacing American English variants with their British English counterparts and vice versa. 
def get_keyword_forms(keyword):
    forms = {keyword}
    for american, british in VARIANT_PAIRS:
        if american in keyword:
            forms.add(keyword.replace(american, british))
        elif british in keyword:
            forms.add(keyword.replace(british, american))
    return list(forms)
#This function expands the keywords in the patterns database by generating all possible forms for each keyword using the `get_keyword_forms` function. 
#It updates the patterns database with the new keyword forms.
def expand_keywords(): #This should be only called once, else it will crash as it cannot convert the list of lists to a list of lists of lists.
    for category, data in patterns.database.items():
        for pattern in data['phrases']:
            new_keywords = []
            for keyword in pattern['keywords']:
                new_keywords.append(get_keyword_forms(keyword))
            pattern['keywords'] = new_keywords
expand_keywords()

#This function calculates the threshold for matching keywords based on the number of keywords in a pattern. 
def get_threshold(num_keywords):
    if num_keywords <= 5: #This only counts as 1 match if there are 5 or fewer keywords in the pattern.
        return num_keywords / 2
    else:                  #This only counts as 1 match if there are more than 5 keywords in the pattern.
        return num_keywords / 4

print("Enter the filename")
while True:
    try:
        filename = input().strip().lower()
        with open(f"data/sample_policies/{filename}", "rt") as f:
            policy_text = f.read()
        break
    except FileNotFoundError:
        print(f"File not found: {filename}")
    
splited = re.split(r'(?<=[.!?])\s+', policy_text)

windows = []
findings = []
count = 0
for i in range(0,len(splited) - 1):
    window = splited[i] + " " + splited[i+1]
    windows.append(window)
tracker = set()

#The main loop iterates through each window of text and checks for matches against the patterns in the database. 
# If a match is found, it records the finding and increments the count.
for window in windows:
    lower_window = window.lower()
    for category, data in patterns.database.items():
        for pattern in data['phrases']:
            matches = 0 #Reset matches for each pattern
            for group in pattern['keywords']:
                #This only counts it as 1 match if any of the forms in the group are found in the window.
                for form in group:
                    if form.lower() in lower_window:
                        matches += 1
                        break
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

#The following loop iterates through the findings and prints out the details of each finding, including the danger level, source, category, and meaning. 
# The danger level is displayed in uppercase for emphasis.
for clause in findings:
    print(f"[{clause['danger'].upper()}] {clause['source']}- {clause['category']} ")
    print(f"The meaning: {clause['meaning']}")
#The scoring system assigns points based on the danger level of each finding. 
#The total score is capped at a maximum of 10 points as a way to quantify the overall risk level of the privacy policy.
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
    # pprint.pprint(patterns.database) this will print the entire database in a pretty format
    print(os.getcwd())
    print(f"windows: {len(windows)}")