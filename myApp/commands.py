import click
from .app import app , db

@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Creates the tables and populates them with data."""

    # création de toutes les tables
    db.create_all()

    # chargement de notre jeu de données
    import yaml
    books = yaml.safe_load(open(filename))

    # import des modèles
    from .models import Author, Book

    # première passe: création de tous les auteurs
    authors = {}
    for b in books:
        a = b["author"]
        if a not in authors:
            o = Author(name=a)
            db.session.add(o)
            authors[a] = o
    db.session.commit()

    # deuxième passe: création de tous les livres
    for b in books:
        a = authors[b["author"]]
        o = Book(price=b["price"],
                 title=b["title"],
                 url=b["url"],
                 img=b["img"],
                 author_id=a.id)
        db.session.add(o)
    db.session.commit()

@app.cli.command()
def syncdb():
    """Creates all missing tables."""
    db.create_all()

@app.cli.command ()
@click.argument("username")
@click.argument("password")
def newuser(username , password ):
    """Adds a new user."""
    from .models import User
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = User(username=username , password=m.hexdigest())
    db.session.add(u)
    db.session.commit()

@app.cli.command ()
@click.argument("username")
@click.argument("password")
def passwd(username, password):
    """Change password of a user."""
    from .models import get_user_by_username
    from hashlib import sha256
    m = sha256()
    m.update(password.encode())
    u = get_user_by_username(username)
    u.password = password
    db.session.commit()

@app.cli.command ()
@click.argument("nom_genre")
def newgenre(nom_genre ):

    """Create a new category."""
    from .models import Genre
    g = Genre(nom=nom_genre)
    db.session.add(g)
    db.session.commit()

@app.cli.command ()
@click.argument("nom_genre")
@click.argument("id_livre")
def ajoutgenretolivre(nom_genre, id_livre):
    """Add a book to a category."""
    from .models import GenreBook
    g = GenreBook(nom=nom_genre, id=id_livre)
    db.session.add(g)
    db.session.commit()