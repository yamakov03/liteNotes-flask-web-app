from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from models import Note, User
import json
from app import db
import datetime
from werkzeug.security import check_password_hash
from . import csrf

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('ckeditor')
        title = request.form.get('title')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id, title=title)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html", user=current_user, time=datetime.datetime.utcnow().strftime("%A, %B %d, %I:%M %p"))

@views.route('/delete-note', methods=['POST'])
@csrf.exempt
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/edit-note/<int:noteId>' , methods=['GET','POST'])
def edit_note(noteId):
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id and request.method == 'POST' and request.form.get('ckeditor'):
                note.data = request.form.get('ckeditor')
                note.title = request.form.get('title')
                note.time = datetime.datetime.utcnow()
                db.session.commit()
                flash('Note updated!', category='success')
                return redirect('/')
    return render_template("edit.html", user=current_user, title=note.title, article_body=note.data, time=datetime.datetime.utcnow().strftime("%B %d, %I:%M %p"))

@views.route('/duplicate-note' , methods=['POST'])
@csrf.exempt
def duplicate_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            new_note = Note(data=note.data, user_id=current_user.id, title=note.title)
            db.session.add(new_note)
            db.session.commit()
            flash('Note duplicated!', category='success')
    return jsonify({})

@views.route('/delete-account', methods=['POST'])
def delete_account():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                db.session.delete(user)
                db.session.commit()
                flash('Account deleted!', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return redirect('/')