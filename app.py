from flask import Flask, jsonify, request, abort
from marshmallow import Schema, fields
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Book

app = Flask(__name__)

# Connecting postgresql
engine = create_engine("postgresql://postgres:1234@localhost/library")
# engine = create_engine("postgresql://user:password@localhost/library")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Schema for book
class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    isbn = fields.String(required=True)
    title = fields.String(required=True)
    author = fields.String(required=True)

# 1) Retrieve all books
@app.route("/api/books", methods=["GET"])
def get_all_books():
    
    session = SessionLocal()
    books = session.query(Book).all()
    schema = BookSchema(many=True)
    return jsonify(schema.dump(books))

# 2) Add a new book
@app.route("/api/books", methods=["POST"])
def add_book():
    session = SessionLocal()

    try:
        data = request.get_json()
        schema = BookSchema()
        validated_data = schema.load(data)

        new_book = Book(**validated_data)
        session.add(new_book)
        session.commit()

        schema = BookSchema()
        return jsonify(schema.dump(new_book)), 201
    except Exception as e:
        session.rollback()
        abort(400, description=str(e))

# 3) Update book details
@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book_details(book_id):
    
    session = SessionLocal()

    try:
        data = request.get_json()
        schema = BookSchema()
        validated_data = schema.load(data, partial=True)

        book = session.query(Book).get(book_id)
        if not book:
            abort(404)

        for key, value in validated_data.items():
            setattr(book, key, value)

        session.commit()

        schema = BookSchema()
        return jsonify(schema.dump(book))
    except Exception as e:
        session.rollback()
        abort(400, description=str(e))
