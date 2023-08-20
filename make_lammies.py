import funcy
import csv
from jinja2 import Environment, FileSystemLoader

templates_dir = "templates"
env = Environment(loader=FileSystemLoader(templates_dir))
lammy_template = env.get_template('one_lammy.html')
doc_template = env.get_template('doc.html')
spreads_template = env.get_template('spreads.html')
front_template = env.get_template('one_lammy_front.html')
back_template = env.get_template('one_lammy_back.html')

class Spread:
    pass

class Config:
    def __init__(self, printrun):
        self.printrun = printrun
        if printrun == "norm":
            self.restructure = 8
        else:
            self.restructure = None

config=Config("norm")

class Doc:
    def __init__(self):
        self.lammies = []

    def render(self):
        return doc_template.render(lammies=self.lammies, printrun=config.printrun)

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
    
    def render_spreads(self, items_per_page=8):
        padded_lammies = list(self.lammies)
        padded_lammies.append(padded_lammies[0])
        # TODO: fix if not full set of eight.
        # TODO: handle non-8 case.
        assert items_per_page == 8
        back = [1,0,3,2,5,4,7,6]
        spreads = []
        
        for chunk in funcy.chunks(items_per_page, padded_lammies):
            print (chunk)
            front_page_order = chunk
            back_page_order = [chunk[x] for x in back]
            spread = Spread()
            spread.front = front_page_order
            spread.back = back_page_order
            spreads.append(spread)
        return spreads_template.render(spreads=spreads, printrun=config.printrun)

class Lammy:
    def __init__(self, lammydict):
        if lammydict == None:
            self.lammydict = {}
        else:
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
    
    def front_render(self):
        return front_template.render(**self.lammydict)
    
    def back_render(self):
        return back_template.render(**self.lammydict)


doc = Doc().from_csv("data/bigsheet.csv")
with open("output.html", "wb") as f:
    f.write(doc.render().encode('utf-8'))
with open("output_spread.html", "wb") as f:
    f.write(doc.render_spreads().encode('utf-8'))