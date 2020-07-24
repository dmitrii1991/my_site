from flask import render_template, request, redirect, url_for, flash, make_response, session

from app import create_app
from app.models import Feedback
from app.database import db
from app.forms import FeedbackForm

app = create_app()
app.config.from_object('config.BaseConfig')


@app.route("/")
def main():
    return render_template('main.html')


@app.route("/about_me")
def about():
    return render_template('about_me.html')


@app.route("/feedback",  methods=["POST", "GET"])
def feedback():
    form = FeedbackForm()
    if request.method == 'POST':
        name = request.form['name']
        topic = request.form['topic']
        email = request.form['email']
        text = request.form['text']
        if len(name) > 2 and len(topic) > 2 and '@' in email:
            try:
                feedback = Feedback(name=name, topic=topic, email=email, text=text)
                db.session.add(feedback)
                db.session.commit()
                flash('Сообщение отправлено', category='success')
            except:
                flash('Ошибка отправки - ошибка сервера', category='error')
        else:
            flash('Ошибка отправки (имя, тема должны содержать хотябы 3 символа и почта должна быть валидна)', category='error')
    return render_template('feedback.html', form=form)


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('errors/404.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001, debug=False)
