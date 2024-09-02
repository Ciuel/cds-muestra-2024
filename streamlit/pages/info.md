# Información sobre la muestra de animales en peligro de extinción del proyecto de extención ciencia de datos

## Motivación
Esta muestra surge como resultado de la intención de explorar los mapas como medio para la visualización de datos y una mejor comprensión de los mismos.

## Los datos
Esta muestra contiene dos fuentes principales de datos:

- GBIF (GBIF.org (27 de agosto de 2024) Descarga de ocurrencias de GBIF (Enlace)[https://doi.org/10.15468/dl.nzngg6]):
GBIF es una base de datos que recopila información de especímenes de todo el mundo mediante la combinación de varios conjuntos de datos de investigadores. A través de este punto de acceso central, se pueden obtener datos de observaciones de animales en Argentina, con ciertas categorías de la Lista Roja de la UICN desde 1994 hasta 2024. Después de un procesamiento (descrito más adelante), se obtiene el conjunto de datos final utilizado en esta aplicación.

- IGN (Argenmap)[https://mapa.ign.gob.ar/] (Áreas Protegidas)[https://dnsg.ign.gob.ar/apps/api/v1/capas-sig/Geodesia+y+demarcaci%C3%B3n/L%C3%ADmites/area_protegida/json]:
El Instituto Geográfico Nacional pone a disposición un archivo GeoJson (un tipo especial de Json que permite describir áreas geográficas) con todas las áreas protegidas del país (parques nacionales, reservas, etc.) y también un mapa completo de la República Argentina con accidentes geográficos y áreas pobladas marcadas. Este mapa se utilizó como base para el mapa que se muestra en esta aplicación, y el GeoJson de las áreas protegidas se utilizó para determinar qué animales se encuentran dentro de estas áreas.

## El procesamiento
Cada año, miles de observaciones de animales se cargan en la base de datos de GBIF solo en Argentina, y cada observación puede tener más de 100 datos. Esto hace que sea imposible cargar o procesar la información de manera comprensible en un mapa en un tiempo razonable, por lo que se requiere filtrar y procesar estos datos.

- El primer paso (y el más importante) fue filtrar en GBIF. Utilizando el mapa interactivo y la consulta que se muestra en el enlace, se filtraron todas las observaciones para incluir solo aquellas en el país, en los años 1994 a 2024, y lo más importante, aquellas que pertenecen a una de las cuatro categorías más riesgosas de la Lista Roja de la UICN (Peligro Crítico, En Peligro, Vulnerable, Casi Amenazado). Esto redujo el conjunto de datos inicial a solo 167,215 observaciones, lo cual es mucho más manejable para las herramientas utilizadas.

- El segundo paso es limpiar y preparar el conjunto de datos para generar el mapa. En este paso, se utilizó la biblioteca pandas para eliminar los datos irrelevantes, eliminar las observaciones con datos faltantes, eliminar las observaciones fuera de las áreas protegidas y agregar el nombre común, el enlace de Wikipedia y una imagen representativa de cada especie. Estos últimos tres pasos se lograron utilizando la API de iNaturalist, un proyecto donde los usuarios pueden cargar observaciones (que también forman parte de GBIF) y guardar información sobre las especies, incluidos los datos obtenidos. También se generó un conjunto de datos con todas las especies para las cuales hay observaciones, que se utiliza en el juego de la aplicación.

- El tercer paso es generar el mapa, o más precisamente, los mapas. Se generó un mapa para cada combinación de las cuatro categorías de la UICN mencionadas anteriormente. Esto se hizo utilizando la biblioteca de gráficos plotly, que permite generar un gráfico de cloropeto que incluye las áreas protegidas y un gráfico de puntos para las observaciones. Esto se hizo para acelerar la carga al seleccionar los mapas en la aplicación. Los mapas incluyen un control deslizante de plotly que controla la visibilidad de las observaciones, lo que permite mostrar solo las observaciones del año seleccionado.

## La Aplicación
- Una vez generados los mapas, se cargan en una aplicación creada con la biblioteca streamlit para mostrarlos. Esto se logra mediante casillas de verificación que seleccionan las categorías a mostrar y mediante un control deslizante de años que va desde 1994 hasta 2024. Al hacer clic en uno de los puntos que aparecen en el mapa, se muestra una imagen, el nombre y una página de referencia (principalmente de Wikipedia) con información sobre la especie. 
- La aplicación también cuenta con un juego de adivinanzas de especies en peligro, donde se muestran cuatro imágenes de especies, una de las cuales está en peligro crítico. El objetivo del juego es adivinar cuál es la especie en peligro crítico. Si el usuario adivina correctamente, se muestran cuatro imágenes más; de lo contrario, las mismas imágenes se mantienen hasta que se adivine correctamente.

