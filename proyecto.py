
class Mensaje:
    def __init__(self, remitente, destinatario, asunto, contenido):
        # Inicializamos los atributos privados del mensaje para encapsular los datos y evitar modificaciones directas.
        # Esto sigue principios de OOP: los datos se mantienen privados y se acceden a través de propiedades.
        self._remitente = remitente  # Email del remitente
        self._destinatario = destinatario  # Email del destinatario
        self._asunto = asunto  # Asunto del mensaje
        self._contenido = contenido  # Contenido del mensaje

    @property
    def remitente(self):
        # Propiedad para acceder al remitente de forma segura (solo lectura).
        # Usamos @property para seguir el patrón de acceso controlado, evitando que se modifique directamente.
        return self._remitente

    @property
    def destinatario(self):
        return self._destinatario  # Similar al remitente, acceso seguro.

    @property
    def asunto(self):
        return self._asunto  # Acceso seguro al asunto.

    @property
    def contenido(self):
        return self._contenido  # Acceso seguro al contenido.

    def __str__(self):
        # Método para representar el objeto como una cadena legible.
        return f"De: {self.remitente}, Para: {self.destinatario}, Asunto: {self.asunto}"

class Carpeta:
    def __init__(self, nombre):
        # Inicializamos la carpeta con un nombre y estructuras para mensajes y subcarpetas.
        # Usamos un diccionario para subcarpetas porque permite un acceso rápido por nombre de subcarpeta
        self._nombre = nombre  # Nombre de la carpeta actual
        self._mensajes = []  # Lista para almacenar los mensajes directamente en esta carpeta
        self._subcarpetas = {}  # Diccionario para subcarpetas

    @property
    def nombre(self):
        # Propiedad para acceder al nombre de la carpeta de forma segura.
        return self._nombre

    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje a la lista de mensajes de esta carpeta.
           Razón: Mantener los mensajes en una lista simple para operaciones rápidas como agregar o listar."""
        self._mensajes.append(mensaje)  # Agregamos el mensaje a la lista

    def agregar_subcarpeta(self, nombre_subcarpeta):
        """Agrega una nueva subcarpeta si no existe.
           Razón: Esto permite la estructura recursiva del árbol, donde cada carpeta puede tener hijos (subcarpetas).
           Usamos un diccionario para evitar duplicados y facilitar el acceso."""
        if nombre_subcarpeta not in self._subcarpetas:
            self._subcarpetas[nombre_subcarpeta] = Carpeta(nombre_subcarpeta)  # Creamos una nueva instancia de Carpeta
        return self._subcarpetas[nombre_subcarpeta]  # Devolvemos la subcarpeta para uso inmediato

    def listar_mensajes(self):
        """Devuelve la lista de mensajes en esta carpeta específica.
           Razón: Esta es una operación básica sin recursión, para listar solo el contenido directo."""
        return self._mensajes

    def mover_mensaje_a(self, mensaje, ruta_destino):
        """Mueve un mensaje de esta carpeta a otra especificada por ruta.
           Parámetros: mensaje (el objeto a mover), ruta_destino (cadena como 'subcarpeta1/subcarpeta2').
           Razón: Implementamos esto para cumplir con la consigna de mover mensajes, usando rutas para navegar el árbol.
           Eficiencia: Como se analizó, O(d + 1), donde d es la profundidad."""
        carpeta_destino = self.obtener_carpeta_por_ruta(ruta_destino)  # Obtenemos la carpeta destino
        if carpeta_destino:  # Verificamos si la ruta es válida
            if mensaje in self._mensajes:  # Aseguramos que el mensaje esté en esta carpeta
                self._mensajes.remove(mensaje)  # Removemos el mensaje de aquí
                carpeta_destino.agregar_mensaje(mensaje)  # Agregamos el mensaje al destino
                return True  # Operación exitosa
        return False  # Fallo en la operación

    def obtener_carpeta_por_ruta(self, ruta):
        """Obtiene una carpeta a partir de una ruta relativa a esta carpeta.
           Esto permite navegar el árbol de forma recursiva, esencial para la estructura de subcarpetas."""
        partes_ruta = ruta.split('/')  # Dividimos la ruta en partes
        carpeta_actual = self  # Comenzamos desde la carpeta actual
        for parte in partes_ruta:  # Iteramos por cada parte de la ruta
            if parte in carpeta_actual._subcarpetas:  # Si la subcarpeta existe
                carpeta_actual = carpeta_actual._subcarpetas[parte]  # Nos movemos a esa subcarpeta
            else:
                return None  # Ruta inválida, devolvemos None
        return carpeta_actual  # Devolvemos la carpeta final

    def buscar_mensajes_recursivo(self, criterio, valor):
        """Realiza una búsqueda recursiva en esta carpeta y todas sus subcarpetas.
           Parámetros: criterio ('asunto' o 'remitente'), valor (cadena a buscar).
           Usamos recursión para recorrer el árbol completo, ya que es una estructura jerárquica.
           Esto cumple con la consigna de búsquedas recursivas y es natural para un árbol."""
        resultados = []  # Lista para almacenar los resultados
        # Buscamos en los mensajes de esta carpeta
        for mensaje in self._mensajes:
            if criterio == 'asunto' and valor.lower() in mensaje.asunto.lower():  
                resultados.append(mensaje)
            elif criterio == 'remitente' and valor.lower() in mensaje.remitente.lower():
                resultados.append(mensaje)
        
        # Llamada recursiva a subcarpetas
        for subcarpeta in self._subcarpetas.values():  # Iteramos por cada subcarpeta
            resultados.extend(subcarpeta.buscar_mensajes_recursivo(criterio, valor))  # Agregamos resultados de la recursión
        return resultados  # Devolvemos todos los resultados encontrados

class Usuario:
    def __init__(self, nombre, email):
        # Inicializamos el usuario con una estructura de carpetas basada en un árbol.
        # Cambiamos a una carpeta raíz para soportar subcarpetas recursivas.
        self._nombre = nombre
        self._email = email
        self._carpetas = Carpeta("raiz")  # Carpeta raíz del árbol
        # Creamos las carpetas iniciales como subcarpetas de la raíz
        self._carpetas.agregar_subcarpeta("bandeja de entrada")
        self._carpetas.agregar_subcarpeta("enviados")

    @property
    def nombre(self):
        return self._nombre  # Acceso seguro al nombre del usuario

    @property
    def email(self):
        return self._email  # Acceso seguro al email

    def recibir_mensaje(self, mensaje):
        # Agregamos el mensaje a la carpeta de bandeja de entrada.
        # Usamos rutas para acceder, manteniendo la consistencia con el árbol.
        inbox = self._carpetas.obtener_carpeta_por_ruta("bandeja de entrada")
        if inbox:
            inbox.agregar_mensaje(mensaje)

    def enviar_mensaje(self, servidor, destinatario_email, asunto, contenido):
        mensaje = Mensaje(self.email, destinatario_email, asunto, contenido)
        servidor.enviar_mensaje(mensaje)  # Enviamos a través del servidor
        sent_folder = self._carpetas.obtener_carpeta_por_ruta("enviados")  # Obtenemos la carpeta de enviados
        if sent_folder:
            sent_folder.agregar_mensaje(mensaje)  # Agregamos a enviados

    def crear_subcarpeta(self, ruta_padre, nombre_nueva_subcarpeta):
        # Crea una subcarpeta en una ruta específica.
        # Permite la expansión del árbol de carpetas de forma dinámica.
        carpeta_padre = self._carpetas.obtener_carpeta_por_ruta(ruta_padre)
        if carpeta_padre:
            return carpeta_padre.agregar_subcarpeta(nombre_nueva_subcarpeta)
        return None

    def mover_mensaje(self, ruta_origen, ruta_destino, asunto_o_indice):
        # Mueve un mensaje usando rutas.
        # Esto integra la funcionalidad de movimiento con el árbol, usando el método de Carpeta.
        carpeta_origen = self._carpetas.obtener_carpeta_por_ruta(ruta_origen)
        if carpeta_origen:
            for mensaje in carpeta_origen.listar_mensajes():
                if asunto_o_indice == mensaje.asunto or asunto_o_indice == carpeta_origen.listar_mensajes().index(mensaje):
                    return carpeta_origen.mover_mensaje_a(mensaje, ruta_destino)
        return False

    def buscar_mensajes(self, criterio, valor):
        # Inicia la búsqueda recursiva desde la carpeta raíz.
        return self._carpetas.buscar_mensajes_recursivo(criterio, valor)

    def listar_mensajes(self, ruta_carpeta="raiz/bandeja de entrada"):
        carpeta = self._carpetas.obtener_carpeta_por_ruta(ruta_carpeta)
        if carpeta:
            return carpeta.listar_mensajes()
        return []

class ServidorCorreo:
    def __init__(self):
        self._usuarios = {}  # Diccionario para almacenar usuarios por email

    def agregar_usuario(self, usuario):
        self._usuarios[usuario.email] = usuario

    def enviar_mensaje(self, mensaje):
        destinatario = self._usuarios.get(mensaje.destinatario)
        if destinatario:
            destinatario.recibir_mensaje(mensaje)
        else:
            print(f"Error: Usuario destinatario {mensaje.destinatario} no encontrado.")


        
