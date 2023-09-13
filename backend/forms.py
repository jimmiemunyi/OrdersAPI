from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField


# update profile form
class UpdateCustomerForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    contact = StringField(
        "Contact (2547XXXXXXXX)",
    )
    submit = SubmitField("Update Profile")


class MakeOrderForm(FlaskForm):
    item = StringField("Item")
    amount = FloatField()
    submit = SubmitField("Make Order")
