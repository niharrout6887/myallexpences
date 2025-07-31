from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, RadioField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class EntryForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    payment_method = RadioField('Payment Method', choices=[('Cash','Cash'), ('Online','Online')], validators=[DataRequired()])
    payment_reason = StringField('Payment Reason', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Submit')
