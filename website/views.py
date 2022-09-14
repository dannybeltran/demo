import json
from crypt import methods
from nis import cat
from flask import Blueprint, render_template, redirect, request, flash, url_for, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is empty", category="error")
        else:
            flash("Note added!", category="success")
            new_note = Note(text=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            # return redirect(url_for('views.home'))
    return render_template("home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    id = json.loads(request.data)["id"]
    note = Note.query.get(id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
