from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Tool
from . import db

tool = Blueprint('tool', __name__)

@tool.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            flash('Name is required!')
        else:
            tool = Tool.query.filter_by(name=name).first() # if this returns a tool, then the name already exists in database

            if tool: # if a tool is found, we want to redirect back to create page
                flash('Tool with same name already exists')
                return redirect(url_for('tool.create'))

            # create a new tool with the form data
            new_tool = Tool(name=name, description=description)

            # add the new user to the database
            db.session.add(new_tool)
            db.session.commit()

    return render_template('create.html')
