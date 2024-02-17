from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Client(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))

        flash('Usuário ou senha incorretos. Tente novamente.', 'danger')

    return render_template('login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    flash('Logout realizado.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return render_template('dashboard.html', user=user)
    else:
        flash('Faça login para acessar o painel!', 'warning')
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        existing_email = User.query.filter_by(email=email).first()

        if existing_user:
            flash('O nome de usuário já está em uso.', 'danger')
        elif existing_email:
            flash('O email já está cadastrado no sistema. Clique em "Esqueci a senha".')
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(name=name, lastname=lastname, email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/new_client', methods=['GET', 'POST'])
def register_new_client():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        email = request.form['email']

        existing_client = Client.query.filter_by(name=name).first()
        existing_email = Client.query.filter_by(email=email).first()

        if existing_client:
            flash(f'O cliente {name} já possui cadastro, verifique seus dados na tela de consulta.', 'warning')
        elif existing_email:
            flash('O email já possui cadastro, verifique seus dados na tela de consulta.', 'warning')
        elif name == '':
            flash('Preencha o nome do cliente!', 'warning') 
        elif company == '':
            flash('Preencha o nome da empresa', 'warning')
        elif email == '':
            flash('Preencha o email do cliente', 'warning')
        else:
            new_client = Client(name=name, company=company, email=email)
            db.session.add(new_client)
            db.session.commit()
            flash(f'Cliente {name} cadastrado com sucesso!')
            return redirect(url_for('register_client'))
    return render_template('cadastro-cliente.html')

@app.route('/register_client', methods=['POST'])
def register_client():
    return render_template('cadastro-cliente.html')

@app.route('/view_client', methods=['GET', 'POST'])
def view_client():
    conn = sqlite3.connect('api/instance/database.db')
    cursor = conn.cursor()

    # Encontrar os clientes
    cursor.execute('''
        SELECT id, name FROM clientes;    
    ''')
    options = cursor.fetchall()

    # Encontrar as empresas
    cursor.execute('''
        SELECT company FROM empresas;
    ''')
    company = cursor.fetchall()

    conn.close()

    clientes = search_all_clients()

    return render_template('consulta-cliente.html', options=options, empresas=company, clientes=clientes)


def search_cients(selected_company):
    conn = sqlite3.connect('api/instance/database.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM clientes
        WHERE company = ?
    ''', (selected_company,))
    clients = c.fetchall()
    conn.close()

    return clients

def search_all_clients():
    conn = sqlite3.connect('api/instance/database.db')
    c = conn.cursor()
    c.execute('''
        SELECT * FROM clientes
    ''')
    clients = c.fetchall()
    conn.close()

    return clients

@app.route('/search', methods=['POST'])
def search():

    if 'company' not in request.form:
        return abort(400, "Campo não encontrado na solicitação!")

    selected_company = request.form['company']

    conn = sqlite3.connect('api/instance/database.db')
    c = conn.cursor()
    c.execute('''
        SELECT company FROM empresas;
    ''')
    empresas = c.fetchall()
    conn.close()

    if not selected_company:
        clientes = search_all_clients()
        return render_template('consulta-cliente.html', empresas=empresas, clientes=clientes)

    if selected_company:
        clientes = search_cients(selected_company)
        return render_template('consulta-cliente.html', empresas=empresas, clientes=clientes, empresa_selecionada=selected_company)

        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port='5000', debug=True)