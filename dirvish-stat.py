import re
import gzip
from dirvishVault import DirvishVault
from dirvishDb import DirvishDb

MASTER_CONFIG=u'/etc/dirvish/master.conf'
BANK_DIR=u'/mnt/backup/dirvish/'

def parseVaults():
    vaults = []
    config = open(MASTER_CONFIG, 'r')
    sectionstart = False
    pattern = re.compile('\s+(\S*)\s+\d+:\d+\s*')
    for line in config:
        if line.startswith('Runall:'):
            sectionstart = True
            continue

        if line.startswith('expire-default:'):
            sectionstart = False

        if sectionstart:
            match = pattern.match(line)
            if match:
                vaults.append(DirvishVault(match.group(1), BANK_DIR.__add__(match.group(1))))
    return vaults

def updateDb(vaults):
    for vault in vaults:
        print vault.__unicode__()

vaults = parseVaults()
db = DirvishDb(vaults)

#pattern = re.compile('^(\d+).*(\d+) \S+\d+ \d+ (\S+)$')
# pattern = re.compile(r'^(\d+).*(\d+) \w+ \d+ (?:[0-9:]+) (/.+)$', flags=re.UNICODE)
pattern = re.compile(r'^(\d+).*\s+(\d+)\s+(?:[A-Za-z]+)\s+(?:\d+)\s+(?:[0-9:]+)\s+(/.+)$', flags=re.UNICODE)

for vault in vaults:
     print vault.__unicode__() #+ " " + vault.maxAge().isoformat()
     for image in vault.images:
        print "-> " + image.__unicode__() #+ " " + str(image.date.isoformat())
        index = gzip.open(image.indexFile())
        db_image = db.imageExists(vault.name, image.date)
        if not db_image:
            db_image = db.createImage(vault.name, image.date)
        else:
            db_image = db_image[0]

        for line in index:
            match = pattern.match(line)
            if match:
                inode = match.group(1)
                size = match.group(2)
                name = match.group(3)
                db_file = db.fileExists(inode, size, name)
                if not db_file:
                    db_file = db.createFile(inode, size, name)
                else:
                    db_file = db_file[0]

                db.createLink(db_file, db_image)
            else:
                print "Fatal index line doesn't match: '" + line + "'"
                exit()
