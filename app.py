from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

#database configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Note('{self.title}', '{self.body}', '{self.created_at}')"

 # Created  new note
@app.route('/notes', methods=['POST'])
def create_note():
    data = request.get_json()
    new_note = Note(title=data['title'], body=data['body'])
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note created successfully', 'note': new_note.__repr__()})

# Read  notes
@app.route('/notes', methods=['GET'])
def get_notes():
    notes = Note.query.all()
    return jsonify([note.__repr__() for note in notes])

# Update notes
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    note = Note.query.get(note_id)
    data = request.get_json()
    note.title = data['title']
    note.body = data['body']
    db.session.commit()
    return jsonify({'message': 'Note updated successfully', 'note': note.__repr__()})

# Delete  notes
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    note = Note.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully', 'note': note.__repr__()})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0',port=4040)
