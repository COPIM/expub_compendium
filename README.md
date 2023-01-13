One of the key deliverables for Work Package 6 of the COPIM project is "an online resource detailing opportunities for experimental book publishing". We've decided to put this together in the form of an online toolkit with details of software, practices, examples, and sensitivities that can be used for experimental publishing.

The ExPub Compendium will build on this review of tools to present a resource for a researcher, artist, or publisher looking to try experimental publishing. From our preliminary design discussions, we have plans to include not only software tools that can be used to do experimental publishing but examples of experimental publications, practices of experimental publishing, publishers who have done some form of experimental publishing, and sensitivities involved in experimental publishing.

## Application structure

The ExPub Compendium is a Python application using the [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework to render as a website and to provide functions around user authentication and login as well as retrieving data from the underlying database. The Flask framework uses a few HTML template pages to render different pages efficiently based on routes defined in Python files. These template pages use a fairly basic [Bootstrap 5](https://getbootstrap.com/) grid design which allows for responsive design using in-built CSS and HTML elements. 

The database is a MariaDB SQL database with a basic structure of Resources, Relationships, and Users. Resources are divided into tools, practices, and books and the table contains fields for these various types of resources. Relationships defines the links between resources using the resource ID in the Resource table: these are rendered on the site as connections between, say, a tool and a practice. Users contains the site's users with basic details like email address and hashed password. This simple structure provides flexibility for displaying resources with filters and to illustrate the connections between various resources. 

### to deploy environment

#### environment files

To deploy this environment, first copy env.template to a new file, env.dev. Fill in the appropriate environment variables.

#### Docker Compose

In the command line, navigate to the directory where this repository is stored on your local machine and run:

`docker-compose up -d --build`

Docker should build the application environment comprising a Python container running Flask and a database container running MariaDB.

The website should then be available in the browser at 'localhost:5000'.

To take down the environment, run:

`docker-compose down`

#### populating the database

To intially create the database and a database user:

`docker-compose exec -it db mariadb -u root -p`

Enter your root password as defined in .env.dev.

`CREATE DATABASE toolkit;`
`CREATE USER 'flask'@'%' IDENTIFIED BY '[PASSWORD]';`
`GRANT CREATE, INSERT, UPDATE, SELECT, DELETE ON toolkit.* TO 'flask'@'%';`

Restart the containers to allow Flask to build the database tables:

`docker-compose down`
`docker-compose up -d --build`

You can then use database_functions.sh and an SQL file to populate the database e.g.

`./database_functions -i ./db_imports/toolkit_db_20230112.sql`

## Database functions 

This repository contains a shell script to perform various database functions including importing a whole database from SQL file, exporting the database in SQL, exporting individual tables as tab-delimited txt file, and importing individual tables from tab-delimited txt file. 

Run `./database_functions -h` to see the instructions for this script. 

## Legacy instructions:

The following is no longer required in Flask-SQLAlchemy 3. See https://stackoverflow.com/questions/73968584/flask-sqlalchemy-db-create-all-got-an-unexpected-keyword-argument-app

To build the database tables run:

`docker exec -it python python`
`from app import db, create_app, models`
`db.create_all(app=create_app())`
