from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cliente.db'
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Cliente %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        novo_cliente = Cliente(name=name, email=email,
        endereco=endereco, telefone=telefone )

        try:
            db.session.add(novo_cliente)
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um erro!'

    else:
        clientes = Cliente.query.order_by(Cliente.created_at).all()
        return render_template('index.html', clientes=clientes)


@app.route('/delete/<int:id>')
def delete(id):
    cliente_del = Cliente.query.get_or_404(id)

    try:
        db.session.delete(cliente_del)
        db.session.commit()
        return redirect('/')
    except:
        return 'Ocorreu um erro ao deletar'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Ocorreu um erro tente mais tarde'

    else:
        return render_template('update.html', cliente=cliente)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)