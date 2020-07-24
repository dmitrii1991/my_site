from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class FeedbackForm(FlaskForm):
    pass
    # name = PasswordField("Имя: ", validators=[DataRequired(), Length(min=4, max=255)])
    # topic = PasswordField("Тема: ", validators=[DataRequired(), Length(min=4, max=255)])
    # email = StringField("Email: ", validators=[Email()])
    # remember = BooleanField("Запомнить", default=False)
    # submit = SubmitField("Отправить")