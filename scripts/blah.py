import json

container = []

with open('asdf.txt', 'r') as fo:
    data = fo.read().split('\n')

for thing in data:
    container.append(
        {
            'username' : thing
        }
    )

with open('out.JSON', 'w') as fo:
    fo.write(json.dumps(container, indent=4))