One of the key deliverables for Work Package 6 of the COPIM project is "an online resource detailing opportunities for experimental book publishing". We've decided to put this together in the form of an online toolkit with details of software, practices, examples, and sensitivities that can be used for experimental publishing.

The online toolkit will build on this review of tools to present a resource for a researcher, artist, or publisher looking to try experimental publishing. From our preliminary design discussions, we have plans to include not only software tools that can be used to do experimental publishing but examples of experimental publications, practices of experimental publishing, publishers who have done some form of experimental publishing, and sensitivities involved in experimental publishing.

## Database functions 

This repository contains a shell script to perform various database functions including importing a whole database from SQL file, exporting the database in SQL, exporting individual tables as tab-delimited txt file, and importing individual tables from tab-delimited txt file. 

Run `./database_functions -h` to see the instructions for this script. 

## Legacy instructions:

The following is no longer required in Flask-SQLAlchemy 3. See https://stackoverflow.com/questions/73968584/flask-sqlalchemy-db-create-all-got-an-unexpected-keyword-argument-app


For creating database and user in production:

`docker-compose exec -it db mysql -u root -p`
`CREATE DATABASE toolkit;`
`CREATE USER 'flask'@'%' IDENTIFIED BY '[PASSWORD]';`
`GRANT CREATE, INSERT, UPDATE, SELECT, DELETE ON toolkit.* TO 'flask'@'%';`

To build the database run:

`docker exec -it python python`
`from app import db, create_app, models`
`db.create_all(app=create_app())`
