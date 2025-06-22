#---------------------------------------------------------------------------------------------------------------------------------------

"Este archivo es como una lista en donde Django ve funciones concretas que responden a cada acción del usuario en la aplicación"

# El usuario entra a taringa.net, y presiona el botón de la "Home" (/home):
###### "La dirección será taringa.net/home"
# Django busca en urls.py que función en VIEWS responde a la url de /home:  
######"Por ejemplo home (request)"
# Ejecuta esa función, obteniendo datos
      
# Finalmente combina el template HTML y los datos (como imagenes, textos, redireccionando,etc); devolviendo una página web.

###"Todas las views van a terminar respondiendo con una página web (HTML)."

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
    images = services.getAllImages() or []    ###: Cambiamos la lista vacía por una llamada a la función "getAllImages()"". ##agregué or [] para que evitar que devuelva None
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

""" ###: Esta línea llama a la función getAllImages(), que está definida en el archivo services.py, que se encuentra dentro de la carpeta Layers. Lo que va a hacer es:
                    1) Busca a los pokémons en la API
                    2) Luego toma los datos de cada uno, los ordena y los pone dentro de tarjetas pokémon separadas
                    3) Guarda una a una cada tarjeta en una lista, y las muestra."""


# función utilizada en el buscador.
def search(request):
    # Guardo lo que escribió el usuario en el campo de búsqueda
    name = request.POST.get('query', '')  # Busca lo que el usuario escribió

    # Si se ingresó algo, realizamos la búsqueda
    if name != '':
        # Llamo a todos los Pokémon disponibles (sin filtrar)
        all_pokemons = services.getAllImages() or []  #  Me trae la lista completa desde la API ##hice lo mismo, agregué el or 

        # Lista donde guardaré solo los que coincidan con el nombre buscado
        images = []  #  Acá voy a guardar los que matchean

        # Me fijo uno por uno si el nombre de cada Pokémon incluye lo que el usuario escribió.
        for card in all_pokemons:
            if name.lower() in card.name.lower():  #  Comparación sin importar mayúsculas
                images.append(card)  #  Si coincide, lo agrego a la lista final

        # Lista de favoritos vacía por ahora
        favourite_list = []  #  Se mantiene para compatibilidad con el template

        # Devuelvo el template con las imágenes filtradas
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })  #  Muestra resultados

    # Si no se escribió nada, redirige a la galería completa
    return redirect('home')  #  Caso en que no se escribió nada

# función utilizada para filtrar por el tipo del Pokemon
def filter_by_type(request):
    # 1. Obtenemos el valor del tipo desde los parámetros de la URL (?type=agua, fuego, etc.).
    # Usamos GET porque generalmente los botones usan método GET, no POST.(Cambiamos el codigo que decia POST por GET)
    type = request.GET.get('type', '')

    # 2. Verificamos que se haya enviado algún tipo. Si no hay nada, redirigimos al home.
    if type != '':
        # 3. Llamamos a la función de servicios que devuelve solo los pokémon de ese tipo.
        images = services.filterByType(type)

        # 4. (Temporal) Lista vacía de favoritos.
        favourite_list = []

        # 5. Renderizamos el home, pero esta vez solo con los pokémon filtrados.
        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
    else:
        # 6. Si no se especificó ningún tipo, simplemente redireccionamos al home sin filtrar.
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