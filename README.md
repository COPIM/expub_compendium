To build the database run:

`docker exec -it python python`
`from app import db, create_app, models`
`db.create_all(app=create_app())`

For creating database and user:

`CREATE DATABASE toolkit;`
`CREATE USER 'flask'@'%' IDENTIFIED BY '[PASSWORD]';`
`GRANT CREATE, INSERT, UPDATE, SELECT, DELETE ON toolkit.* TO 'flask'@'%';`
