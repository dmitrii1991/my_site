import os
from datetime import datetime

import pandas
from gtts import gTTS

from app.database import db


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<Category %r>' % self.name


class View(db.Model):
    __tablename__ = 'view'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return '<View %r>' % self.name


class Words(db.Model):
    __tablename__ = 'words'
    __table_args__ = (
        db.UniqueConstraint("view_id", "word"),
    )
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(255), nullable=False)
    translation = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(511), nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category = db.relationship('Category',  backref=db.backref('words', lazy=True))

    view_id = db.Column(db.Integer, db.ForeignKey('view.id', ondelete='CASCADE'), nullable=False)
    view = db.relationship('View',  backref=db.backref('views', lazy=True))

    def __repr__(self):
        return '<Words %r>' % self.word


def insert_data():
    """Обогощаем таблицу из данных xlsx"""
    db.create_all()
    direct = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data\english.xlsx')
    music_directory = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static\music')
    df_program = pandas.read_excel(direct, sheet_name='programm')
    df_other = pandas.read_excel(direct, sheet_name='other')
    view_dict = {}
    category_dict = {}
    words_in_base = []
    words = []

    view_all = db.session.query(View).all()
    if view_all:
        for elem in view_all:
            view_dict[elem.name] = elem.id

    category_all = db.session.query(Category).all()
    if category_all:
        for elem in category_all:
            category_dict[elem.name] = elem.id

    if "Программирование" not in category_dict.keys():
        new_category = Category(name="Программирование")
        db.session.add(new_category)
        db.session.commit()
        id_category_programm = new_category.id                  # возвращ id
        category_dict["Программирование"] = id_category_programm
    else:
        id_category_programm = category_dict["Программирование"]
    if "Остальное" not in category_dict.keys():
        new_category = Category(name="Остальное")
        db.session.add(new_category)
        db.session.commit()
        id_category_other = new_category.id                  # возвращ id
        category_dict["Остальное"] = id_category_other
    else:
        id_category_other = category_dict["Остальное"]

    words_all = db.session.query(Words).all()
    for element in words_all:
        el = tuple([element.view_id, element.word])
        words_in_base.append(el)

    for i, row in df_program.iterrows():
        if row["Вид"] not in view_dict.keys():
            new_view = View(name=row["Вид"])
            db.session.add(new_view)
            db.session.commit()
            id_view = new_view.id                              # возвращ id
            view_dict[row["Вид"]] = id_view
        else:
            id_view = view_dict[row["Вид"]]
        if tuple([view_dict[row["Вид"]], row["англ"]]) not in words_in_base:
            words.append(Words(word=row['англ'], translation=row['перев'], url='', category_id=id_category_programm, view_id=id_view))
            tts = gTTS(row['англ'], lang='en')
            tts.save(os.path.join(music_directory, f"{row['англ']}.mp3"))
            print(f'Добавлено {row["англ"]}')

    if words:
        db.session.add_all(words)
        db.session.commit()

    words = []
    for i, row in df_other.iterrows():
        if row["Вид"] not in view_dict.keys():
            new_view = View(name=row["Вид"])
            db.session.add(new_view)
            db.session.commit()
            id_view = new_view.id                              # возвращ id
            view_dict[row["Вид"]] = id_view
        else:
            id_view = view_dict[row["Вид"]]
        if tuple([view_dict[row["Вид"]], row["англ"]]) not in words_in_base:
            words.append(Words(word=row['англ'], translation=row['перев'], url='', category_id=id_category_other, view_id=id_view))
            tts = gTTS(row['англ'], lang='en')
            tts.save(os.path.join(music_directory, f"{row['англ']}.mp3"))
            print(f'Добавлено {row["англ"]}')
    if words:
        db.session.add_all(words)
        db.session.commit()


if __name__ == '__main__':
    db.create_all()
    insert_data()