#!/usr/bin/env python3
"""YouTube Video Transcriptor — downloads audio and transcribes with OpenAI Whisper."""

import sys
import re
import os
import glob
import tempfile

import yt_dlp
import whisper

DEFAULT_WHISPER_MODEL = "base"

WHISPER_MODELS = ("tiny", "base", "small", "medium", "large")


def extract_video_id(url: str) -> str:
    """Extract the YouTube video ID from multiple URL formats.

    Supported formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    """
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)",
        r"youtube\.com/shorts/([^&\n?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(
        f"No se pudo extraer el ID del video desde la URL: {url}\n"
        "Asegúrate de que el enlace sea válido (ej: https://www.youtube.com/watch?v=XXXX)."
    )


def download_audio(url: str, output_dir: str) -> str:
    """Download the best available audio from a YouTube URL into output_dir.

    Returns the path to the downloaded audio file.
    Raises RuntimeError if the download fails.
    """
    outtmpl = os.path.join(output_dir, "audio.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except yt_dlp.utils.DownloadError as exc:
        raise RuntimeError(f"No se pudo descargar el audio: {exc}") from exc

    # Locate the output file (extension may vary if ffmpeg is unavailable)
    matches = glob.glob(os.path.join(output_dir, "audio.*"))
    if not matches:
        raise RuntimeError(
            "yt-dlp no produjo ningún archivo de audio. "
            "Verifica que ffmpeg esté instalado y el video sea accesible."
        )
    return matches[0]


def transcribe_audio(
    audio_path: str,
    model_name: str = DEFAULT_WHISPER_MODEL,
    language: str | None = None,
) -> str:
    """Transcribe an audio file using OpenAI Whisper.

    Args:
        audio_path: Path to the audio file.
        model_name: Whisper model size (tiny, base, small, medium, large).
        language: Optional ISO-639-1 language code hint (e.g. 'es', 'en').
                  When None, Whisper auto-detects the language.

    Returns:
        The full transcript as a plain-text string.
    """
    model = whisper.load_model(model_name)
    kwargs = {}
    if language:
        kwargs["language"] = language
    result = model.transcribe(audio_path, **kwargs)
    return result["text"].strip()


def save_transcript(text: str, video_id: str, output_dir: str = ".") -> str:
    """Save transcript text to a .txt file and return the file path."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{video_id}_transcript.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(text)
    return filepath


def transcribe(
    url: str,
    model_name: str = DEFAULT_WHISPER_MODEL,
    language: str | None = None,
    output_dir: str = ".",
) -> str:
    """Download audio, transcribe with Whisper, and save the result.

    Returns the path of the saved transcript file.
    """
    video_id = extract_video_id(url)
    print(f"Video ID: {video_id}")

    with tempfile.TemporaryDirectory() as tmpdir:
        print("Descargando audio...")
        audio_path = download_audio(url, tmpdir)

        print(f"Transcribiendo con el modelo Whisper '{model_name}'...")
        text = transcribe_audio(audio_path, model_name=model_name, language=language)

    filepath = save_transcript(text, video_id, output_dir)
    print(f"Transcripción guardada en: {filepath}")
    return filepath


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str]):
    import argparse

    parser = argparse.ArgumentParser(
        prog="transcriptor",
        description="Transcribe videos de YouTube a partir de su URL usando OpenAI Whisper.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL del video de YouTube (ej: https://www.youtube.com/watch?v=XXXX)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_WHISPER_MODEL,
        choices=WHISPER_MODELS,
        help=(
            "Modelo de Whisper a utilizar. "
            "Modelos más grandes son más precisos pero más lentos. "
            f"Por defecto: {DEFAULT_WHISPER_MODEL}"
        ),
    )
    parser.add_argument(
        "--language",
        default=None,
        metavar="LANG",
        help=(
            "Código de idioma ISO-639-1 para guiar a Whisper (ej: es, en, pt). "
            "Si no se indica, Whisper detecta el idioma automáticamente."
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        metavar="DIR",
        help=(
            "Directorio donde se guardará el archivo de transcripción. "
            "Si no se indica, se abre una ventana para seleccionarlo manualmente."
        ),
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_transcript",
        help="Imprime la transcripción completa en la terminal además de guardarla.",
    )
    return parser.parse_args(argv)


def ask_output_dir() -> str:
    """Open a GUI folder-picker dialog and return the selected directory.

    Falls back to the current directory (".") if tkinter is not available
    (e.g. headless server, no display) or the user closes/cancels the dialog.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        return "."

    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        directory = filedialog.askdirectory(
            title="Selecciona el directorio donde guardar la transcripción"
        )
        root.destroy()
        return directory if directory else "."
    except tk.TclError:
        return "."


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    args = _parse_args(argv)

    # If no URL was passed as argument, ask interactively
    if not args.url:
        try:
            args.url = input("Ingresa la URL del video de YouTube: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelado.")
            return 1

    if not args.url:
        print("Error: no se proporcionó una URL.", file=sys.stderr)
        return 1

    # If no output directory was given, open a GUI folder-picker dialog
    if args.output_dir is None:
        args.output_dir = ask_output_dir()

    try:
        filepath = transcribe(
            args.url,
            model_name=args.model,
            language=args.language,
            output_dir=args.output_dir,
        )
    except (ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    if args.print_transcript:
        print("\n" + "=" * 60)
        with open(filepath, encoding="utf-8") as fh:
            print(fh.read())

    return 0


if __name__ == "__main__":
    sys.exit(main())
