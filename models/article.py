from database.setup import get_db_connection
CONN = get_db_connection()
CURSOR = CONN.cursor()

class Article:
    all = {}

    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        type(self).all[self.id] = self

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, int):
            self._id = value
        else:
            raise TypeError("id must be of type int")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise TypeError("Title must be of type str")
        if not (2 <= len(value) <= 256):
            raise ValueError("Title must be between 2 and 256 characters")
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError("Content must be of type str")
        if len(value) == 0:
            raise ValueError("Content must be longer than 0 characters")
        self._content = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if isinstance(value, int):
            self._author_id = value
        else:
            raise TypeError("author_id must be of type int")

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if isinstance(value, int):
            self._magazine_id = value
        else:
            raise TypeError("magazine_id must be of type int")

    def save(self):
        sql = """
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        if hasattr(self, '_id'):
            sql = """
                UPDATE articles
                SET title = ?, content = ?, author_id = ?, magazine_id = ?
                WHERE id = ?
            """
            CURSOR.execute(sql, (self.title, self.content, self.author_id, self.magazine_id, self.id))
            CONN.commit()

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        article = cls(title=title, content=content, author_id=author_id, magazine_id=magazine_id)
        article.save()
        return article

    @property
    def author(self):
        from models.author import Author  
        sql = """
            SELECT id, name
            FROM authors
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.author_id,))
        author_data = CURSOR.fetchone()
        return Author(*author_data) if author_data else None

    @property
    def magazine(self):
        from models.magazine import Magazine  
        sql = """
            SELECT id, name, category
            FROM magazines
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.magazine_id,))
        magazine_data = CURSOR.fetchone()
        return Magazine(*magazine_data) if magazine_data else None