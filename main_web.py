import os.path
from math import ceil
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db_name = f'local_data.db'
app.config['SECRET_KEY'] = '6a060b7c7$$95a212Gb5d01G742e_18888fa114395cD328b_213eA1125594079aaFVDf5SV5168fe43f2FDHHDac441e80bf'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100), default=datetime.utcnow().date())
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
        if head and text:
            db.session.add(note)
            db.session.commit()
        return redirect('/')
    except:
        return 'Невозможно добавить заметку'


@app.route('/delete_note/<int:id>', methods=['GET', 'POST'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect('/')
    except:
        return 'Невозможно удалить заметку'


@app.route('/find_note', methods=['GET', 'POST'])
def find_note():
    founded_notes = []
    head = request.form['header']
    date = request.form['date']
    if os.path.isfile(db_name):
        if head and date:
            founded_notes = Note.query.filter_by(header=head, date=date)
        elif head:
            founded_notes = Note.query.filter_by(header=head)
        elif date:
            founded_notes = Note.query.filter_by(date=date)
        else:
            return render_template('single_main.html', note_groups=founded_notes)
        founded_notes = founded_notes.order_by(Note.date).all()
        six_l = ceil(len(founded_notes) / 6)
        founded_notes = [founded_notes[i * 6:(i + 1) * 6] for i in range(six_l)]
    return render_template('single_main.html', note_groups=founded_notes)


if __name__ == '__main__':
    app.run(debug=True)