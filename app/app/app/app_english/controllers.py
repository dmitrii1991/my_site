from flask import Flask, render_template, g, request, flash, redirect, url_for, abort, make_response, session
from flask import Blueprint

from app.database import db

from .models import View, Category, Words, insert_data


app_english = Blueprint('app_english', __name__, template_folder='templates', static_folder='static')


@app_english.route('/')
def english():
    return render_template('app_english/base_app_english.html')


@app_english.route('/programm')
@app_english.route('/programm/<int:page>', methods=['GET', 'POST'])
def english_words(page=1):
    all_words = db.session.query(Words).filter(Words.category_id == '1').paginate(page, 25, False)
    len_all_words = all_words.total
    now_page = all_words.page
    return render_template('app_english/english_words_programm.html', now_page=now_page, len_all_words=len_all_words, all_words=all_words)


@app_english.route('/other')
@app_english.route('/other/<int:page>', methods=['GET', 'POST'])
def english_words_other(page=1):
    all_words = db.session.query(Words).filter(Words.category_id == '2').paginate(page, 25, False)
    len_all_words = all_words.total
    now_page = all_words.page
    return render_template('app_english/english_words_other.html', now_page=now_page, len_all_words=len_all_words, all_words=all_words)


@app_english.route('/11')
def english2():
    insert_data()
    return render_template('app_english/base_app_english.html')
