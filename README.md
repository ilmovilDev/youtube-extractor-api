# YouTube Content Extractor API

Esta aplicación Flask proporciona una API para extraer contenido de videos de YouTube, incluyendo la extracción de audio, transcripción de texto y generación de un resumen de los puntos principales. La aplicación utiliza la biblioteca `yt_dlp` para descargar audio y `langchain` para procesamiento de lenguaje natural.

## Tecnologías Utilizadas

- **Python 3.11**: Lenguaje de programación principal de la aplicación.
- **Flask**: Framework para desarrollar aplicaciones web y API.
- **yt_dlp**: Biblioteca para descargar videos y audio desde YouTube.
- **Langchain**: Framework para el procesamiento de lenguaje natural, utilizado para extraer y resumir texto.
- **Docker**: Para crear contenedores que facilitan la implementación y portabilidad de la aplicación.
- **FFmpeg**: Herramienta de procesamiento multimedia, usada para la manipulación de archivos de audio.

## Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/ilmovilDev/youtube-extractor-api.git
    ```

2. **Accede al directorio del proyecto:**
    ```bash
    cd youtube-extractor-api.git
    ```

## Ejecución con Docker

Para ejecutar la aplicación usando Docker, sigue los pasos:

1. **Construir la imagen Docker**:
    ```bash
    docker build -t youtube_content_extractor .
    ```

2. **Ejecutar el contenedor**:
    ```bash
    docker run -p 5000:5000 youtube_content_extractor
    ```

Una vez iniciado el contenedor, la API estará disponible en `http://localhost:5000`.

## Configuración

1. **Renombra el archivo `.env.example` a `.env` y configura las variables de entorno necesarias**:
    ```env
    GROQ_API_KEY=tu_api_key
    ```

## Endpoint
### Descargar Audio
- **URL**: `/download_audio`
- **Método**: `GET`
- **Descripción**: Extrae el audio de un video de YouTube y lo descarga en formato MP3.
- **Parámetros**: 
  - `video_url` (string, requerido): URL del video de YouTube.
- **Ejemplo de solicitud en Postman**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
- **Respuesta**
    - **Código 200**: Devuelve el archivo de audio descargado
    - **Código 400**: Error en la solicitud (e.g., URL no válida).

![Respuesta de Postman del Endpoint "/download_audio"](https://res.cloudinary.com/dihhlrchn/image/upload/v1731495489/Youtube%20app/knmbrlvuzsafsulktolo.png)


### Extraer Transcripción
- **URL**: `/extract_text`
- **Método**: `GET`
- **Descripción**: Extrae el texto del video en múltiples idiomas si están disponibles.
- **Parámetros**: 
  - `video_url` (string, requerido): URL del video de YouTube.
- **Ejemplo de solicitud en Postman**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
- **Respuesta**
    - **Código 200:** JSON con el título del video, el canal y la transcripción.
    - **Código 400:** Error en la solicitud (e.g., duración del video excede el límite).

![Respuesta de Postman del Endpoint "/extract_text"](https://res.cloudinary.com/dihhlrchn/image/upload/v1731495489/Youtube%20app/ozyx8lqgazjkq639x7lq.png)

### Generar Resumen
- **URL**: `/generate_summary`
- **Método**: `GET`
- **Descripción**: Genera un resumen del contenido del video basado en la transcripción extraída.
- **Parámetros**: 
  - `video_url` (string, requerido): URL del video de YouTube.
- **Ejemplo de solicitud en Postman**
```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```
- **Respuesta**
    - **Código 200:** JSON con el título del video, el canal y el resumen.
    - **Código 400:** Error en la solicitud (e.g., transcripción no disponible).

![Respuesta de Postman del Endpoint "/generate_summary"](https://res.cloudinary.com/dihhlrchn/image/upload/v1731495489/Youtube%20app/zt0ed1hvffeizwknd2u0.png)

## Datos del Autor

- **Nombre**: Luis Carrasco
- **GitHub**: [github.com/ilmovilDev](https://github.com/ilmovilDev)

## Licencia

Este proyecto está bajo la licencia MIT.
