from flask import Flask, render_template, request,jsonify
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

[17:34, 1/25/2023] Lauro: @app.route("/catch_pokemon", methods=["POST"])
def catch_pokemon():
    user_id = request.form["user_id"]
    pokemon_name = request.form["pokemon_name"]

    # Check if the user already has the Pokemon
    user_collection = Collection.query.filter_by(user_id=user_id, pokemon_name=pokemon_name).first()

    if user_collection is None:
        # Check if the Pokemon has been collected by any user
        any_user_collection = Collection.query.filter_by(pokemon_name=pokemon_name).first()

        if any_user_collection is None:
            # check if the user has less than 5 Pokemon
            user = User.query.filter_by(id=user_id).first()
            if user.collection_count < 5:
                # The Pokemon has not been collected by any user, so add it to the database
                new_pokemon = Collection(user_id=user_id, pokemon_name=pokemon_name)
                db.session.add(new_pokemon)
                # increment the collection_count
                user.collection_count += 1
                db.session.commit()
                return jsonify({"message": "Pokemon added to collection!"})
            else:
                return jsonify({"message": "You can only have up to 5 Pokemon"})
        else:
            # The Pokemon has already been collected by another user
            return jsonify({"message": "Pokemon already in collection."})
    else:
        # The user already has the Pokemon
        return jsonify({"message": "You already have this Pokemon."})
[17:36, 1/25/2023] Lauro: from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pokemon.db"
db = SQLAlchemy(app)

# Create the "collection" table
class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pokemon_name = db.Column(db.String, nullable=False)

# Create the "user" table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    collection = db.relationship("Collection", backref="user", lazy=True)
    collection_count = db.colunm(db.integer, default=0)

@app.route("/catch_pokemon", methods=["POST"])
def catch_pokemon():
    user_id = request.form["user_id"]
    pokemon_name = request.form["pokemon_name"]

    # Check if the user already has the Pokemon
    user_collection = Collection.query.filter_by(user_id=user_id, pokemon_name=pokemon_name).first()

    if user_collection is None:
        # Check if the Pokemon has been collected by any user
        any_user_collection = Collection.query.filter_by(pokemon_name=pokemon_name).first()

        if any_user_collection is None:
            # The Pokemon has not been collected by any user, so add it to the database
            new_pokemon = Collection(user_id=user_id, pokemon_name=pokemon_name)
            db.session.add(new_pokemon)
            db.session.commit()
            return jsonify({"message": "Pokemon added to collection!"})
        else:
            # The Pokemon has already been collected by another user
            return jsonify({"message": "Pokemon already in collection."})
    else:
        # The user already has the Pokemon
        return jsonify({"message": "You already have this Pokemon."})


    

if __name__ == '__main__':
    app.run(debug=True)