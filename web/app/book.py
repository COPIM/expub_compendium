# @name: book.py
# @creation_date: 2021-11-03
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: book route for book-related functions and pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Resource
from werkzeug.exceptions import abort
from . import db

book = Blueprint('book', __name__)

# function to retrieve data about a single book from the database
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        abort(404)
    return book

# route for displaying all books in database
@book.route('/books')
def get_books():
    books = Book.query
    return render_template('books.html', books=books)

# route for displaying a single book based on the ID in the database
@book.route('/books/<int:book_id>')
def show_book(book_id):
    book = get_book(book_id)
    return render_template('book.html', book=book)

# route for editing a single book based on the ID in the database
@book.route('/books/<int:book_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_book(book_id):
    book = get_book(book_id)

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']

        if not name:
            flash('Name is required!')
        else:
            book = Book.query.get(book_id)
            book.name = name
            book.description = description
            db.session.commit()
            return redirect(url_for('book.get_books'))

    return render_template('edit.html', book=book)

# route for function to delete a single book from the edit page
@book.route('/books/<int:book_id>/delete', methods=('POST',))
@login_required
def delete_book(book_id):
    book = get_book(book_id)
    deletion = Book.query.get(book_id)
    db.session.delete(deletion)
    db.session.commit()
    flash('Successfully deleted!')
    return redirect(url_for('book.get_books'))
