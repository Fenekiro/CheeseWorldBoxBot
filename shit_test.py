import ujson

with open("app/researches.json", "r", encoding="utf-8") as file:
    researches = ujson.loads(file.read())

for r in researches:
    print(r)
