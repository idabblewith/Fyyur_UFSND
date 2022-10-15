from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

dialect = "postgresql+psycopg2"
username = "postgres"
password = "1"
db_host = "localhost"
db_port = "5432"
db_name = "test"

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"{dialect}://{username}:{password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    person = Person.query.first()
    return f"Hello {person.name}!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)
