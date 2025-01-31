One of the key deliverables for Work Package 6 of the COPIM project is "an online resource detailing opportunities for experimental book publishing". We've decided to put this together in the form of an online compendium with details of software, practices, examples, and sensitivities that can be used for experimental publishing.

The Experimental Publishing Compendium will build on this review of tools to present a resource for any researcher, artist, or publisher looking to try experimental publishing. This compendium includes not only software tools that can be used to do experimental publishing but practices of experimental publishing and examples of experimental publications.

## application structure

The Experimental Publishing Compendium is a Python application using the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework to render as a website and to provide functions around user authentication and login as well as retrieving data from the underlying database. The Flask framework uses a few HTML template pages to render different pages efficiently based on routes defined in Python files. 

The database is a MariaDB SQL database with a basic structure of Resources, Relationships, and Users. Resources are divided into tools, practices, and books and the table contains fields for these various types of resources. Relationships defines the links between resources using the resource ID in the Resource table: these are rendered on the site as connections between, say, a tool and a practice. Users contains the site's users with basic details like email address and hashed password. This simple structure provides flexibility for displaying resources with filters and to illustrate the connections between various resources. 

### admin interface

There's an admin interface for editing resources and relationships in the browser. To login with a user account that has been previously set up, go to ./login and enter your email address and password. 

Once logged in, you can access the page to add a new resource at ./create. Select using the dropdown whether you want to create a tool, a practice, or a book. At the bottom of the form, you will be able to add relationships between your new resource and other resources: to select multiple resources to create relationships with, hold Ctrl on your keyboard while selecting options in the selection list.

You can also use the 'edit' link which will appear next to every resource to edit an existing resource, add new relationships between existing resources, and delete an existing resource.

Logged in users can log out at ./logout.

### RESTful API

The application has a simple RESTful API deployed using [Marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html) to define schemas based on the SQLAlchemy database models. It allows a simple JSON export of users (login required), tools, practices, and books.

The API is relatively open and is available at ./api 

## deployment instructions

### environment files

To deploy this environment, first copy env.template to a new file, env.dev. Fill in the appropriate environment variables.

### Docker Compose

In the command line, navigate to the directory where this repository is stored on your local machine and run:

`docker-compose up -d --build`

Docker should build the application environment comprising a Python container running Flask and a database container running MariaDB.

The website should then be available in the browser at 'localhost:5000'.

To take down the environment, run:

`docker-compose down`

### populating the database

To intially create the database and a database user:

`docker-compose exec -it db mariadb -u root -p`

Enter your root password as defined in .env.dev.

`CREATE DATABASE compendium;`
`CREATE USER 'flask'@'%' IDENTIFIED BY '[PASSWORD]';`
`GRANT CREATE, INSERT, UPDATE, SELECT, DELETE ON compendium.* TO 'flask'@'%';`

Restart the containers to allow Flask to build the database tables:

`docker-compose down`
`docker-compose up -d --build`

You can then use database_functions.sh and an SQL file to populate the database e.g.

`./database_functions -i ./db_imports/compendium_db_20230112.sql`

## database functions 

This repository contains a shell script to perform various database functions including importing a whole database from SQL file, exporting the database in SQL, exporting individual tables as tab-delimited txt file, and importing individual tables from tab-delimited txt file. 

Run `./database_functions -h` to see the instructions for this script. 

### legacy database instructions:

The following is no longer required in Flask-SQLAlchemy 3. See https://stackoverflow.com/questions/73968584/flask-sqlalchemy-db-create-all-got-an-unexpected-keyword-argument-app

To build the database tables run:

`docker exec -it python python`
`from app import db, create_app, models`
`db.create_all(app=create_app())`

## credits

Content in the Experimental Publishing Compendium is © 2022–2025 [COPIM](https://copim.ac.uk) and licensed under a [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Book cover data is from the [Open Library Covers API](https://openlibrary.org/dev/docs/api/covers).

The Experimental Publishing Compendium's source code is available at [https://github.com/COPIM/expub_compendium](https://github.com/COPIM/expub_compendium) and is licensed under the [MIT License](https://github.com/COPIM/expub_compendium/blob/main/LICENSE).

The Experimental Publishing Compendium was developed by [Simon Bowie](https://simonxix.com) and designed by [Joel Galvez](https://www.joelgalvez.com/) and Martina Vanini.