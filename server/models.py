from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)

    posts = db.relationship("Post", backref="author")

    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name")
        return name

    @validates("phone_number")
    def validate_phone(self, key, phone_number):
        if not re.fullmatch(r"\d{10}", phone_number):
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String)
    category = db.Column(db.String)

    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    @validates("content")
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates("summary")
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters")
        return summary

    @validates("category")
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return category

    @validates("title")
    def validate_title(self, key, title):
        clickbait_words = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_words):
            raise ValueError("Title must be sufficiently clickbait-y")
        return title

