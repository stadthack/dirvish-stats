
import sqlite3

class DirvishDb:

    conn = None
    c = None
    vaults = None
    links = None

    def __init__(self, vaults):
        self.conn = sqlite3.connect('dirvish.db')
        self.c = self.conn.cursor()
        self.vaults = vaults
        self.links = []
        self.createDatabases()

    def createDatabases(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS image (id INTEGER PRIMARY KEY ASC AUTOINCREMENT, name TEXT, time TEXT);''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS file (id INTEGER PRIMARY KEY ASC AUTOINCREMENT, inode INTEGER, size INTEGER, name TEXT);''')
        self.c.execute('''CREATE TABLE IF NOT EXISTS image_file (image_id INTEGER, file_id INTEGER, FOREIGN KEY (image_id) REFERENCES image (id), FOREIGN KEY (file_id) REFERENCES file (id));''')
        self.conn.commit()


    def fileExists(self, inode, size, name):
        self.c.execute('''SELECT * from file WHERE inode=? AND size=? AND name=?;''', (inode, size, name))
        file = self.c.fetchone()
        return file

    def createFile(self, inode, size, name):
        self.c.execute('''INSERT INTO file (inode, size, name) VALUES (?, ?, ?);''', (inode, size, name))
        #self.conn.commit()
        return self.c.lastrowid

    def createLink(self, file_id, image_id):
        self.links.append([image_id, file_id])
        #self.c.execute('''INSERT INTO image_file (image_id, file_id) VALUES (?,?);''', (image_id, file_id))

    def flushLinks(self):
        self.c.executemany('''INSERT INTO image_file (image_id, file_id) VALUES (?,?);''', self.links)
        self.links = []

    def imageExists(self, name, time):
        self.c.execute('''SELECT * FROM image WHERE name = ? AND time = ?;''', (name, time))
        image = self.c.fetchone()
        return image

    def createImage(self, name, time):
        self.c.execute('''INSERT INTO image (name, time) VALUES (?, ?);''', (name, time))
        #self.conn.commit()
        return self.c.lastrowid
