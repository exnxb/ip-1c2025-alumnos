#---------------------------------------------------------------------------------------------------------------------------------------

"Este archivo responde a las acciones del usuario en la aplicación."
# El usuario entra a la página y presiona en "Home":
"La dirección del path será: /home"
# Django busca en urls.py que función en VIEWS responde a /home:  
"En urls.py: path('home/', views.home, name='home'),"
# Ejecuta la función que corresponde (home(request)), para que realize el trabajo:
"En views.py: def home (request)"
# Combina el template HTML y los datos obtenidos (ya sean imagenes, textos, redireccionando, etc); devolviendo una página web.
"Una vez ejecutada la función home (request), devuelve una página web (HTML)."

#---------------------------------------------------------------------------------------------------------------------------------------

# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services     # Dentro del proyecto está la carpeta "layers", y allí hay un archivo llamado "services.py".Lo importo con el nombre "services"
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados: uno de las imágenes de la API (images) y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages()    ###: Cambiamos la lista vacía por una llamada a la función "getAllImages()", definida en services.py.
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

""" ###: Esta línea llama a la función getAllImages(), que está definida en el archivo services.py, que se encuentra dentro de la carpeta "layers". Lo que va a hacer es:
                    1) Busca a los pokémons en la API
                    2) Luego toma los datos, los ordena y los pone dentro de tarjetas
                    3) Guarda una a una cada tarjeta en una lista, y las muestra."""


# función utilizada en el buscador.
def search(request):
    name = request.POST.get('query', '')

    # si el usuario ingresó algo en el buscador, se deben filtrar las imágenes por dicho ingreso.
    if (name != ''):
        images = []
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    type = request.POST.get('type', '')

    if type != '':
        images = [] # debe traer un listado filtrado de imágenes, segun si es o contiene ese tipo.
        favourite_list = []

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        return redirect('home')

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    pass

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def exit(request):
    logout(request)
    return redirect('home')