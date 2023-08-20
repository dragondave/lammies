import csv
from jinja2 import Environment, FileSystemLoader

templates_dir = "templates"
env = Environment(loader=FileSystemLoader(templates_dir))
lammy_template = env.get_template('one_lammy.html')
page_template = env.get_template('page.html')

class Config:
    def __init__(self, printrun):
        self.printrun = printrun

config=Config("micro")

class Page:
    def __init__(self):
        self.lammies = []

    def render(self):
        return page_template.render(lammies=self.lammies, printrun=config.printrun)

    def from_csv(self, filename):
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile) # TODO: replace
            for row in reader:
                for key, value in row.items():
                    # this is a hack
                    if value == "None":
                        row[key] = None
                if row['ref'] and row['printrun'] == config.printrun:
                    for i in range(0, int(row['printcount'])):
                        self.lammies.append(Lammy(row))
                    print(row)
        return self
    
    def restructure(self, items=8):
        if items == 8:
            front = [1,2,3,4,5,6,7,8]
            back = [2,1,4,3,6,5,8,7]
        
        




class Lammy:
    def __init__(self, lammydict):
        self.lammydict = {
            'ref': lammydict['ref'],
            'fronttext': lammydict['fronttext'],
            'frontflavour': lammydict.get('frontflavour', None),
            'roleplaying': lammydict.get("roleplaying", None),
            'mechanical': lammydict.get("mechanical", None),
            'religious': lammydict.get("religious", None),
            'relicon': lammydict.get("relicon", None),
            'printrun': lammydict.get("printrun", None),
        }

    def __repr__(self):
        return f"[{self.lammydict['ref']}: {self.lammydict['fronttext']}]"

    def render(self):
        return lammy_template.render(**self.lammydict)


page = Page().from_csv("data/bigsheet.csv")
with open("output.html", "wb") as f:
    f.write(page.render().encode('utf-8'))