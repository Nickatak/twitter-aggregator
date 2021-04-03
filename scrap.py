import json

with open('idols.json') as fo:
    data = json.loads(fo.read())

container = []
for thing in data:
    container.append({
        'screen_name' : thing['username']
    })

with open('idols.json', 'w') as fo:
    fo.write(json.dumps(container, indent=4))
