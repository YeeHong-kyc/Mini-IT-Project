import json

data = {
    "Item name": "",
    "Item Description": "",
    "Upload a Photo": ["colour", "brand", "features"]
}

with open("output.json", "w") as json_file:
    json.dump(data, json_file, indent=4)


with open("output.json", "r") as json_file:
    loaded_data = json.load(json_file)
    print("Loaded JSON data:")
    print(loaded_data)