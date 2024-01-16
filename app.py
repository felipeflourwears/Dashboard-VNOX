from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions

import time

# Variables globales para almacenar el token y su tiempo de expiración
token_info = {
    'token': None,
    'expiration_time': 0
}

app = Flask(__name__)
model_token = ModelToken() 
model_actions = ModelActions() 


def obtener_token():
    print("Entrando a la funcion OT")
    current_time = time.time()

    # Verificar si el token existente sigue siendo válido
    if token_info['token'] is None or current_time > token_info['expiration_time']:
        # Obtener un nuevo token si no hay uno existente o ha expirado
        new_token = ModelToken.get_token()
        token_info['token'] = new_token
        # Establecer el tiempo de expiración (ajusta según sea necesario)
        token_info['expiration_time'] = current_time + 86000
        print("NEW TOKEN")
        print("token: ", token_info)
        return token_info['token']
    else:
        print("ELSE TODAVIA MISMO TOKEN")
        print("token: ", token_info)
        return token_info['token']
    
@app.route('/reset_player/<string:player_id>', methods=['GET'])
def reset_player(player_id):
    try:
        token = obtener_token()
        print(f"Token: {token}")
        
        ModelActions.reset_player(token, player_id)
        print(f"Player reset successfully: {player_id}")

        # Redirigir al usuario a la ruta principal después de resetear el player
        return redirect(url_for('index', reset='reset'))
    except Exception as e:
        print(f"Error resetting player: {str(e)}")
        # Aquí puedes agregar un manejo más específico del error si es necesario
        return render_template('404.html', error_message=str(e))



@app.route('/')
def index():
    token = obtener_token()
    get_players = ModelToken.use_token_getPlayerList(token)
    print(get_players)
    num_players = len(get_players)
    print(f"El número total de players es: {num_players}")
    reset_status = request.args.get('reset', None)
    return render_template('index.html', players_info=get_players, reset_status=reset_status)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=puerto)
    app.run()