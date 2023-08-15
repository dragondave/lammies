import csv
from jinja2 import Environment, FileSystemLoader

templates_dir = "templates"
env = Environment(loader=FileSystemLoader(templates_dir))
lammy_template = env.get_template('one_lammy.html')
page_template = env.get_template('page.html')

class Page:
    def __init__(self):
        self.lammies = []

    def render(self):
        return page_template.render(lammies=self.lammies)

    def from_csv(self, filename):
        with open(filename, "r") as csvfile:
            reader = csv.DictReader(csvfile) # TODO: replace
            for row in reader:
                for key, value in row.items():
                    # this is a hack
                    if value == "None":
                        row[key] = None
                if row['ref']:
                    for i in range(0, int(row['printcount'])):
                        self.lammies.append(Lammy(row))
                    print(row)
        return self



class Lammy:
    def __init__(self, lammydict):
        self.lammydict = {
            'ref': lammydict['ref'],
            'fronttext': lammydict['fronttext'],
            'frontflavour': lammydict.get('frontflavour', None),
            'roleplaying': lammydict.get("roleplaying", None),
            'mechanical': lammydict.get("mechanical", None),
            'religious': lammydict.get("religious", None),
        }

    def __repr__(self):
        return f"[{self.lammydict['ref']}: {self.lammydict['fronttext']}]"

    def render(self):
        return lammy_template.render(**self.lammydict)


page = Page().from_csv("data/bigsheet.csv")
with open("output.html", "wb") as f:
    f.write(page.render().encode('utf-8'))