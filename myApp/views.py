from .app import app, db
from .models import *
from flask import render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField, SubmitField, FloatField
from wtforms.validators import DataRequired, Optional
from wtforms import PasswordField
from hashlib import sha256
from flask_login import login_user, current_user, logout_user, login_required
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
    
class BookForm(FlaskForm):
    id = HiddenField ("id")
    price = StringField("Prix",validators =[DataRequired()])
    title = StringField("Titre",validators =[DataRequired()])
    url = StringField("Url",validators =[DataRequired()])
    img = StringField("Image",validators =[DataRequired()])
    author_id = StringField("Id de l'auteur",validators =[DataRequired()])

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

class IdForm(FlaskForm):
    id = StringField("Id",validators =[DataRequired()])

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
        form=f,
        is_fav=is_fav(current_user.username, id)
        )

@app.route("/edit/book/<int:id>")
@login_required
def edit_book(id):
    b = get_book_by_id(id)
    f = BookForm(id=b.id, price=b.price, title=b.title, url=b.url, img=b.img, author_id=b.author_id )
    return render_template(
        "edit-book.html", book=b, form=f)

@app.route("/delete/book/")
@login_required
def delete_book():
    f = IdForm(id=None)
    return render_template(
        "delete-book.html", form=f)

@app.route("/delete/save/book/", methods =("POST",))
def save_delete_book():
    f = IdForm()
    print(int(f.id.data),f.validate_on_submit())
    if f.validate_on_submit():
        b = get_book_by_id(int(f.id.data))
        db.session.delete(b)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template(
        "delete-book.html", form=f)

@app.route("/delete/author/")
@login_required
def delete_author():
    f = IdForm(id=None)
    return render_template(
        "delete-author.html", form=f)

@app.route("/delete/save/author/", methods =("POST",))
def save_delete_author():
    f = IdForm()
    print(int(f.id.data),f.validate_on_submit())
    if f.validate_on_submit():
        a = get_author_by_id(int(f.id.data))
        db.session.delete(a)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template(
        "delete-book.html", form=f)

@app.route("/save/book/", methods =("POST",))
def save_book():
    b = None
    f = BookForm()
    if f.validate_on_submit():
        b = get_book_by_id(int(f.id.data))
        b.price = f.price.data
        b.title = f.title.data
        b.url = f.url.data
        b.img = f.img.data
        b.author_id = f.author_id.data
        db.session.commit()
        return redirect(url_for("detail", id=b.id))
    b = get_book_by_id(int(f.id.data))
    return render_template("edit-book.html", author=b, form=f)


@app.route("/author/<id>")
def one_author(id):
    return render_template(
        "author.html",
        author=get_author_by_id(int(id)),
        books = get_books_by_author(int(id)))

@app.route("/edit/author/<int:id>")
@login_required
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
    f = AdvancedSearchForm()

    if f.validate_on_submit():
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

        books = filter_books(name_auth, name_book, max_price)

        return render_template(
            "home.html",
            title="Résultats de la recherche avancée",
            books=books,
            form=f
        )
    
    return render_template("search.html", form=f)

@app.route("/add_fav/<int:book_id>")  #ça marche
def add_fav(book_id):
    if not is_fav(current_user.username, book_id):
        new_fav(current_user.username, book_id)
        db.session.commit()
    return redirect(url_for('detail', id=book_id))

@app.route("/retire_fav/<int:book_id>")  #ça marche aussi tkt
def retire_fav(book_id):
    if is_fav(current_user.username, book_id):
        retirer_fav(current_user.username, book_id)
        db.session.commit()
    return redirect(url_for('detail', id=book_id))

@app.route('/user_favorites')
def user_favorites():
    user = current_user.username
    favorite_books = get_favs(user)
    return render_template('favorites.html', books=favorite_books, title="Mes Livres Favoris")


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
@login_required
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
