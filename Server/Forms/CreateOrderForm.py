from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length


class CreateOrderForm(FlaskForm):
    workshops = SelectField("Производства", coerce=str)
    city = StringField("Город", validators=[])
    street = StringField("Улица", validators=[])
    home = IntegerField("Дом", validators=[])
    apartment = IntegerField("Квартира", validators=[])
    floor = IntegerField("Этаж", validators=[])
    type_order = HiddenField()
    description = TextAreaField("Комментарии к заказу")
    type_payment = SelectField("Тип оплаты", choices=[("1", "оплата при получении")])
    submit = SubmitField("Заказать")