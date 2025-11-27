from io import BytesIO
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    Класс для распознавания речи из аудио-байтов.
    Метод recognize() возвращает ТЕКСТ (str) или False.
    """

    # Инициализируешь клиента один раз (лучше вынести API_KEY в env)
    client = OpenAI(
        api_key="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",
    )

    MODEL_NAME = "whisper-1"

    @classmethod
    def recognize(cls, audio_bytes: bytes) -> str | bool:
        """
        :param audio_bytes: raw bytes, которые приходят с request.FILES['file'].read()
        :return: текст (str) или False
        """

        if not audio_bytes:
            return False

        try:
            file_obj = BytesIO(audio_bytes)
            file_obj.name = "audio.webm"  # имя нужно, чтобы API понимал формат

            transcription = cls.client.audio.transcriptions.create(
                model=cls.MODEL_NAME,
                file=file_obj,
                language="ru",
                response_format="text",
            )

            text = transcription.strip() if isinstance(transcription, str) else str(transcription).strip()

            if not text:
                return False

            return text

        except Exception as e:
            logger.exception("Ошибка при распознавании речи через Whisper: %s", e)
            return False
