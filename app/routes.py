from app import app
from flask import Flask,render_template,request,user,db,redirect,url_for,flash
from models import requests
from flask_login import current_user

app = Flask(__name__)

@app.route('/')
def home():
    return 'welcome to my pokemon app'


@app.route('/pokemon',methods=['get','post'])
def pokemon():
    if requests.method == 'post':
        name = requests.form['name']
        return render_template ('pokemon.html', pokemon = pokemon_data)
    return render_template('index.html')
url = f'https://pokeapi.co/'
response = requests.get('https://pokeapi.co/')
pokemon_data = response.json()
# return render_template ('pokemon.html', pokemon = pokemon_data)
# return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)




   
@app.route('/catch_pokemon/<pokemon_name>')
def catch_pokemon(pokemon_name):
    # check if the pokemon is already in the database
    pokemon = pokemon.query.filter_by(name=pokemon_name).first()
    if not pokemon:
        # if not, add the pokemon to the database
        pokemon = pokemon(name=pokemon_name)
        db.session.add(pokemon)
        db.session.commit()

    # check if the current user has already caught this pokemon
    user_pokemon = user_pokemon.query.filter_by(user_id=current_user.id, pokemon_id=pokemon.id).first()
    if not user_pokemon:
        # check if the user has less than 5 total pokemon
        if len(current_user.pokemon_collection.all()) < 5:
            # add the pokemon to the user's collection
            user_pokemon = user_pokemon(user_id=current_user.id, pokemon_id=pokemon.id)
            db.session.add(user_pokemon)
            db.session.commit()
            return redirect(url_for('pokemon_collection'))
        else:
            flash("You have reached the maximum number of Pokemon in your collection.")
            return redirect(url_for('pokemon_collection'))
    else:
        flash("You have already caught this Pokemon.")
        return redirect(url_for('pokemon_collection'))


@app.route('/remove_pokemon/<pokemon_id>')
def remove_pokemon(pokemon_id):
    user_pokemon = user_pokemon.query.filter_by(user_id=current_user.id, pokemon_id=pokemon_id).first()
    if user_pokemon:
        db.session.delete(user_pokemon)
        db.session.commit()
    return redirect(url_for('pokemon_collection'))

@app.route('/attack/<user_id>')
def attack(user_id):
    target_user = user.query.get(user_id)
    current_user_pokemon = current_user.pokemon_collection.all()
    target_user_pokemon = target_user.pokemon_collection.all()
    return render_template('attack.html', current_user_pokemon=current_user_pokemon, target_user_pokemon=target_user_pokemon)


def determine_winner(user_pokemon, target_user_pokemon):
    # determine winner based on stats, abilities, etc.
    winner = user_pokemon
    loser = target_user_pokemon
    # ...
    return winner, loser

@app.route('/attack/<user_id>')
def attack(user_id):
    target_user = user.query.get(user_id)
    current_user_pokemon = current_user.pokemon_collection.all()
    target_user_pokemon = target_user.pokemon_collection.all()
    winner, loser = determine_winner(current_user_pokemon, target_user_pokemon)
    if winner == current_user_pokemon:
        current_user.wins += 1
        target_user.losses += 1
    else:
        current_user.losses += 1
        target_user.wins += 1
    db.session.commit()
    return render_template('attack.html', winner=winner, loser=loser)

if __name__ == '__main__':
    app.run(debug=True)