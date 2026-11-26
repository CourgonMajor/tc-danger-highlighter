from patterns import database
import json
with open("patterns.json", "w") as f:
    json.dump(database, f, indent=2)
