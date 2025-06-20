#---------------------------------------------------------------------------------------------------------------------------------------

"Este archivo es como una lista en donde Django ve funciones concretas que responden a cada acción del usuario en la aplicación"

# El usuario entra a taringa.net, y presiona el botón de la "Home" (/home):
                                                                           "La dirección será taringa.net/home"
# Django busca en urls.py que función en VIEWS responde a la url de /home:  
                                                                           "Por ejemplo home (request)"
# Ejecuta esa función, obteniendo datos
      
# Finalmente combina el template HTML y los datos (como imagenes, textos, redireccionando,etc); devolviendo una página web.

"Todas las views van a terminar respondiendo con una página web (HTML)."

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
    images = services.getAllImages()    ###: Cambiamos la lista vacía por una llamada a la función "getAllImages()"".
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

""" ###: Esta línea llama a la función getAllImages(), que está definida en el archivo services.py, que se encuentra dentro de la carpeta Layers. Lo que va a hacer es:
                    1) Busca a los pokémons en la API
                    2) Luego toma los datos de cada uno, los ordena y los pone dentro de tarjetas pokémon separadas
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