import re

from flask import current_app
from flask.ext.mongoengine import mongoengine
from flask.ext.script import Manager
from html.parser import HTMLParser
from requests import get

from dofus.model.equipement import Equipement


populate_manager = Manager(usage="Auto populate database")

DOFUS_DOMAIN = "http://www.dofus.com"
equipements = "http://www.dofus.com/fr/mmorpg/encyclopedie/equipements?text=&type_id[0]=1&type_id[1]=9&type_id[2]=11&type_id[3]=82&type_id[4]=17&type_id[5]=10&type_id[6]=16&type_id[7]=23&type_id[8]=81&type_id[9]=151&size=96&page="
equipements_pages = list(range(1, 26))


# class HTMLParser()
# print("url", r.url)
# print("headers", r.headers)
# print("response content", r.text)
# print("content", r.content)

EFFECTS = [
    r"^.* Vitalité$",
    r"^.* Intelligence$",
    r"^.* Agilité$",
    r"^.* Chance$",
    r"^.* Force$",
    r"^.* Puissance$",
    r"^.* Sagesse$",
    r"^.* Critique$",
    r"^.* PA$",
    r"^.* PM$",
    r"^.* Portée$",
    r"^.* Invocations$",
    r"^.* Prospection$",
    r"^.* Fuite$",
    r"^.* Tacle$",
    r"^.* Dommages$",
    r"^.* Dommages Neutre$",
    r"^.* Dommages Feu$",
    r"^.* Dommages Air$",
    r"^.* Dommages Eau$",
    r"^.* Dommages Terre$",
    r"^.* Dommages Critiques$",
    r"^.* Résistance Neutre$",
    r"^.* Résistance Feu$",
    r"^.* Résistance Terre$",
    r"^.* Résistance Eau$",
    r"^.* Résistance Air$",
    r"^.* Résistance Critiques$"
]

class Node():
    def __init__(self):
        self.level = 0
        self.tag = None
        self.attrs = None
        self.data = None
        self.children = []
        self.parent = None

    def __repr__(self):
        ret = ""
        ret += "\t"*self.level+"<"+str(self.tag)+" "+str(self.attrs)+">\n"
        if self.data:
            ret += "\t"*(self.level+1)+str(self.data)+"\n"
        for child in self.children:
            ret += child.__repr__()
        ret += "\t"*(self.level)+"</"+str(self.tag)+">"+"\n"
        return ret


class MyHTMLParserList(HTMLParser):
    def __init__(self, tree = None):
        super().__init__()
        self.tree = tree
        self.current = None
        self.tbody = False

    def handle_starttag(self, tag, attrs):
        if tag != "tbody" and not self.tbody:
            return
        if tag == "tbody":
            self.tbody = True
        node = Node()
        node.tag = tag
        node.attrs = attrs
        if not self.tree:
            self.tree = node
        # print("current", self.current)
        if not self.current:
            self.current = self.tree
        else:
            node.level = self.current.level+1
            node.parent = self.current
            self.current.children.append(node)
        self.current = node
    def handle_endtag(self, tag):
        if tag != "tbody" and not self.tbody:
            return
        if tag == "tbody":
            self.tbody = False
        self.current = self.current.parent
    def handle_data(self, data):
        if not self.tbody:
            return
        if self.current:
            self.current.data = data


class MyHTMLParserEquipPage(HTMLParser):
    def __init__(self, tree = None):
        super().__init__()
        self.tree = tree
        self.current = None
        self.equipement = {}
        # title
        self.title = False
        # image
        self.picture = False
        # type
        self.type = False
        self.type_span = False
        # level
        self.level = False
        # effets
        self.effets = False
        self.effets_level = 0

    def handle_starttag(self, tag, attrs):
        # fix
        if tag == "img" and "title" in list(self.equipement.keys()) and not self.picture:
            src, ref = attrs[0]
            self.equipement["picture"] = ref
            self.picture = True
        if tag == "h1":
            self.title = True
        if self.type and tag == "span":
            self.type_span = True
        node = Node()
        node.tag = tag
        node.attrs = attrs
        if not self.tree:
            self.tree = node
        if not self.current:
            self.current = self.tree
        else:
            node.level = self.current.level+1
            node.parent = self.current
            self.current.children.append(node)
        self.current = node

    def handle_endtag(self, tag):
        if tag == "h1":
            self.title = False
        if self.type_span and tag == "span":
            self.type = False
            self.type_span = False
        self.current = self.current.parent

    def handle_data(self, data):
        if data.strip() == "Effets":
            self.effets = True
            self.effets_level = self.current.level-1
        if self.effets:
            for effect in EFFECTS:
                if re.search(effect, data.strip()):
                    if not "effects" in list(self.equipement.keys()):
                        self.equipement["effects"] = []
                    self.equipement["effects"].append(data.strip())
            if self.current.level < self.effets_level:
                self.effets = False
        if self.type_span:
            self.equipement["type"] = data.strip()
        if data.strip() == "Type":
            self.type = True
        if self.title:
            self.equipement["title"] = data.strip()
        if "Niveau" in data and not self.level:
            un, deux, self.equipement["level"] = data.rpartition(" ")
            self.level = True
        if self.current:
            self.current.data = data


def write_test_file(tree):
    f = open('output.html', 'w')
    f.write(str(tree))
    f.close()


def rescue_href(tree):
    href = []
    for tr in tree.children:
        for td in tr.children:
            if len(td.children):
                span = td.children[0]
                if len(span.children):
                    a = span.children[0]
                    if len(a.attrs):
                        for attr in a.attrs:
                            key, value = attr
                            if key == "href":
                                if not value in href:
                                    href.append(value)
    return href


def rescue_element_page(href):
    dofus_link = DOFUS_DOMAIN+href
    print(DOFUS_DOMAIN+href)
    # check if allready exist
    if Equipement.objects(dofus_link=dofus_link).count():
        return
    # get
    r = get(dofus_link)
    if r.status_code == 200:
        parser = MyHTMLParserEquipPage()
        html = r.text
        parser.feed(html)
        eq = parser.equipement
        effects = {}
        if "effects" in list(eq.keys()):
            for effect in eq["effects"]:
                m = re.match(r"(?P<from>-?\d+)( à (?P<to>-?\d+))?(?P<percent>%?) (?P<carac>.*)", effect)
                if m:
                    _from = m.group('from')
                    _to = m.group('to')
                    _percent = m.group('percent')
                    _carac = m.group('carac')
                    effects[_carac] = {
                        'min': _from,
                        'max': _to if (_to) else _from,
                        'percent': True if (_percent == "%") else False
                    }
        equipement = Equipement(title=eq["title"], level=eq["level"], type=eq["type"],
                                image=eq["picture"], effects=effects, dofus_link=dofus_link)
        try:
            equipement.save()
        except mongoengine.errors.NotUniqueError as e:
            print(e)
    else:
        print("code", r.status_code)


@populate_manager.command
def populate():
    count = 0
    for page in equipements_pages:
        r = get(equipements+str(page))
        if r.status_code == 200:
            parser = MyHTMLParserList()
            html = r.text
            parser.feed(html)
            hrefs = rescue_href(parser.tree)
            for href in hrefs:
                count = count+1
                rescue_element_page(href)
        else:
            print("code", r.status_code)
    print(count)


@populate_manager.command
def drop_database():
    # drop database
    current_app.db.connection.drop_database("dofus")


if __name__ == "__main__":
    populate_manager.run()
