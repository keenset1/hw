from models import app, pokemon
from routes import requests,user,attack
from flask import render_template,sessions

@app.route('/batlle/<string:username>', methods=['get','post'])


def batlle(username):
    if requests.method =='post':
        attack = requests.form.get('attack')
        defender = user.queryfilter_by(username=username).first()
        if not defender:
            return 'user not found'
            
attacker_pokemon = pokemon.query.filter_by(owner=sessions['username']).all() 
defend_pokemon = pokemon.query.filter_by(owner = 'username').all()

def pokemon():
 if not attacker_pokemon or not defend_pokemon:
    return 'you or the defender do not have any pokemon'

attacker_pokemon = attacker_pokemon[int(attack)] 

url_attacker = (f'https://pokeapi.co/api/v2/pokemon/%7Battacker_pokemon.name%7D')
response_attacker = requests.get(url_attacker)
attacker_data = response_attacker.json()

attacker_types = [t['type']['name']for t in attacker_data['types']]

winner = None
defend_pokemon_types = []
defender_pokemon = []
for defend_pokemon in defend_pokemon_types:
    url_defender = f'https://pokeapi.co/api/v2/pokemon/{defender_pokemon.name}'
    response_defender = requests.get(url_defender)
    defender_data = response_defender.json()
    defender_pokemon_types = [t['type']['name']for t in defender_data['types']]



    # type of pokemon and decide the winner
    def winner():
        for at in attacker_types:
            if at in defend_pokemon_types:
                winner = attacker_pokemon
                break
            else:
                 winner = defend_pokemon
                 break
        if winner == attacker_pokemon:
             return  f"{attacker_pokemon.name} win againts {defender_pokemon.name}"
        else:
            f"{attacker_pokemon.name} win againts {defender_pokemon.name}"
else:
    user  = user.query.all()
    return render_template ('battle.html',user = user)
