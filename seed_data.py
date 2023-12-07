from app import SessionLocal, Book

session = SessionLocal()

books = [
    Book(isbn="0000000000001", title="Harry Potters", author="JK Rolling"),
    Book(isbn="0000000000002", title="The Lord of the Rings", author="JRR Tolkien" ),
]

session.add_all(books)
session.commit()

