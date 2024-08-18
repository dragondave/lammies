import funcy
import csv
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

templates_dir = "templates"
env = Environment(loader=FileSystemLoader(templates_dir))
lammy_template = env.get_template('one_lammy.html')
doc_template = env.get_template('doc.html')
spreads_template = env.get_template('spreads.html')
front_template = env.get_template('one_lammy_front.html')
back_template = env.get_template('one_lammy_back.html')
GAME = "🪦 Grave of the Eternal Fire 🪦"
MICROGAME = "Grave of the Eternal Fire"

def _clean_string(s):
    bold = "CLEAVE FLAME IDENTIFY MUTE STAGGER VENOM WEAKEN COMMAND RESIST REFRESH WOUNDED HEAL MASS DETECT IMPALE IMMUNE"
    replacements = {'""': '"', "\n": "<br>"}
    for b in bold.split(' '):
        replacements[b] = f"<b>{b}</b>"
    if not s:
        return s
    for old, new in replacements.items():
        s=s.replace(old, new)
    return s


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

def as_int(s):
    if not s:
        return 0
    else:
        return int(s)

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
                if row['ref']:
                    for i in range(0, as_int(row['printcount'])):
                        self.lammies.append(Lammy(row))
                    print(row)
        return self

    def render_spreads(self, items_per_page=8):
        padded_lammies = list(self.lammies)
        # there should be items-per-page - 1 placeholders
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        padded_lammies.append(PLACEHOLDER_LAMMY)
        pages = len(padded_lammies) // items_per_page
        padded_lammies = padded_lammies[:pages*items_per_page]
        # TODO: fix if not full set of eight.
        # TODO: handle non-8 case.
        assert items_per_page == 8
        back = [4,5,6,7,0,1,2,3]
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
                'frontflavour': _clean_string(lammydict.get('frontflavour', None)),
                'roleplaying':  _clean_string(lammydict.get("roleplaying", None)),
                'mechanical': _clean_string(lammydict.get("mechanical", None)),
                'religious': _clean_string(lammydict.get("religious", None)),
                'relicon': lammydict.get("relicon", None),
                'printrun': _clean_string(lammydict.get("printrun", None)),
                'game': GAME,
                'microgame': MICROGAME,
                'printrun': config.printrun,
            }

    def __repr__(self):
        return f"[{self.lammydict['ref']}: {self.lammydict['fronttext']}]"

    def render(self):
        return lammy_template.render(**self.lammydict)

    def front_render(self):
        return front_template.render(**self.lammydict)

    def back_render(self):
        return back_template.render(**self.lammydict)


def make_pdf(html):
    """Generate a PDF file from a string of HTML."""
    htmldoc = HTML(string=html)
    return htmldoc.write_pdf()


config=Config("micro")
PLACEHOLDER_LAMMY = Lammy({'ref': '', 'fronttext': '', 'printrun':config.printrun})

for csv_name in ["common_resources"]:
    doc = Doc().from_csv(f"data/{csv_name}-modified.csv")
    html = doc.render()
    with open(f"output/{csv_name}.html", "wb") as f:
        f.write(html.encode('utf-8'))
    # with open(f"output/{csv_name}.pdf", "wb") as f:
    #     f.write(make_pdf(html))

config=Config("norm")
PLACEHOLDER_LAMMY = Lammy({'ref': '', 'fronttext': '', 'printrun':config.printrun})

for csv_name in ["flange", "foxx_talismans", "talismans", "marks", "blessings"]:
    doc = Doc().from_csv(f"data/{csv_name}-modified.csv")
    html = doc.render()
    with open(f"output/{csv_name}.html", "wb") as f:
        f.write(doc.render_spreads().encode('utf-8'))
    # with open(f"output/{csv_name}.pdf", "wb") as f:
    #     f.write(make_pdf(html))
