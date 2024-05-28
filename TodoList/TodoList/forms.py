from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired , Length , EqualTo , ValidationError
from TodoList.models import User

class SignForm(FlaskForm):
    username = StringField('Username' , validators = [DataRequired() 
                                                      , Length(min = 4 , max = 20)])
    
    email = StringField('Email' , validators = [DataRequired() 
                                                , Length(min = 4 , max = 20)])
    
    password = PasswordField('Password' , validators = [DataRequired() 
                                                        , Length(min = 6)])
    
    confirm_password = PasswordField("Confirm password" , validators=[DataRequired() 
                                                                      , Length(min=6) , EqualTo("password")])
    
    submit = SubmitField("Sign In")

    def validate_username(self , username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
       
    def validate_email(self , email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')
       

class LoginForm(FlaskForm):
    email = StringField('Email' , validators = [DataRequired() 
                                                , Length(min = 4 , max = 20)])
    
    password = PasswordField('Password' , validators = [DataRequired() 
                                                        , Length(min = 6)])
    
    submit = SubmitField("Login In")
    
class ToDoForm(FlaskForm):
    title = StringField('Title' , validators = [DataRequired() 
                                                , Length(min = 1 , max = 30)])
    
    submit = SubmitField("Add")

