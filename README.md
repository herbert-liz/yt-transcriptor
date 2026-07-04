# yt-transcriptor

Herramienta de línea de comandos en Python que descarga y guarda la transcripción (subtítulos) de cualquier video de YouTube con solo proporcionarle el enlace.

---

## ✨ Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| **Un solo argumento** | Solo necesitas pasar la URL del video; el programa hace todo lo demás. |
| **Múltiples formatos de URL** | Soporta `youtube.com/watch?v=…`, `youtu.be/…`, `youtube.com/shorts/…` y `youtube.com/embed/…`. |
| **Selección de idioma** | Intenta obtener la transcripción en español, inglés y portugués (en ese orden). Se puede personalizar. |
| **Guardado automático** | Guarda la transcripción en un archivo `.txt` con el nombre `<video_id>_transcript.txt`. |
| **Salida configurable** | Permite elegir el directorio de destino con `--output-dir`. |
| **Impresión en terminal** | Opción `--print` para ver la transcripción directamente en la consola. |
| **Modo interactivo** | Si no se pasa la URL como argumento, el programa la solicita de forma interactiva. |

---

## 📋 Requisitos

- Python 3.10 o superior
- El video de YouTube debe tener subtítulos/captions disponibles (manuales o generados automáticamente).

---

## 🚀 Instalación

```bash
# 1. Clona el repositorio
git clone https://github.com/herbert-liz/yt-transcriptor.git
cd yt-transcriptor

# 2. (Opcional) Crea un entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

# 3. Instala las dependencias
pip install -r requirements.txt
```

---

## 🎬 Uso

### Forma básica — pasar la URL como argumento

```bash
python transcriptor.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Modo interactivo — el programa pide la URL

```bash
python transcriptor.py
# 🔗 Ingresa la URL del video de YouTube: https://youtu.be/dQw4w9WgXcQ
```

### Opciones disponibles

```
uso: transcriptor [-h] [--lang LANG [LANG ...]] [--output-dir DIR] [--print] [url]

argumentos posicionales:
  url                    URL del video de YouTube

opciones:
  -h, --help             muestra esta ayuda y sale
  --lang LANG [LANG …]   Idioma(s) preferidos (por defecto: es en pt)
  --output-dir DIR       Directorio de salida (por defecto: directorio actual)
  --print                Imprime la transcripción en la terminal
```

### Ejemplos adicionales

```bash
# Obtener transcripción en inglés primero, luego español
python transcriptor.py "https://www.youtube.com/watch?v=XXXX" --lang en es

# Guardar en una carpeta específica
python transcriptor.py "https://youtu.be/XXXX" --output-dir ./transcripciones

# Ver la transcripción en la terminal (el archivo también se guarda en disco)
python transcriptor.py "https://www.youtube.com/watch?v=XXXX" --print

# Combinación: guardar en carpeta e imprimir en terminal
python transcriptor.py "https://youtu.be/XXXX" --output-dir ./out --print
```

---

## 📂 Estructura del proyecto

```
yt-transcriptor/
├── transcriptor.py     # Script principal
├── requirements.txt    # Dependencias del proyecto
└── README.md           # Documentación
```

---

## ⚠️ Limitaciones

- Requiere que el video tenga subtítulos habilitados en YouTube (ya sean manuales o generados automáticamente).
- Videos con subtítulos completamente deshabilitados mostrarán un error descriptivo.
- El contenido de la transcripción depende de la calidad de los subtítulos disponibles en YouTube.

---

## 📄 Licencia

Este proyecto es de uso libre. Consulta el archivo `LICENSE` si existe, o contáctate con el autor para más información.
