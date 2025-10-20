from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Length

class MateriForm(FlaskForm):
    judul = StringField('Judul', validators=[DataRequired()])
    deskripsi = TextAreaField('Deskripsi')
    kategori = SelectField('Kategori', choices=[
        ('Matematika', 'Matematika'),
        ('Bahasa', 'Bahasa'),
        ('Sains', 'Sains'),
        ('Sosial', 'Sosial')
    ])
    video_url = StringField('URL Video')
    file = FileField('Upload File')
    submit = SubmitField('Simpan')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Daftar')

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField('Password Lama', validators=[DataRequired()])
    new_password = PasswordField('Password Baru', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Ubah Password')
