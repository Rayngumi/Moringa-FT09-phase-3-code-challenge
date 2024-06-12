from models.__init__ import CURSOR, CONN
from models.author import Author

class Magazine:
    def __init__(self, cursor, id=None,  name=None, category=None):
        self.conn = CONN
        self.cursor = CURSOR
        self._id = None
        self._name = None
        self._category = None
        self.name = name
        self.category = category

    def create_magazines_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                         (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT)''')
        self.conn.commit()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
        self.cursor.execute("INSERT OR REPLACE INTO magazines (name, category) VALUES (?,?)", (value, self.category))
        self.conn.commit()
        self._id = self.cursor.lastrowid

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Category must be a string or None")
        if value is not None and len(value) == 0:
            raise ValueError("Category cannot be empty")
        self._category = value
        self.cursor.execute("INSERT OR REPLACE INTO magazines (name, category) VALUES (?,?)", (self.name, value))
        self.conn.commit()
        self._id = self.cursor.lastrowid

    def __repr__(self):
        return f'<Magazine {self.name}>'
    

    def articles(self):
        self.cursor.execute('''SELECT a.title 
                              FROM magazines 
                              JOIN articles a ON magazines.id = a.magazine_id 
                              WHERE magazines.id =?''', (self.id,))
        results = self.cursor.fetchall()
        return [row[0] for row in results]

    def contributors(self):
        self.cursor.execute('''SELECT a.name 
                              FROM magazines 
                              JOIN articles art ON magazines.id = art.magazine_id 
                              JOIN authors a ON art.author_id = a.id 
                              WHERE magazines.id =?''', (self.id,))
        results = self.cursor.fetchall()
        return [row[0] for row in results]
    
    def article_titles(self):
        self.cursor.execute('''SELECT a.title 
                              FROM magazines 
                              JOIN articles a ON magazines.id = a.magazine_id 
                              WHERE magazines.id =?''', (self.id,))
        results = self.cursor.fetchall()
        if results:
            return [row[0] for row in results]
        return None

    def contributing_authors(self):
        self.cursor.execute('''SELECT a.id, a.name 
                              FROM magazines 
                              JOIN articles art ON magazines.id = art.magazine_id 
                              JOIN authors a ON art.author_id = a.id 
                              WHERE magazines.id =? 
                              GROUP BY a.id, a.name 
                              HAVING COUNT(art.id) > 2''', (self.id,))
        results = self.cursor.fetchall()
        if results:
            authors = []
            for row in results:
                author = Author(id=row[0], name=row[1])
                authors.append(author)
            return authors
        return None