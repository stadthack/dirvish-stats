from json.encoder import JSONEncoder
import re


class Filetree:

    # name = ''
    # size = 0
    # childs = {}
    pattern = re.compile(r'^(.+?)(/.*)$', flags=re.UNICODE)

    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.childs = {}


    def append(self, name, size):
        print name
        self.size = self.size + size
        rname = name.replace(self.name, "", 1)
        rname = rname.lstrip("/")
        match = self.pattern.match(rname)
        if match:
            if not match.group(1) in self.childs:
                if (self.name == '/'):
                    self.childs[match.group(1)] = Filetree(self.name + match.group(1), 0)
                else:
                    self.childs[match.group(1)] = Filetree(self.name + "/" + match.group(1), 0)
            self.childs[match.group(1)].append(name, size)
            print match.group(1)

    def __unicode__(self):
        return self.name + "(" + self.size + ")"

class FiletreeEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Filetree):
            return { 'name': o.name, 'size': o.size, 'childs': o.childs}
        return JSONEncoder.default(self, o)