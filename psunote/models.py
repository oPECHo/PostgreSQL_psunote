from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

        db.reflect()


note_tag_m2m = db.Table(
    "note_tag",
    sa.Column("note_id", sa.ForeignKey("notes.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False)

    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())


class Note(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)

    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text)

    tags: Mapped[list[Tag]] = relationship(secondary=note_tag_m2m)

    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
