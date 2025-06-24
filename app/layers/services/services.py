#---------------------------------------------------------------------------------------------------------------------------------------
"""
Este archivo recibe pedidos desde views.py (como por ejemplo buscar tal pokémon, filtrar por nombre, guardarlo, etc); se conecta con transport.py para solicitarle la información (en formato JSON), 
y luego organiza los datos obtenidos en tarjetas, para mostrar en la web.
"""""
#---------------------------------------------------------------------------------------------------------------------------------------


# capa de servicio/lógica de negocio

from ..transport import transport
from ...config import config
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

# Esta función arma el listado principal de Pokémon que se muestran en la galería del home y en el buscador.
def getAllImages():
    json_pokemons = transport.get_AllImages() or [] # 1) Llama a la  función "get_AllImages()", del archivo "transport.py", la cual se conecta con la API y devuelve el listado de imágenes crudas (JSON). Agregamos "or []" para evitar errores si la API no responde.
    lista_de_tarjetas = [] # lista vacía para ir guardando cada Pokémon ya transformado en una tarjeta ("Card")
    for dato in json_pokemons: # 2) Recorre cada objeto JSON (osea cada Pokémon en forma de información) de la lista que devuelve get_AllImages(), y los convierte uno a uno en una card.
        tarjeta = translator.fromRequestIntoCard(dato) #3) llama a la función fromRequestIntoCard(dato), definida en translator.py, y convierte el JSON actual (variable "dato") en una tarjeta
        lista_de_tarjetas.append(tarjeta) # 4) Añade la tarjeta al listado "lista_de_tarjetas"  
    return lista_de_tarjetas # 5) Por último, devuelve todas las tarjetas generadas.
    # Se borra el "pass", cuya función, al estar el código de la función ya completo, es innecesaria

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