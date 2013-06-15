import re
import gzip
from dirvishVault import DirvishVault
from dirvishDb import DirvishDb
import os

MASTER_CONFIG=u'/etc/dirvish/master.conf'
# TODO read from master.conf
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

def updateDb(vaults, db):
    pattern = re.compile(r'^\s*(\d+)\s+\d+\s+([A-Za-z-]+)\s+\d+\s+.+?\s+.+?\s+(\d*)\s*[A-Za-z]+\s+\d+\s+[0-9:]+\s+(/.+)$', flags=re.UNICODE)
    for vault in vaults:
        #print vault.__unicode__() #+ " " + vault.maxAge().isoformat()
        for image in vault.images:
            print "-> " + image.__unicode__() #+ " " + str(image.date.isoformat())

            db_image = db.imageExists(vault.name, image.date)
            if not db_image:
                db_image = db.createImage(vault.name, image.date)
            else:
                continue

            if not os.path.exists(image.indexFile()):
                #print "skipping... empty backup"
                continue
            index = gzip.open(image.indexFile())

            for line in index:
                match = pattern.match(line)
                if match:
                    inode = match.group(1)
                    size = match.group(3)
                    name = match.group(4)
                    type = None
                    attr = match.group(2)[0]
                    if (attr == '-'):
                        type = 0
                    elif (attr == 'd'):
                        type = 1
                    elif (attr == 'l'):
                        type = 2
                    elif (attr == 's'):
                        type = 3
                    elif (attr == 'p'):
                        type = 4
                    elif (attr == 'c'):
                        type = 5
                    elif (attr == 'b'):
                        type = 6
                    else:
                        print "Unknown file type : " + match.group(2)[0]
                        exit()
                    db_file = db.fileExists(inode, size, name)
                    if not db_file:
                        db_file = db.createFile(inode, size, name, type)
                    else:
                        db_file = db_file[0]

                    db.createLink(db_file, db_image)
                else:
                    print "Fatal index line doesn't match: '" + line + "'"
                    exit()
            db.flushLinks()
            db.conn.commit()

vaults = parseVaults()
db = DirvishDb()
updateDb(vaults,db)


