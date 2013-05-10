import os
from datetime import datetime, timedelta
from dirvishImage import DirvishImage


class DirvishVault:
    folder = None
    name = None
    images = None

    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.images = []

        # read images
        dirnames = os.listdir(self.folder)
        dirnames.remove("dirvish")
        for dirname in dirnames:
            # print os.path.join(self.folder, dirname)
            self.images.append(DirvishImage(self.name, dirname, os.path.join(self.folder, dirname)))

    def maxAge(self):
        oldest = None
        for image in self.images:
            if oldest == None:
                oldest = image.date
                continue
            if oldest < image.date:
                oldest = image.date
        return oldest

    def maxAgedImageOlderThan(self, delta):
        now = datetime.now()
        otherdate = now - delta
        return otherdate < self.maxAge()

    def __unicode__(self):
        return self.name