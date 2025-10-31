import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ev3th:H7gIVtAT1oawosUJpc3U05lpTUpqsQrP@dpg-d2vp4ejuibrs73djr4r0-a.oregon-postgres.render.com/db_tec_vqqh'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

    def to_dict(self):
        return{
            'no_control': self.no_control,
            'nombre': self.nombre,
            'ap_paterno': self.ap_paterno,
            'ap_materno': self.ap_materno,
            'semestre': self.semestre,
        }

with app.app_context():
    db.create_all()

#Ruta raiz
@app.route('/')
def index():
    #return 'Hola Mundo'
    
    # Trae todos los estudiantes
    estudiantes = Estudiante.query.all()
    return render_template('index.html', estudiantes=estudiantes)

#Ruta /estudiantes crear un nuevo estudiante
@app.route('/estudiantes/new', methods=['GET','POST'])
def create_estudiante():
    if request.method == 'POST':
        
        #Agregar Estudiante
        no_control = request.form['no_control']
        nombre = request.form['nombre']
        ap_paterno = request.form['ap_paterno']
        ap_materno = request.form['ap_materno']
        semestre = request.form['semestre']

        nvo_estudiante = Estudiante(no_control=no_control, nombre=nombre, ap_paterno=ap_paterno, ap_materno= ap_materno, semestre= semestre)

        db.session.add(nvo_estudiante)
        db.session.commit()

        return redirect(url_for('index'))
    
    #Aqui sigue si es GET
    return render_template('create_estudiante.html')

#Actualizar estudiante
@app.route('/estudiantes/update/<string:no_control>', methods=['GET','POST'])
def update_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    if request.method == 'POST':
        estudiante.nombre = request.form['nombre']
        estudiante.ap_paterno = request.form['ap_paterno']
        estudiante.ap_materno = request.form['ap_materno']
        estudiante.semestre = request.form['semestre']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_estudiante.html', estudiante=estudiante)

#Eliminar estudiante
@app.route('/estudiantes/delete/<string:no_control>')
def delete_estudiante(no_control):
    alumno = Estudiante.query.get(no_control)
    if alumno:
        db.session.delete(alumno)
        db.session.commit()
    return redirect(url_for('index'))

#Ruta /estudiantes
@app.route('/alumnos')
def getAlumnos():
    return 'Aqui van los alumnos'


if __name__ == '__main__':
    app.run(debug=True)
