import docker
from typing import Tuple


class DockerContainer:
    def __init__(self, code_path: str, timeout: int = 1):
        """
        :param code_path: ПОЛНЫЙ путь к .py файлу на хосте (например: /home/user/project/media/code_submits/123.py)
        :param timeout: лимит времени на выполнение (в секундах)
        """
        self.client = docker.from_env()
        self.timeout = timeout
        self.code_path = code_path  # сюда передаём fs.path(...) из Django

        # базовые настройки контейнера
        self.base_settings = {
            "image": "python_runner",
            "command": "python /app/code.py",
            "network_disabled": True,
            "mem_limit": "100m",
            "cpu_period": 100000,
            "cpu_quota": 50000,
            "detach": True,
        }

    def _build_settings(self) -> dict:
        """
        Собираем финальный dict настроек для контейнера,
        подставляя путь к файлу в volumes.
        """
        settings = self.base_settings.copy()

        # volumes обязательно с АБСОЛЮТНЫМ путём
        settings["volumes"] = {
            self.code_path: {
                "bind": "/app/code.py",
                "mode": "ro",
            }
        }

        return settings

    def run(self) -> Tuple[bool, int, str]:
        """
        Запускает контейнер.
        :return: (is_ok, status_code, logs)
        """
        try:
            settings = self._build_settings()

            container = self.client.containers.run(**settings)

            # ждём завершения с таймаутом
            result = container.wait(timeout=self.timeout)
            status_code = result.get("StatusCode", 1)

            logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="ignore")
            print(logs)

            container.remove()

            is_ok = (status_code == 0)
            return is_ok, status_code, logs

        except Exception as e:
            # сюда можно ещё логирование прикрутить
            return False, -1, str(e)
