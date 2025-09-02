import whisper
import requests
import tempfile
import os
from app.services.storage import storage_service


class TranscriptionService:
    """Audio transcription service using Whisper"""

    def __init__(self):
        self.model = whisper.load_model("base")

    def transcribe_from_url(self, audio_url: str) -> tuple[str, float]:
        """Download and transcribe audio from URL"""

        # Download audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            response = requests.get(audio_url)
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        try:
            # Transcribe using Whisper
            result = self.model.transcribe(temp_file_path)
            text = result["text"]

            # Calculate average confidence if available
            segments = result.get("segments", [])
            if segments:
                avg_confidence = sum(
                    seg.get("no_speech_prob", 0) for seg in segments
                ) / len(segments)
                confidence = (
                    1.0 - avg_confidence
                )  # Convert no_speech_prob to confidence
            else:
                confidence = 0.8  # Default confidence

            return text.strip(), min(confidence, 1.0)

        finally:
            # Clean up temp file
            os.unlink(temp_file_path)

    def transcribe_from_file(self, file_path: str) -> tuple[str, float]:
        """Transcribe audio from local file"""
        result = self.model.transcribe(file_path)
        text = result["text"]

        # Calculate confidence similar to URL method
        segments = result.get("segments", [])
        if segments:
            avg_confidence = sum(
                seg.get("no_speech_prob", 0) for seg in segments
            ) / len(segments)
            confidence = 1.0 - avg_confidence
        else:
            confidence = 0.8

        return text.strip(), min(confidence, 1.0)


transcription_service = TranscriptionService()
