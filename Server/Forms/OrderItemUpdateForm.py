from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, IntegerField
from wtforms.validators import Length, Email, DataRequired, ValidationError, EqualTo


class OrderItemUpdateForm(FlaskForm):
    count = IntegerField("Колличество: ", validators=[DataRequired()])
    submit = SubmitField("Сохранить")