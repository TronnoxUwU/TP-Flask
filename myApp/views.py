from .app import app, db
from .models import *
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, SubmitField, FloatField
from wtforms.validators import DataRequired, Optional
from wtforms import PasswordField
from hashlib import sha256
from flask_login import login_user, current_user, logout_user
from flask import request


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class AuthorForm(FlaskForm):
    id = HiddenField ("id")
    name = StringField("Nom",validators =[DataRequired()])
    
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class AdvancedSearchForm(FlaskForm):
    name_auth = StringField('Nom de l\'auteur', validators=[Optional()])
    name_book = StringField('Nom du livre', validators=[Optional()])
    max_price = FloatField('Prix maximum', validators=[Optional()])
    submit = SubmitField('Search')

@app.route("/login/", methods=("GET","POST",))
def login():
    print("login")
    f = LoginForm()
    if f.validate_on_submit():
        print("Post")
        user = f.get_authenticated_user()
        print(user)
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
        "login.html",
        form=f
    )

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/")
def home():
    f = SearchForm()
    if f.validate_on_submit():
        return redirect(url_for('search_books', srch=f.search.data))
    return render_template(
        "home.html",
        title="My Books !",
        books=get_sample(),
        form=f
        )

@app.route("/detail/<id>")
def detail(id):
    f = SearchForm()
    return render_template(
        "detail.html",
        book=get_book_by_id(int(id)),
        form=f)

@app.route("/author/<id>")
def one_author(id):
    return render_template(
        "author.html",
        author=get_author_by_id(int(id)),
        books = get_books_by_author(int(id)))

@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author_by_id(id)
    f = AuthorForm(id=a.id, name=a.name)
    return render_template (
        "edit-author.html",
        author=a, form=f)
    
@app.route("/search", methods=['GET'])
def search_books():
    f = SearchForm()
    srch = request.args.get('srch', '')
    if srch:
        books = livres_par_deb_titre(srch)
        return render_template(
            "home.html",
            title="Résultats de recherche pour : "+srch,
            books=books,
            form=f
        )
    return redirect(url_for('home'))

def livres_par_deb_titre(srch) -> list:
    book_src = []
    for book in get_all_books():
        if srch.lower() in book.title.lower():
            book_src.append(book)
    return book_src

@app.route("/advanced_search", methods=['GET', 'POST'])
def advanced_search():
    f = AdvancedSearchForm()  # Instancie le formulaire

    if f.validate_on_submit():  # Si le formulaire est soumis et valide
        # Récupération des données du formulaire
        name_auth = f.name_auth.data
        name_book = f.name_book.data
        max_price = f.max_price.data
        print(name_auth + " - " + name_book + " - " + str(max_price))

        # Fonction de filtrage des livres
        def filter_books(name_auth, name_book, max_price):
            books = get_all_books()
            filtered_books = []
            for book in books:
                if ((not name_auth or name_auth.lower() in book.author.name.lower()) and
                    (not name_book or name_book.lower() in book.title.lower()) and
                    (not max_price or book.price <= max_price)):
                    filtered_books.append(book)
            return filtered_books

        # Filtrer les livres en fonction des critères
        books = filter_books(name_auth, name_book, max_price)

        # Renvoyer les résultats à la page home.html avec les livres filtrés
        return render_template(
            "home.html",
            title="Résultats de la recherche avancée",
            books=books,
            form=f
        )
    
    # Si la méthode est GET (affichage initial), on renvoie juste le formulaire
    return render_template("search.html", form=f)



@app.route("/save/author/", methods =("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = get_author_by_id(int(f.id.data))
        a.name = f.name.data
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    a = get_author_by_id(int(f.id.data))
    return render_template("edit-author.html", author=a, form=f)
# add,author

@app.route("/add/author/")
def add_author():
    f = AuthorForm(id=None, name="")
    return render_template (
        "add-author.html",
        form=f)

@app.route("/add/save/author/", methods =("POST",))
def save_new_author(new=False):
    print(new)
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
        a = Author(name=f.name.data)
        db.session.add(a)
        db.session.commit()
        return redirect(url_for("one_author", id=a.id))
    return render_template("edit-author.html", author=a, form=f)

# @app.route("/save/author/", methods =("POST",))
# def save_author():
#     a = None
#     f = AuthorForm()
#     if f.validate_on_submit():
#         a = get_author_by_id(int(f.id.data))
#         a.name = f.name.data
#         db.session.commit()
#         return redirect(url_for("one_author", id=a.id))
#     a = get_author_by_id(int(f.id.data))
#     return render_template (
#         "edit-author.html",
#         author=a, form=f)
