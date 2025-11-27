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
        base_url="https://bothub.chat/api/v2/openai/v1",  # если юзаешь прокси/совместимый API
    )

    # Модель для транскрибации:
    # - классика: "whisper-1"
    # - новые: "gpt-4o-mini-transcribe" / "gpt-4o-transcribe" (если доступны на твоём endpoint)
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
            # Делаем из байтов file-like объект
            file_obj = BytesIO(audio_bytes)
            file_obj.name = "audio.webm"  # имя нужно, чтобы API понимал формат

            # Запрос к аудио-API OpenAI
            transcription = cls.client.audio.transcriptions.create(
                model=cls.MODEL_NAME,
                file=file_obj,
                language="ru",
                response_format="text",
            )

            # В новом клиенте transcription уже строка, но на всякий случай
            text = transcription.strip() if isinstance(transcription, str) else str(transcription).strip()

            if not text:
                return False

            return text

        except Exception as e:
            logger.exception("Ошибка при распознавании речи через Whisper: %s", e)
            return False
