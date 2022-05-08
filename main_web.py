import os.path
from math import ceil
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from random import randint


app = Flask(__name__)
db_name = f'local_data#{randint(0, 100)}#.db'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    header = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Note %r>' % self.id


@app.route('/', methods=['GET'])
def main():
    six_note_groups = []
    if os.path.isfile(db_name):
        six_note_groups = Note.query.order_by(Note.date).all()
        six_l = ceil(len(six_note_groups) / 6)
        six_note_groups = [six_note_groups[i * 6:(i + 1) * 6] for i in range(six_l)]
    return render_template('main.html', note_groups=six_note_groups)


@app.route('/add_note', methods=['POST'])
def add_note():
    if not os.path.isfile(db_name):
        db.create_all()
    head = request.form['header']
    text = request.form['text']
    note = Note(header=head, text=text)
    try:
        db.session.add(note)
        db.session.commit()
        return redirect('/')
    except:
        return 'Невозможно добавить заметку'


if __name__ == '__main__':
    app.run(debug=True)