from .app import db
from flask_login import UserMixin

class Author(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self ):
        return self.name


class Book(db.Model):
    __tablename__ = "book"
    
    id = db.Column(db.Integer , primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    img = db.Column(db.String(100))
    author_id = db.Column(db.Integer , db.ForeignKey("author.id"))
    
    author = db.relationship("Author",backref=db.backref("books", lazy="dynamic"))
    estAdore = db.relationship("Favorites", back_populates="favBook")
    genrelivre = db.relationship("GenreBook",back_populates="livres")

    def __repr__(self ):
        return self.title
    
class Genre(db.Model):
    nom = db.Column(db.String(100) , primary_key =True)
    genrelivre = db.relationship("GenreBook",back_populates="genres")

    def __repr__(self ):
        return self.title
    
class GenreBook(db.Model):
    nom = db.Column(db.String(100) , db.ForeignKey("genre.nom"), primary_key =True)
    id = db.Column(db.Integer , db.ForeignKey("book.id") , primary_key =True)
    livres = db.relationship("Book",back_populates="genrelivre")
    genres = db.relationship("Genre",back_populates="genrelivre")

    def __repr__(self ):
        return self.title

class User(db.Model,UserMixin):
    
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    
    adore = db.relationship("Favorites", back_populates="userFav")

    def __repr__(self):
        return self.username
    
    def get_id(self):
        return self.username

class Favorites(db.Model):
    __tablename__ = "favorite"
    
    user = db.Column(db.String(50), db.ForeignKey("user.username"), primary_key=True)
    userFav = db.relationship("User", back_populates="adore")
    
    id = db.Column(db.Integer , db.ForeignKey("book.id"), primary_key=True)
    favBook = db.relationship("Book", back_populates="estAdore")
        
    def __repr__(self):
        return f"{self.user} {self.id}"

def new_fav(user, id):
    favorite = Favorites(user=user, id=id)
    db.session.add(favorite)
    db.session.commit()

def retirer_fav(user, id):
    fav = Favorites.query.get({"user": user, "id": id})
    if fav:
        db.session.delete(fav)
        db.session.commit()

def is_fav(user, id):
    return Favorites.query.get({"user": user, "id": id}) is not None

def get_favs(user):
    favs = Favorites.query.filter_by(user=user).all()
    books = [fav.favBook for fav in favs]
    return books
    
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