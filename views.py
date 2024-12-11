from app import app
from flask import render_template, request, redirect, url_for
from modelos import Info, Curriculo, Projeto, Contato
import os
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, logout_user, login_required
from peewee import DoesNotExist
from usuario import Usuario

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def home():
    info = Info.select().first()
    curriculo = Curriculo.select().first()
    contato = Contato.select().first()
    projetos = Projeto.select()
    return render_template("index.html", info=info, curriculo=curriculo, projetos=projetos, contato=contato)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard', user_id=current_user.id))
    
    conta_existente = Usuario.select().exists()

    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        usuario = Usuario.get_by_email(email)

        if usuario and usuario.check_password(senha):
            login_user(usuario)
            return redirect(url_for('dashboard', user_id=current_user.id))
        
        error = 'Credenciais incorretas. Tente novamente.'
        return render_template('login.html', error=error, conta_existente=conta_existente)

    return render_template("login.html", conta_existente=conta_existente)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if Usuario.select().count() > 0:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if not nome or not email or not senha:
            error = 'Todos os campos são obrigatórios.'
            return render_template('sign_up.html', error=error)
        
        if senha != confirmar_senha:
            error = 'As senhas não coincidem.'
            return render_template('sign_up.html', error=error)
        
        if Usuario.get_or_none(Usuario.email == email):
            error = 'Este email já está em uso.'
            return render_template('sign_up.html', error=error)
        
        usuario = Usuario(nome=nome, email=email)
        usuario.set_password(senha)
        usuario.save()

        Info.create(
            nome=nome,
            bio="",
            usuario=usuario
        )

        return redirect(url_for('login'))

    return render_template("sign_up.html")


@app.route("/dashboard/<int:user_id>", methods=['GET', 'POST'])
@login_required
def dashboard(user_id):

    if current_user.id != user_id:
        return redirect(url_for('dashboard', user_id=current_user.id))

    try:
        info = Info.get(Info.usuario == current_user)
    except DoesNotExist:
        info = None
    try:
        curriculo = Curriculo.get(Curriculo.usuario == current_user)
    except DoesNotExist:
        curriculo = None
    try:
        contato = Contato.get(Contato.usuario == current_user)
    except DoesNotExist:
        contato = None

    if request.method == 'POST':
        if 'foto' in request.files:
            foto = request.files['foto']

            if foto and allowed_file(foto.filename):
                filename = secure_filename(foto.filename)
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                info.foto = filename
                info.save()

        if "editar_info" in request.form:
            if info:
                info.nome = request.form['nome']
                info.bio = request.form['bio']
                info.save()
            else:
                info = Info.create(
                    nome = request.form['nome'],
                    bio = request.form['bio'],
                    usuario = current_user
                )

        if "editar_curriculo" in request.form:
            if curriculo:
                curriculo.experiencia = request.form['experiencia']
                curriculo.educacao = request.form['educacao']
                curriculo.save()
            else:
                curriculo = Curriculo.create(
                    experiencia = request.form['experiencia'],
                    educacao = request.form['educacao'],
                    usuario = current_user
                )
        
        if "editar_contato" in request.form:
            if contato:
                contato.email = request.form['email']
                contato.telefone = request.form['telefone']
                contato.save()
            else:
                contato = Contato.create(
                    email = request.form['email'],
                    telefone = request.form['telefone'],
                    usuario = current_user
                )
        
        if "adicionar_projeto" in request.form:
            projeto = Projeto.create(
                titulo = request.form['titulo'],
                descricao = request.form['descricao'],
                usuario = current_user
            )
            projeto.save()
        return redirect(url_for('dashboard', user_id=current_user.id))
    
    projetos = Projeto.select()

    return render_template("dashboard.html", info=info, curriculo=curriculo, contato=contato, projetos=projetos)


@app.route("/editar_projeto/<int:id>", methods=['POST'])
def editar_projeto(id):
    projeto = Projeto.get(Projeto.id == id)
    if projeto.id == id:
        projeto.titulo = request.form['titulo']
        projeto.descricao = request.form['descricao']
        projeto.save()
    return redirect(url_for('dashboard', user_id=current_user.id))


@app.route("/deletar_projeto/<int:id>", methods=['POST'])
def deletar_projeto(id):
    projeto = Projeto.get(Projeto.id == id)
    projeto.delete_instance()
    return redirect(url_for('dashboard', user_id=current_user.id))
