from .app import db
from flask_login import UserMixin

class Author(db.Model):
    __tablename__ = "AUTHOR"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self ):
        return self.name


class Book(db.Model):
    __tablename__ = "BOOK"
    
    id = db.Column(db.Integer , primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
    
    author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))
    estAdore = db.relationship("Favorite", back_populates="favBook")
    

    def __repr__(self ):
        return self.title

class User(db.Model,UserMixin):
    __tablename__ = "USER"
    
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    
    adore = db.relationship("Favorite", back_populates="userFav")

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self.username

class Favorites(db.Model):
    __tablename__ = "FAVORITE"
    
    user = db.Column(db.String(50), db.ForeignKey("USER.username"), primary_key=True)
    userFav = db.relationship("User", back_populates="adore")
    
    id = db.Column(db.Integer , db.ForeignKey("BOOK.id"), primary_key =True)
    favBook = db.relationship("Book", back_populates="estAdore")
    
    def __init__(self, user="", id=0):
        self.user = user
        self.id = id
        
    def __repr__(self):
        return self.user + str(self.id)
    
def new_fav():
    session = db.Session(engine)
	
	bur = Article( 1, "burger", 69.5)
	session.add( bur )
	esclave = Article(2, "esclave", 1)
	Elysee = Article( 3, "Elysee", 240)
	asp = Article( 4, "aspirateur dyson", 49.99)
	
	session.add_all( [esclave, Elysee, asp ] )
	session.commit()
    
def retire_fav():
    
def get_favs():
    
def get_sample():
    return Book.query.limit(10).all()

def get_all_author():
    return Author.query.all()

def get_all_books():
    return Book.query.all()

def get_book_by_id(id:int):
    return Book.query.get_or_404(id)

def get_author_by_id(id:int):
    return Author.query.get_or_404(id)

def get_books_by_author(id:int):
    return Author.query.get_or_404(id).books.all()

def get_user_by_username(username:str):
    return User.query.get_or_404(username)

from .app import login_manager
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)