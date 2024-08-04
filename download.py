import requests
import csv
import io
import requests_cache
# requests_cache.install_cache()

tabs = [
        {'gid': 461547648, 'name': 'marks', 'printrun': 'large', 'print': 
            {"printcount": "Print Count", "ref": "Reference Number", "fronttext": "Front Text", "roleplaying": "Roleplaying Effect",
         "religious": "Religious Alignment"}
        },
        {'gid': 657279460, 'name': 'flange', 'printrun': 'large', 'print': 
         {"printcount": "Print Count", "ref": "Reference Number", "fronttext": "Name", "frontflavour": "Front Text", "mechanical": "Back Text"}
         },
        {'gid': 923420315, 'name': 'talismans', 'printrun': 'large', 'print': 
         {"printcount": "Print Count", "ref": "Reference Number", "fronttext": "Name", "frontflavour": "Front Text", "mechanical": "Back Text"}
        },
        {'gid': 1592624607, 'name': 'foxx_talismans', 'printrun': 'large', 'print':
         {"printcount": "Print Count", "ref": "Reference Number", "fronttext": "Name",  "frontflavour": "Front Text", "mechanical": "Back Text"}
        },
        {'gid': 1243514760, 'name': 'common_resources', 'printrun': 'micro', 'print':
         {"printcount": "Print Count", "ref": "Reference Number", "fronttext": "Front Text", "mechanical": "Back Text"}
        },
        ]

# printcount,,ref,fronttext,frontflavour,roleplaying,mechanical,religious,relicon,printrun,,,,


for tab in tabs:
    print (tab['name'])
    URL = f"https://docs.google.com/spreadsheets/d/1x8xfYGf5PQqbj-2RSEMw95U5n8lCJBWgvJ5Q_IIzZCw/export?format=csv&gid={tab['gid']}"
    response = requests.get(URL)
    response.raise_for_status()
    with open(f"data/{tab['name']}.csv", 'wb') as f:
        f.write(response.content)
    header = response.content.decode('utf-8').split('\n')[0].strip().split(',')
    rest = response.content.partition(b'\n')[2]
    print(header)
    for new, old in tab['print'].items():
        pos = header.index(old)
        header[pos] = new
    with open(f"data/{tab['name']}-modified.csv", "wb") as f:
        f.write(','.join(header).encode('utf-8'))
        f.write(b'\n')
        f.write(rest)
    print(header)