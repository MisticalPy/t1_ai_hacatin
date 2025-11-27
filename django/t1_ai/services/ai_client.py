from openai import OpenAI, RateLimitError, APIError, BadRequestError


class AIClient:
    client = OpenAI(
        api_key="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",
    )

    MODEL_FOR_QUESTIONS = "gpt-4o-mini"

    @classmethod
    def generate_question(cls, messages) -> str:
        try:
            response = cls.client.chat.completions.create(
                model=cls.MODEL_FOR_QUESTIONS,
                messages=messages,

            )

            return response.choices[0].message.content

        except RateLimitError:
            return "Ошибка: превышен лимит. Пополни баланс API."

        except BadRequestError as e:
            return "Ошибка в запросе — проверь формат messages."

        except APIError as e:
            return "Сервер OpenAI не отвечает. Попробуй позже."

        except Exception as e:
            return f"Неизвестная ошибка: {e}"