# afinidata-content-manager
Content manager 
El content manager es el encargado de distribuir el contenido para el proyecto Afinidata. En él se encuentran dos aplicaciones especiales independientes funcionando, las cuales son: posts y messenger_users.

Los modelos en la aplicación ‘posts’ son:

Post: Modelo que guarda el contenido que se distribuirá al usuario a través del chatbot.

Interaction: Modelo que guarda distintas acciones que puede tener un usuario del chatbot asociadas o no a un post.

Feedback: Modelo que guarda las calificaciones que un usuario del chatbot le da a un bot.

Label: Modelo que guarda las distintas categorías que puede tener un post.

Question: Modelo que guarda las distintas preguntas que puede recibir un usuario del bot, asociadas a un post, a través de un servicio REST.

Response: Modelo que guarda las distintas respuestas que un usuario dio a determinada question.

Review: Modelo que guarda la revisión de un post, para su aprobación o denegación. 

UserReviewRole: Modelo que guarda el rol que cumple un usuario dentro de una review. (Autor o revisor).

Approbation: Modelo que guarda la aprobación de un post a través de un review, y el usuario que aprobó el post.

Rejection: Modelo que guarda la denegación de un post a través de un review, el usuario que denegó el post y un mensaje del porqué.

ReviewComment: Modelo que guarda comentarios hechos por un usuario sobre un review.

QuestionResponse: Modelo que guarda distintas respuestas con valor puntuado para una question.
Los modelos en la aplicación ‘messenger_users’ son:

User: Modelo que guarda los usuarios del bot en el canal (messenger)

UserData: Modelo que guarda los datos asociados a un usuario del bot en el canal.

Los modelos en la aplicación ‘posts’ que tienen referencia un usuario a través de una llave Foránea, hacen referencia a los usuarios nativos de django, y no a los usuarios del bot que se encuentran en la aplicación ‘messenger_users’.

Definición de Modelos:

Aplicación ‘posts’

Post:
name: Nombre del post. 
status: Puede ser: draft, review, rejected, need_changes, published. Donde “draft” representa que aún está en borrador, “review” que se encuentra en revisión, “rejected” que ha sido rechazado, “need_changes” que hay cambios por realizar y “published”, que representa que el servicio que distribuye los posts lo tomará en cuenta.
type: Puede ser: embeded, youtube. Donde embeded muestra en un iframe que ocupa toda la pantalla el contenido de un link, y youtube muestra un vídeo de youtube a través de su ID. (Próximo paso, un editor WYSIWYG y un type extra llamado “content”).
content: Dependiendo del type, debería ser un link en el type “embeded”, y el ID del vídeo de Youtube en el type “youtube”. (Próximo paso, contenido resultante del editor WYSIWYG en el type “content”).
content_activity: Contenido que es enviado al usuario del bot cuando este por problemas de conexión no puede ver el enlace o el vídeo del post. Se utiliza este signo “|” para delimitar el contenido de cada mensaje a través del chatbot.
user: Usuario creador del post.
min_range: El servicio que devuelve actividades se basa en un value para devolver un post dentro del rango, si value es mayor a este atributo el post es candidato para ser enviado.
max_range: El servicio que devuelve actividades se basa en un value para devolver un post dentro del rango, si value es menor a este atributo el post es candidato para ser enviado.
preview: El servicio que devuelve actividades, devuelve un pequeño resumen de qué trata esta actividad para llamar la atención del usuario, es este atributo.
new (Por eliminar): Delimitaba en cierta fecha si el servicio debía de tomar en cuenta el post para enviarse a usuarios.
thumbnail: El servicio que devuelve actividades, devuelve una imagen relacionada a la actividad. La url de la imagen debe guardarse en este atributo.
area_id (Para uso próximo): En idea, guarda el id del área al que pertenecen (Áreas basadas en el proyecto Core (cognitivo, motor, emocional)). Para que el servicio basado en el área solicitada devuelva únicamente posts de esa área. Por defecto se están solicitando a través del chatbot únicamente posts con área 1, mismo valor que se está guardando automáticamente en el modelo.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

