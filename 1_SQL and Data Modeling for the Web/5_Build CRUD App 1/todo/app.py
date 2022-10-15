from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

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


class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"<Todo {self.id} {self.description}>"


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template(
        "index.html",
        data=Todo.query.all(),
    )


# @app.route("/todos/create", methods=["POST"])
# def create_todo():
#     description = request.form.get("description", "")
#     todo = Todo(description=description)
#     db.session.add(todo)
#     db.session.commit()
#     return redirect(url_for("index"))


@app.route("/todos/create", methods=["POST"])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()["description"]
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        body["description"] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)
    else:
        return jsonify(body)


if __name__ == "__main__":
    app.run(debug=True)
