from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
import smtplib

# Credencials -------------------------------
email_send = "marco.a.ponce.p@gmail.com"  # "bretrayal_nights@yahoo.com"
password_not = "jfkgsrpzyozggrml"  # "coyotas515"
email_to = "maarco.app98@gmail.com"

# Flask setup
app = Flask(__name__)
app.config['SECRET_KEY'] = "8f5s6d4f9s3d5fs9d3s6"

# Bootstrap Set up
Bootstrap(app)

# SQL set up

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///clients.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    cellphone = db.Column(db.String(250), nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    game_type = db.Column(db.String(250), nullable=False)
    cp = db.Column(db.String(250), nullable=False)


db.create_all()


class Info(FlaskForm):
    name = StringField(label="full name", validators=[DataRequired()])
    email = StringField(label="email", validators=[DataRequired(), Email()])
    cellphone = StringField(label="Número celular", validators=[DataRequired()])
    numero_personas = SelectField(label="Número de personas que participaran",
                                  choices=["8", "9", "10", "11", "12", "13", "14", "15", "más de 15"])
    game_type = SelectField(label="Historia",
                            choices=["Panic At The Disco!", "Sombras del Pasado", "Demoliendo Destinos"])
    cp = StringField(label="Código Postal", validators=[DataRequired()])
    submit_button = SubmitField('submit')


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/info', methods=["GET", "POST"])
def info():
    info_form = Info()
    if info_form.validate_on_submit():
        message = f'''Subject: Cotizacion nueva \n \n
                 {info_form.name.data} quiere cotizar una sesion para {info_form.numero_personas.data} personas, 
                para la historia {info_form.game_type.data}. Lo puedes contactar por WhatsApp 
                al numero: {info_form.cellphone.data} o a su correo: {info_form.email.data}, 
                su CP es {info_form.cp.data}.'''.encode("utf-8")
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            try:
                connection.login(user=email_send, password=password_not)
                connection.sendmail(
                    from_addr=email_send,
                    to_addrs=email_to,
                    msg=message
                )
            except Exception as e:
                # Print any error messages to stdout
                print(e)
            

        new_client = Client(
            name=info_form.name.data,
            email=info_form.email.data,
            cellphone=info_form.cellphone.data,
            numero_personas=info_form.numero_personas.data,
            game_type=info_form.game_type.data,
            cp=info_form.cp.data
        )
        db.session.add(new_client)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('info.html', form=info_form)


if __name__ == '__main__':
    app.run(debug=True)
