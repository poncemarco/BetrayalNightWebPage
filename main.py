from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email
import smtplib

# Credencials -------------------------------
email_send = "marco.a.ponce.p@gmail.com"#"bretrayal_nights@yahoo.com"
password_not = "7471482660" #"coyotas515"
email_to = "maarco.app98@gmail.com"


app = Flask(__name__)
app.config['SECRET_KEY'] = "8f5s6d4f9s3d5fs9d3s6"

Bootstrap(app)

class Info(FlaskForm):
    name = StringField(label="full name", validators=[DataRequired()])
    email = StringField(label="email", validators=[DataRequired(), Email()])
    cellphone = StringField(label="Número celular", validators=[DataRequired()])
    numero_personas = SelectField(label="Número de personas que participaran", choices=[5, 6, 7, 8, 9, 10, 11, 12, "más de 12"])
    game_type = SelectField(label="Historia", choices=["Panic At The Disco!", "Sombras del Pasado", "Demoliendo Destinos"])
    submit_button = SubmitField('submit')

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/info', methods=["GET", "POST"])
def info():
    info_form = Info()
    if info_form.validate_on_submit():
        with smtplib.SMTP('smtp.gmail.com', 465) as connection:
            connection.starttls()
            connection.login(user=email_send, password=password_not)
            connection.sendmail(
                from_addr=email_send,
                to_addrs=email_to,
                msg=f'Subject: Cotizacion nueva \n\n '
                    f'{info_form.name.data} quiere cotizar una sesion para'
                    f'{info_form.numero_personas.data} personas, para la historia'
                    f'{info_form.game_type.data} \n '
                    f'Lo puedes contactar por WhatsApp al número: {info_form.cellphone.data} \n'
                    f'o a su correo: {info_form.email.data}'
            )
        return redirect(url_for('home'))

    return render_template('info.html', form=info_form)


if __name__ == '__main__':
    app.run(debug=True)