Interaction:
post: Post asociado a la interacción. (Puede ser nulo, acciones como “iniciar sesión” no van asociadas a ningún post. Acciones como calificar si).
user_id: ID del usuario del bot asociado a la interaction.
username: Username del usuario del bot asociado a la interaction (Redundancia que se utiliza para ciertos reportes).
channel_id: channel id del usuario del bot.
bot_id: Bot al cual está conectado el usuario.
type: String que guarda el tipo de interaction que ejecutó el usuario, estas pueden ser de cualquier tipo. De uso cotidiano en la plataforma en ciertas cosas se encuentran ‘session’ y ‘opened’, su uso puede ser muy variado.
value: Valor de tipo Entero que puede almacenarse en las interacciones. (Formato de Entero posiblemente temporal, guardado así por alguna necesidad, por revisar)
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

Feedback:
post: Post que recibe la calificación del usuario.
user_id: ID del usuario del bot asociado a la interaction.
username: Username del usuario del bot asociado a la interaction (Redundancia que se utiliza para ciertos reportes).
channel_id: channel id del usuario del bot.
bot_id: Bot al cual está conectado el usuario.
Value: Valor de tipo entero que el usuario del bot le dio al post.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

Label:
name: Nombre de la categoría
posts: Referencia de muchos a muchos con el modelo Posts.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).
Question:
name: Texto de pregunta que le llega al usuario (si se solicita a través de un servicio).
Post: Referencia al post que pertenece esa pregunta.
Replies (Por eliminar): Casilla de texto que guardaba las posibles respuestas a una pregunta. 
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

Response:
question: Referencia a la question respondida.
user_id: ID del usuario del bot que respondió a la pregunta.
username: Username del usuario del bot que respondió la pregunta.
response: Respuesta del usuario a la pregunta.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

Review:
post: Post por revisar
status: Estado del review. Puede ser: pending, completed.
comment: Casilla que permite que el creador del post deje un comentario para el revisor sobre su post.
users: Usuarios vinculados a esta Revisión. (Author y Revisor) a través del modelo UserReviewRole.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

UserReviewRole:
review: Referencia al review.
user: Usuario vinculado al review.
role: Rol que cumple el usuario respecto al review. Puede tener valor: author, reviser. (Solo el usuario con el rol “reviser” o un superusuario puede completar el review).

Approbation: 
user: Usuario que aprobó el review (Y el post), puede ser únicamente el usuario con rol de “reviser” para esa review, o cualquier superusuario.
review: Review aprobada.




Rejection: 
user: Usuario que rechazó el review (Y el post), puede ser únicamente el usuario con rol de “reviser” para esa review, o cualquier superusuario.
review: Review rechazada.
comment: Casilla para que el usuario explique porqué rechazó el post.

ReviewComment:
user: Usuario asignado al review (O superusuario), creador del comentario en el review.
review: Enlace al modelo Review
comment: Comentario del usuario para la review.

QuestionResponse:
question: question asociada al tipo de respuesta
response: posible respuesta del usuario para la pregunta.
value: valor numérico de la QuestionResponse.

Aplicación ‘messenger_users’

User:
last_channel_id (por eliminar): ID propio de los canales (redes sociales, etc) propio de cada usuario.
channel_id: ID propio de los canales (redes sociales, etc) propio de cada usuario.
backup_key (por eliminar): Llave propia de cada usuario para ser identificado.
bot_id: Bot al que pertenece el usuario. (distinto bot puede representar para el mismo usuario un distinto channel_id)
username: Llave única por usuario.
created_at, updated_at: (Uso general, fecha de creación, fecha de última actualización).

UserData:
user: Usuario vinculado a la data.
data_key: atributo vinculado al usuario.
data_value: valor asignado al atributo y usuario.








MÉTODOS:

Aplicación posts

(ClassBasedView) HomeView: Muestra el listado de posts basado en los parámetros del formulario, de no existir muestra el listado de todos los posts agregados.

En el método get_context_data toma data del modelo interaction, y la compara para mostrar totales sobre esas interactions.

(Function) Post: Muestra el contenido del post individualmente. Si la url en sus parámetros GET trae el parámetro username o channel_id, buscará entre los usuarios del bot a este y creará dos interactions, una de tipo session y una de tipo opened.

Session se irá modificando con la cantidad de minutos que el usuario permanezca dentro del post.

(ClassBasedView) StatisticsView: Muestra los mismos datos para cada post individual en el HomeView. (Posiblemente por remover)

