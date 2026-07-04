#!/usr/bin/env python3
"""YouTube Video Transcriptor — fetches captions/subtitles from a YouTube video URL."""

import sys
import re
import os

from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.formatters import TextFormatter


# Preferred language order for transcript lookup
DEFAULT_LANGUAGES = ["es", "en", "pt"]


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


def fetch_transcript(video_id: str, languages: list | None = None) -> tuple[str, str]:
    """Fetch and format the transcript for a YouTube video.

    Returns a tuple of (formatted_text, language_code).
    Tries each language in *languages* before falling back to any available transcript.
    """
    if languages is None:
        languages = DEFAULT_LANGUAGES

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Try requested languages first (manual then auto-generated)
        try:
            transcript = transcript_list.find_transcript(languages)
        except NoTranscriptFound:
            # Fall back to the first available transcript (any language)
            transcript = next(iter(transcript_list))

        raw = transcript.fetch()
        formatter = TextFormatter()
        text = formatter.format_transcript(raw)
        return text, transcript.language_code

    except TranscriptsDisabled:
        raise RuntimeError(
            "Los subtítulos están deshabilitados para este video. "
            "No es posible obtener la transcripción."
        )
    except NoTranscriptFound:
        raise RuntimeError(
            f"No se encontró una transcripción en los idiomas: {languages}. "
            "Prueba con otro video o especifica un idioma diferente con --lang."
        )


def save_transcript(text: str, video_id: str, output_dir: str = ".") -> str:
    """Save transcript text to a .txt file and return the file path."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{video_id}_transcript.txt"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as fh:
        fh.write(text)
    return filepath


def transcribe(url: str, languages: list | None = None, output_dir: str = ".") -> str:
    """High-level helper: extract ID → fetch transcript → save to file.

    Returns the path of the saved transcript file.
    """
    video_id = extract_video_id(url)
    print(f"🎬 Video ID detectado: {video_id}")

    print("⏳ Obteniendo transcripción…")
    text, lang = fetch_transcript(video_id, languages)
    print(f"✅ Transcripción obtenida (idioma: {lang})")

    filepath = save_transcript(text, video_id, output_dir)
    print(f"💾 Transcripción guardada en: {filepath}")
    return filepath


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _parse_args(argv: list[str]):
    """Minimal argument parser (no external dependencies)."""
    import argparse

    parser = argparse.ArgumentParser(
        prog="transcriptor",
        description="Transcribe videos de YouTube a partir de su URL.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL del video de YouTube (ej: https://www.youtube.com/watch?v=XXXX)",
    )
    parser.add_argument(
        "--lang",
        nargs="+",
        default=DEFAULT_LANGUAGES,
        metavar="LANG",
        help=(
            "Idioma(s) preferidos para la transcripción, en orden de prioridad. "
            f"Por defecto: {DEFAULT_LANGUAGES}"
        ),
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        metavar="DIR",
        help="Directorio donde se guardará el archivo de transcripción. Por defecto: directorio actual.",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        dest="print_transcript",
        help="Imprime la transcripción completa en la terminal además de guardarla.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    args = _parse_args(argv)

    # If no URL was passed as argument, ask interactively
    if not args.url:
        try:
            args.url = input("🔗 Ingresa la URL del video de YouTube: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nCancelado.")
            return 1

    if not args.url:
        print("❌ No se proporcionó una URL.", file=sys.stderr)
        return 1

    try:
        filepath = transcribe(args.url, languages=args.lang, output_dir=args.output_dir)
    except (ValueError, RuntimeError) as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        return 1

    if args.print_transcript:
        print("\n" + "=" * 60)
        with open(filepath, encoding="utf-8") as fh:
            print(fh.read())

    return 0


if __name__ == "__main__":
    sys.exit(main())
