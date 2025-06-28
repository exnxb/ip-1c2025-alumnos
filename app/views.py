#---------------------------------------------------------------------------------------------------------------------------------------

"Este archivo (las vistas) es el controlador. Con él, Django responde a las solicitudes del navegador del usuario en la aplicación. "
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
from .layers.services import services     # Es el módulo. Dentro del proyecto está la carpeta "layers", y allí hay un archivo llamado "services.py". Lo importo con el nombre "services"
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_page(request):
    return render(request, 'index.html')

# Esta función obtiene 2 listados: uno de las imágenes de la API (images) y otro de favoritos, ambos en formato Card, y los dibuja en el template 'home.html'.
def home(request):
    images = services.getAllImages() or []    ###: Cambiamos la lista vacía por una llamada a la función "getAllImages()"". Se agrega  "or []"" para que devuelva siempre un iterable, aunque esté vacío (osea evita un valor None o inválido).
    favourite_list = []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

""" ###: Esta línea llama a la función getAllImages(), que está definida en el archivo services.py, que se encuentra dentro de la carpeta "layers". Lo que va a hacer es:
                    1) Busca a los pokémons en la API
                    2) Luego toma los datos, los ordena y los pone dentro de tarjetas
                    3) Guarda una a una cada tarjeta en una lista, y las muestra."""


# Función que maneja las búsquedas por nombre de cada Pokémon. METODO POST (trabaja con los formularios enviados, no visibles en la url)
def search(request):
    # Guardo lo que escribió el usuario en el campo de búsqueda
    name = request.POST.get('query', '')  # Recibe y busca lo que el usuario escribió. Cuando Django recibe el formulario, lo recibe en forma de objeto. El objeto es el REQUEST; .POST es el "diccionario", y .get('query') es la clave en ese diccionario
    if name != '': # Si el usuario no escribió algo vacío entonces...
        images = services.filterByCharacter(name)  #  me trae la lista filtrada por nombre (reutiliza la función filterByCharacter(name) en services.py)
        favourite_list = []  #  Se mantiene la lista vacía para evitar errores con el template (home.html)
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })  #  Funcion render (parámetros), devuelve el template con las imágenes filtradas (construye la página con las imágenes filtradas)
    # request es el objeto, home.html la plantilla HTML, images contiene los Pokémon a mostrar, y favourite_list la lista vacía
    else: # Si no se escribió nada...
        return redirect('home')  # redirige a la galería completa


# función utilizada para filtrar por el tipo del Pokemon (desde los botones fuego - agua - planta). METODO GET METODO POST (trabaja con los valores enviados en la url)
def filter_by_type(request):
    # 1. El valor del tipo (siendo type la clave) está codificado dentro de cada botón; y cada valor está definido en home.html como un parámetro a tomar por la URL filter_by_type/?type= (water, fire, etc.), 
    type = request.GET.get('type', '') # Cambiamos el codigo, reemplazando POST por GET, ya que generalmente los botones usan método GET, no POST.
    if type != '': # Si el usuario no envia algo vacío entonces...
        images = services.filterByType(type) # 3. Llamamos a la función de servicios que devuelve solo los pokémon de ese tipo.
        favourite_list = [] # 4. (Temporal) Lista vacía de favoritos.
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list }) # 5. Renderizamos home.html, pero esta vez solo con los pokémon filtrados.
    else: # 6. Si no se especificó ningún tipo, simplemente redireccionamos al home sin filtrar.
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