(ClassBasedView) NewPostView: Usa el parámetro LoginRequiredMixin (mismo uso en las demás vistas) para obligar al usuario a iniciar sesión para crear un post. Se sobreescribe la función form_valid para hacer una redirección a la vista posts.

(ClassBasedView) EditPostView: Usa el parámetro LoginRequiredMixin (mismo uso en las demás vistas) para obligar al usuario a iniciar sesión para crear un post. 

Se sobreescribe la función form_valid para hacer una redirección a la vista posts.

Se sobreescribe la función get_context_data para validar que al editar, solo pueda hacerlo el usuario creador del post, un superusuario o algún revisor asignado a través de un review.

(Function) edit_interaction: Servicio hecho para modificar los minutos que transcurren cuando un usuario del bot está viendo un post. (revisar script en posts/statics/js/post.js

(Function) set_user_send (Por eliminar): Crea una interacción de tipo “sended” (por modificar) basándose en el username o channel_id de un usuario del bot. 
*Se creó una función para crear cualquier tipo de interaction, por lo cual esta función es innecesaria.

(Function) Feedback: Crea o modifica la calificación de un usuario del bot a un post, basándose en su username, channel_id y el id del post, al igual que el atributo value y el atributo bot_id. (Genéricamente se está utilizando el 1)

No permite como valor de value un valor mayor a 5 ni menor a 1.

(ClassBasedView) DeletePostView: Vista para eliminar un post.
(Por cambiar) Enlace de redirección
(Por cambiar) en el método get_object, revisar que solo pueda eliminarse por el usuario creador o un superusuario.

(Function) create_tag: Servicio que crea un objeto del modelo Label de no existir, retorna un error si el label existe. Se utiliza en la vista de edición de post. (posts/static/js/edit-post.js)

(Function) tags: Servicio que devuelve todas las tags existentes. (Necesario en la vista de edición de post. (posts/static/js/edit-post.js)

(Function) set_tag_to_post (param: id, GET: name): Servicio que agrega un label a un post. (Relación muchos a muchos), basándose en el nombre de este label y como parámetro el id del post.

(Function) get_tag_to_post (param: id): Servicio que devuelve los label de un post. (Relación muchos a muchos)

(Function) remove_tag_to_post (param: id, GET: name): Servicio que elimina un label a un post. (Relación muchos a muchos), basándose en el nombre de este label y como parámetro el id del post.

(ClassBasedView) PostsListView (Por eliminar): Devuelve el listado de todos los posts con cálculos sobre su uso basado en instancias del modelo interaction. El uso del homeView para eso dejó esta función obsoleta.

(Function) post_by_limits(GET: value, area_id = default 1, username): Devuelve, basándose si el usuario del bot pertenece a un grupo un post.
El id de estos posts puede venir de un servicio externo (Grupo A, B) o generarse en modo aleatorio. (Grupo C).

Tomando las interacciones del usuario se descartan aquellos con interacciones existentes.

(Function) post_activity(param: id, GET: post_count): Devuelve el contenido de la actividad, dividido en partes con el signo “|” basándose en post_count para saber cual es el siguiente párrafo a devolver.
A su vez aumenta el valor de la variable post_count para su siguiente uso.

(ClassBasedView) QuestionsView: Listado de instancias del modelo question.
(por agregar) paginación
(por agregar) usar ListView

(ClassBasedView) CreateQuestionView: Vista genérica para la creación de una question vinculada a un post.
(por agregar) usar la url para tomar el id del post.
(por agregar) permitir crear preguntas vinculadas a un post únicamente por superusuario, dueño del post o revisor.

(ClassBasedView) EditQuestionView: Vista genérica para la edición de una question vinculada a un post.
En el método get_context_data se agrega un formulario para crear question_response.

(por agregar) usar la url para tomar el id del post.
(por agregar) permitir crear preguntas vinculadas a un post únicamente por superusuario, dueño del post o revisor.

(ClassBasedView) QuestionView: Vista genérica de una question vinculada a un post.

(ClassBasedView) DeleteQuestionView: Vista genérica para la eliminación de una question vinculada a un post.

(Function) question_by_post(params: id): Devuelve al hacer una instancia del modelo question asociada por el id de un post.
(por arreglar) Crear un método general y uno para chatfuel.

(Function) set_interaction_to_post(GET: interaction_type, username, post_id):
Crea una instancia del modelo de tipo interaction, para el usuario definido con el username y de tipo interaction_type.

(Function) get_thumbnail_to_post(param: id): Devuelve el contenido de la propiedad thumbnail del objeto post con el id del parámetro, método específico para chatfuel que despliega automáticamente una imagen.

(Function) create_response_for_question (param: id, GET: username, response): Crea un objeto del modelo Response, para el usuario con el username y su respuesta con el parámetro response para el objeto del modelo question con el id en las url params.

(Function) get_replies_to_question (param: id): Método específico para chatfuel que devuelve distintas quick replies con las posibles respuestas para el objeto del modelo question con el id en param.

Estas respuestas pueden basarse en una propiedad del objeto question llamada replies, o de instancias del modelo QuestionResponse.

(ClassBasedView) ReviewPostView: Vista general de un review.

(ClassBasedView) ChangePostStatusToReviewView: Vista con formulario para solicitar la revisión de un post.

se modifica get_context_data, para obtener el post del posible nuevo review.
se modifica form_valid para verificar que no hayan revisiones pendientes ya.

(ClassBasedView) Reviews: Listado de reviews. (Para author y revisor, únicamente las de los posts creados o por revisar, para superusuario, todas).

(ClassBasedView) ReviewView: Vista general de un review. Si el usuario es de tipo revisor y está asignado a ese review, al igual que cualquier superusuario, puede aprobarla o denegarla desde esta vista.

(ClassBasedView) AcceptReviewView: Vista que aprobará un post, y finalizará un review.
Verifica que ha sido utilizada por un superusuario o revisor asignado a esa review.

(ClassBasedView) Rejectioniew: Vista que denegará un post, y finalizará un review.
Verifica que ha sido utilizada por un superusuario o revisor asignado a esa review.

(ClassBasedView) ChangePostToNeedChangesView: Vista que cambiará el status de un post a ‘need_changes’.
Verifica que ha sido utilizada por un superusuario o revisor asignado a esa review.
(ClassBasedView) AddReviewCommentView: Añade un comentario asociado a un review.

(ClassBasedView) CreateQuestionResponseView: Crea un objeto del modelo QuestionResponse a través de un formulario. 

(ClassBasedView) EditQuestionResponseView: Vista de edición de un objeto del modelo QuestionResponse a través de un formulario. 

Aplicación messenger_users:

(Function) new_user: Crea una instancia del modelo User, verificando antes que este no exista a través del last_channel_id.

(Function) add_attribute (Por eliminar): Servicio específico para chatfuel, crea una instancia del modelo UserData, asociado a un usuario a través del channel_id. En el proyecto core este servicio es más eficiente.

(Function) by_userame: Servicio específico para chatfuel que devuelve el ID de un usuario basado en el username.

Aplicación Upload:

(ClassBasedView) UploadView: En esta vista en el protocolo get se muestra el formulario para añadir un archivo CSV. El único rol permitido es el de superusuario o de author.

En el protocolo post, basado en el archivo cargado, despliega los artículos por subir con la data en estos, basado en el CSV subido a través del método get. 

(ClassBasedView) UploadPostsView: A través de los kwargs obtiene el nombre del archivo, el cual se encarga de leer, cargar los posts dentro de él y eliminarlos.

TODO:

Convertir todas las funciones (Excepto las de tipo post) en ClassView.
Crear métodos en los modelos para únicamente ejecutarlos en los métodos dentro de views y no repetir código o hacer compleja la operación en el método.
Definir un esquema único para los templates, donde todos se encuentren en la misma carpeta base y hagan referencia a ella.
Eliminar la aplicación Dash
Revisar los métodos en uso dentro de chatfuel para eliminar los que ya no son necesarios sin encontrar problemas en el flujo.
Convertir last_channel_id en channel_id, eliminar el duplicado. 
Definir la aplicación “api”, y dentro de ella el manejo de versiones de la api.

Reglas de código:

Utilizar únicamente la función request en necesidades de tipo post. Por lo demás utilizar ClassBasedViews.
Implementar lo máximo posible métodos en el modelo y no en las vistas.
Archivos de js con sintaxis ES6. 
De preferencia en archivos js, funciones asíncronas y lenguaje puro. (No jQuery)
