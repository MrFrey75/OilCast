from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

page_sections = db.Table(
    'page_sections',
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True),
    db.Column('section_id', db.Integer, db.ForeignKey('section.id'), primary_key=True),
    db.Column('position', db.Integer)  # for ordering
)


class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    pages = db.relationship('Page', backref='board', lazy=True)
    page_view_time = db.Column(db.Integer, default=10)  # in seconds


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    sections = db.relationship('Section', secondary=page_sections,
                               backref=db.backref('pages', lazy='dynamic'),
                               order_by='page_sections.c.position')
    show_title = db.Column(db.Boolean, default=True)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=True)
    content = db.Column(db.Text, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
