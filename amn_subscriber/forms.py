from flask_wtf import FlaskForm
import wtforms as f


class MainForm(FlaskForm):
    surname = f.StringField(
        'Prénom',
        validators=[
            f.validators.input_required(message='Ce champ est requis'),
            f.validators.Length(min=3, max=100, message='La valeur doit être comprise entre 3 et 100 caractères')
        ])
    name = f.StringField(
        'Nom',
        validators=[
            f.validators.input_required(message='Ce champ est requis'),
            f.validators.Length(min=3, max=100, message='La valeur doit être comprise entre 3 et 100 caractères')
        ])

    email = f.StringField(
        'Adresse e-mail',
        validators=[
            f.validators.input_required(message='Ce champ est requis'),
            f.validators.email(message="Ceci n'est pas une adresse email valide")]
    )

    note = f.TextAreaField('Commentaire', render_kw={'placeholder': "Si vous avez un commentaire, c'est ici !"})

    gdpr = f.BooleanField(
        "J'accepte de recevoir, à cette addresse email, les futures infolettres de l'association.",
        validators=[f.validators.input_required('ce choix est nécessaire')]
    )

    submit_button = f.SubmitField("S'inscrire")


class LoginForm(FlaskForm):
    login = f.StringField('Login', validators=[f.validators.InputRequired()])
    password = f.PasswordField('Mot de passe', validators=[f.validators.InputRequired()])
    next = f.HiddenField(default='')

    login_button = f.SubmitField('Login')
