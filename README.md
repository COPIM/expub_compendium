To build the database run:

`docker exec -it python python`
`from app import db, create_app, models`
`db.create_all(app=create_app())`
