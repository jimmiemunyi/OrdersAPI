from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


# update profile form
class UpdateCustomerForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    contact = StringField("Contact")
    submit = SubmitField("Update Profile")
