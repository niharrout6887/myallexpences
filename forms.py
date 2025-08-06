from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SubmitField, DateField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class EntryForm(FlaskForm):
    date = DateField('Date', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    payment_method = StringField('Payment Method', validators=[InputRequired(), Length(max=100)])
    payment_reason = StringField('Payment Reason', validators=[InputRequired(), Length(max=200)])
    submit = SubmitField('Save')
