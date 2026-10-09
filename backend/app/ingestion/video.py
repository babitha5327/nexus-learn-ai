from pathlib import Path
from app.ingestion.base import ParsedUnit


def parse_video(path: Path, model_size: str = "small", window_s: float = 30.0) -> list[ParsedUnit]:
    """Transcribe with faster-whisper and group segments into ~window_s timestamped units."""
    from faster_whisper import WhisperModel
    model = WhisperModel(model_size, compute_type="int8")
    segments, _ = model.transcribe(str(path), vad_filter=True)
    units: list[ParsedUnit] = []
    buf, start, end = [], None, 0.0
    for seg in segments:
        start = seg.start if start is None else start
        buf.append(seg.text.strip())
        end = seg.end
        if end - start >= window_s:
            units.append(ParsedUnit("transcript", " ".join(buf), t_start=start, t_end=end))
            buf, start = [], None
    if buf:
        units.append(ParsedUnit("transcript", " ".join(buf), t_start=start, t_end=end))
    return units
