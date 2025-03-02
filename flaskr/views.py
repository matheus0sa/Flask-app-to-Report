from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import g

from werkzeug.exceptions import abort

from .auth import login_required
from .db import get_db

import os

bp = Blueprint("reports", __name__)


        


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    reports = os.listdir('flaskr/scripts')
    return render_template("reports/index.html", reports=reports)


def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("report.index"))

    return render_template("report/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?", (title, body, id)
            )
            db.commit()
            return redirect(url_for("report.index"))

    return render_template("report/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("report.index"))


def get_report(nick):
    
    f = open(f'flaskr/scripts/{nick}.py', 'r')
    f_plaintext = f.read()
    f.close()

    exec(f_plaintext)

    return locals()['R']()

@bp.route("/view/<nick>")
@login_required
def view(nick):
    df = get_report(nick)
    df = df.to_html(max_rows=30, max_cols=10, justify='center', show_dimensions=True)
    return render_template("reports/report.html", df=df, nick=nick.capitalize())


@bp.route("/inserir", methods=("GET", "POST"))
@login_required
def inserir():
    if request.method == "POST":
        nick = request.form["nick"]
        file = request.files['file']
        file.save(f'flaskr/scripts/{nick}.py')
        print(nick)
        print(file)
    return render_template("reports/insert.html")



@bp.route("/replace/<nick>")
@login_required
def replace(nick):
    return 'To do'


@bp.route("/deleteR/<nick>")
@login_required
def deleteR(nick):
    return 'To do'
