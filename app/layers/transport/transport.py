#---------------------------------------------------------------------------------------------------------------------------------------

# Este archivo se conecta con la API, y obtiene los datos de cada Pokémon en formato JSON."

# Un JSON es un formato utilizado para guardar e intercambiar datos. Está formado por pares clave-valor."

"""
Ejemplo:

{
  "pokemon": [
    {
      "nombre": "Charizard",
      "tipo": "Fuego"
    },
  ]
}

"""
#---------------------------------------------------------------------------------------------------------------------------------------


# capa de transporte/comunicación con otras interfaces o sistemas externos.

import requests
from ...config import config

# comunicación con la REST API.
# este método se encarga de "pegarle" a la API y traer una lista de objetos JSON.

def get_AllImages():   # Se cambió el nombre de la función getAllImages(), por get_AllImages() para evitar confusiones con el archivo services.py
    json_collection = []
    for id in range(1, 152):   # Este es el rango que recorre la API (osea los pokémones que va a mostrar). Se ampliá el rango (originalmente 30) para mostrar los de la primera generación (151) 
        response = requests.get(config.STUDENTS_REST_API_URL + str(id))

        # si la búsqueda no arroja resultados, entonces retornamos una lista vacía de elementos.    
        if not response.ok:
            print(f"[transport.py]: error al obtener datos para el id {id}")
            continue

        raw_data = response.json()

        if 'detail' in raw_data and raw_data['detail'] == 'Not found.':
            print(f"[transport.py]: Pokémon con id {id} no encontrado.")
            continue

        json_collection.append(raw_data)

    return json_collection

# obtiene la imagen correspodiente para un type_id especifico 
def get_type_icon_url_by_id(type_id):
    base_url = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/types/generation-iii/colosseum/'
    return f"{base_url}{type_id}.png"