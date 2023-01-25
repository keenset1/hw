from flask import Flask, render_template, request
from app import app 
from models import requests, attack
from flask_sqlalchemy import SQLAlchemy
from app import app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pokemon.db'
db = SQLAlchemy(app)

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    hp = db.Column(db.Float, nullable=False)
    defense = db.Column(db.Float, nullable=False)
    attack = db.Column(db.String(100), nullable=False)
    owner = db.Column(db.String(100), nullable=False)


    def _repr_(self):
        return f"Pokemon('{self.name}', '{self.hp}', '{self.defense}','{self.attack})"


@app.route('/')
def home():
    return "Welcome to the Pokemon App"

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        name = request.form['name']
        owner = request.form['owner']
        pokemon = Pokemon.query.filter_by(name=name, owner=owner).first()
        if not pokemon:
            url = f'https://pokeapi.co/api/v2/pokemon/{name}'
            response = requests.get(url)
            pokemon_data = response.json()
            pokemon = Pokemon(name=pokemon_data['name'], hp=pokemon_data['hp'], attack=pokemon_data['attack'], defense =pokemon_data['defense'],  owner=owner)
            db.session.add(pokemon)
            db.session.commit()
        return render_template('pokemon.html', pokemon=pokemon)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)