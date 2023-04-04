# @name: search.py
# @creation_date: 2023-04-04
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Search route for search results
# @acknowledgements:
# https://medium.com/@joseortizcosta/search-utility-with-flask-and-mysql-60bb8ee83dad

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Resource
from sqlalchemy import or_

search = Blueprint('search', __name__)

#endpoint for search
@search.route('/search', methods=['GET'])
def basic_search():
    if request.args.get('query') is not None:
        query = request.args.get('query')
        results = Resource.query.filter(
            or_(
                Resource.name.ilike('%' + query + '%'),
                Resource.description.ilike('%' + query + '%'),
                Resource.developer.ilike('%' + query + '%'),
                Resource.longDescription.ilike('%' + query + '%'),
                Resource.experimental.ilike('%' + query + '%'),
                Resource.considerations.ilike('%' + query + '%'),
                Resource.references.ilike('%' + query + '%'),
                Resource.author.ilike('%' + query + '%'),
                Resource.isbn.ilike('%' + query + '%'),
                Resource.typology.ilike('%' + query + '%'),
            )).all()
        return render_template('search.html', results=results)
    else:
        return redirect(url_for('main.index'))