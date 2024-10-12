from flask import Flask, jsonify, request
from flask_cors import CORS  # Importa CORS
from animeflv import AnimeFLV

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas las rutas

@app.route('/search', methods=['GET'])
def search_anime():
    anime_name = request.args.get('name')
    if anime_name:
        api = AnimeFLV()
        animes = api.search(anime_name)
        return jsonify([{'id': anime.id, 'title': anime.title} for anime in animes])
    else:
        return jsonify({'error': 'Please provide an anime name'}), 400

@app.route('/anime', methods=['GET'])
def anime_info():
    id = request.args.get('id')
    
    # Validación de que el id no sea None o vacío
    if not id:
        return jsonify({'error': 'No anime ID provided'}), 400

    try:
        api = AnimeFLV()
        anime = api.get_anime_info(id)  # Asegúrate de que este método devuelva la información detallada del anime
        
        # Validación de que anime no sea None y contenga los atributos esperados
        if anime.id != None and anime.title != None and anime.synopsis != None:
            return jsonify({
                'id': anime.id,
                'title': anime.title,
                'description': anime.synopsis,
                'poster': anime.poster
            })
        else:
            return jsonify({'error': 'Anime not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
