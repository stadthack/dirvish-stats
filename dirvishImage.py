import datetime
import os


class DirvishImage:

    path = None
    vault = None
    date = None

    def __init__(self, vault, folder, path):
        self.folder = path
        self.vault = vault
        self.date = datetime.datetime.strptime(folder, '%Y%m%d%H%M')

    def indexFile(self):
        return os.path.join(self.folder, "index.gz")

    def __unicode__(self):
        return self.folder
