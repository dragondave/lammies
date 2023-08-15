import csv
from jinja2 import Environment, FileSystemLoader

templates_dir = "templates"
env = Environment(loader=FileSystemLoader(templates_dir))
lammy_template = env.get_template('one_lammy.html')


class Lammy:
    def __init__(self, lammydict):
        self.lammydict = {
            'ref': lammydict['ref'],
            'fronttext': lammydict['fronttext'],
            'roleplaying': lammydict.get("roleplaying", None),
            'mechanical': lammydict.get("mechanical", None),
            'religious': lammydict.get("religious", None),
        }

    def __repr__(self):
        return f"[{self.lammydict['ref']}: {self.lammydict['fronttext']}]"

    def render(self):
        return lammy_template.render(**self.lammydict)



def one_csv(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield Lammy(row)


marks = list(one_csv('data/marks.csv'))

print (marks[0].render())
