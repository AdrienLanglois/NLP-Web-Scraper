import json
    
def save_json(dict):
    json_object = json.dumps(dict, indent=4)
    
    with open("results/articles.json", "w") as outfile:
        outfile.write(json_object)
    