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