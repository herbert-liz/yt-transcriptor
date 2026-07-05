# yt-transcriptor

Herramienta de línea de comandos en Python que descarga el audio de cualquier video de YouTube y genera una transcripción usando OpenAI Whisper, sin depender de los subtítulos del video.

---

## Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| **Un solo argumento** | Solo necesitas pasar la URL del video; el programa descarga el audio y transcribe automáticamente. |
| **Sin dependencia de subtítulos** | Usa OpenAI Whisper para transcribir el audio directamente, por lo que funciona aunque el video no tenga subtítulos. |
| **Múltiples formatos de URL** | Soporta `youtube.com/watch?v=...`, `youtu.be/...`, `youtube.com/shorts/...` y `youtube.com/embed/...`. |
| **Selección de modelo** | Permite elegir el modelo de Whisper según la precisión y velocidad deseadas (tiny, base, small, medium, large). |
| **Detección automática de idioma** | Whisper detecta el idioma del audio automáticamente. Se puede indicar un idioma con `--language`. |
| **Guardado automático** | Guarda la transcripción en un archivo `.txt` con el nombre `<video_id>_transcript.txt`. |
| **Selector de carpeta (GUI)** | Si no se indica `--output-dir`, se abre automáticamente una ventana emergente para elegir dónde guardar el archivo. |
| **Salida configurable** | Permite elegir el directorio de destino con `--output-dir`. |
| **Impresión en terminal** | Opción `--print` para ver la transcripción directamente en la consola, además de guardarla. |
| **Modo interactivo** | Si no se pasa la URL como argumento, el programa la solicita de forma interactiva. |

---

## Requisitos

- Python 3.10 o superior
- [ffmpeg](https://ffmpeg.org/download.html) instalado y disponible en el PATH del sistema (requerido por Whisper y yt-dlp para la conversion de audio)

---

## Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/herbert-liz/yt-transcriptor.git
cd yt-transcriptor

# 2. (Opcional) Crea un entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

# 3. Instala las dependencias de Python
pip install -r requirements.txt
```

Instala ffmpeg si aun no lo tienes:

- **Ubuntu / Debian**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`
- **Windows**: descarga el instalador desde https://ffmpeg.org/download.html y agrega el binario al PATH.

---

## Uso

### Forma básica — pasar la URL como argumento

```bash
python transcriptor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Modo interactivo — el programa pide la URL

```bash
python transcriptor.py
# Ingresa la URL del video de YouTube: https://youtu.be/dQw4w9WgXcQ
```

### Opciones disponibles

```
uso: transcriptor [-h] [--model {tiny,base,small,medium,large}]
                  [--language LANG] [--output-dir DIR] [--print] [url]

argumentos posicionales:
  url                    URL del video de YouTube

opciones:
  -h, --help             muestra esta ayuda y sale
  --model MODEL          Modelo de Whisper a usar (por defecto: base)
  --language LANG       Código de idioma ISO-639-1 (ej: es, en, pt).
                         Si no se indica, Whisper lo detecta automáticamente.
  --output-dir DIR       Directorio de salida. Si se omite, se abre una ventana
                         emergente para seleccionarlo manualmente.
  --print                Imprime la transcripción en la terminal
```

### Ejemplos adicionales

```bash
# Usar el modelo large para mayor precisión
python transcriptor.py "https://www.youtube.com/watch?v=XXXX" --model large

# Indicar el idioma del video para mayor velocidad y precisión
python transcriptor.py "https://youtu.be/XXXX" --language es

# Guardar en una carpeta específica
python transcriptor.py "https://youtu.be/XXXX" --output-dir ./transcripciones

# Ver la transcripción en la terminal (el archivo también se guarda en disco)
python transcriptor.py "https://www.youtube.com/watch?v=XXXX" --print

# Combinación: modelo small, idioma inglés, guardar en carpeta e imprimir
python transcriptor.py "https://youtu.be/XXXX" --model small --language en --output-dir ./out --print
```

---

## Modelos de Whisper

| Modelo | Velocidad | Precisión | Memoria requerida |
|--------|-----------|-----------|-------------------|
| tiny   | Muy rápido | Básica    | ~1 GB              |
| base   | Rápido     | Buena     | ~1 GB              |
| small  | Moderado   | Muy buena | ~2 GB              |
| medium | Lento      | Alta      | ~5 GB              |
| large  | Muy lento  | Máxima    | ~10 GB             |

El modelo `base` es el valor por defecto y ofrece un buen equilibrio entre velocidad y precisión para la mayoría de los casos.

---

## Estructura del proyecto

```
yt-transcriptor/
├── transcriptor.py     # Script principal
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

---

## Limitaciones

- La primera ejecución descarga el modelo de Whisper seleccionado (puede tardar según el tamaño del modelo y la velocidad de conexión). Los modelos se almacenan en caché para usos posteriores.
- La calidad de la transcripción depende de la claridad del audio del video.
- Videos con restricciones geográficas o de edad pueden no ser descargables.

---

## Licencia

Este proyecto es de uso libre. Consulta el archivo `LICENSE` si existe, o contáctate con el autor para más información.
