# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# Esta función arma el listado principal de Pokémon que se muestran en la galería del home y en el buscador.
def getAllImages():
    # 1. Llama a una función del archivo transport.py que se encarga de conectarse con la PokéAPI
    #    y devuelve una lista con los datos crudos de varios Pokémon.
    raw_data = transport.getAllImages() or []  # Agregamos "or []" para evitar errores si la API no responde. Ademas cambiamos el nombre de la funcion get_pokemon a getAllimages como figura en transport.py

    cards = []  # 2. Creamos un nuevo listado donde vamos a guardar cada Pokémon ya transformado en una "Card"

    # 3. Recorremos todos los Pokémon crudos(datos json sin convertir) que llegaron desde la API...
    for poke in raw_data:
        # 4. A cada uno lo transformamos en una "Card" usando el traductor definido en translator.py
        #    La función "to_card()" se encarga de tomar solo los campos que nos interesan (imagen, nombre, tipo, etc.)
        card = translator.fromRequestIntoCard(poke)

        # 5. Agregamos esa Card al listado final
        cards.append(card)

    # 6. Devolvemos el listado de Cards listo para ser usado en el home, el buscador y los filtros
    return cards

# función que filtra según el nombre del pokemon.
def filterByCharacter(name):
    filtered_cards = []

    for card in getAllImages():
        # debe verificar si el name está contenido en el nombre de la card, antes de agregarlo al listado de filtered_cards.
        filtered_cards.append(card)

    return filtered_cards

# función que filtra las cards según su tipo.
def filterByType(type_filter):
    filtered_cards = []

    for card in getAllImages():
        # Compara en minúsculas para evitar errores de mayúsculas
        if type_filter.lower() in [t.lower() for t in card.types]:
            filtered_cards.append(card)

    return filtered_cards

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    fav = '' # transformamos un request en una Card (ver translator.py)
    fav.user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.save_favourite(fav) # lo guardamos en la BD.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = [] # buscamos desde el repositories.py TODOS Los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = '' # convertimos cada favorito en una Card, y lo almacenamos en el listado de mapped_favourites que luego se retorna.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = request.POST.get('id')
    return repositories.delete_favourite(favId) # borramos un favorito por su ID

#obtenemos de TYPE_ID_MAP el id correspondiente a un tipo segun su nombre
def get_type_icon_url_by_name(type_name):
    type_id = config.TYPE_ID_MAP.get(type_name.lower())
    if not type_id:
        return None
    return transport.get_type_icon_url_by_id(type_id)