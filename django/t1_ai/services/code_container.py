import docker
import tempfile
import os
from typing import Tuple


class DockerContainer:
    def __init__(self, code_path: str, timeout: int = 1, input_data: str | None = None):
        """
        :param code_path: ПОЛНЫЙ путь к .py файлу на хосте
        :param timeout: лимит времени на выполнение (в секундах)
        :param input_data: строка, которая пойдёт в input() внутри кода
        """
        self.client = docker.from_env()
        self.timeout = timeout
        self.code_path = code_path
        self.input_data = input_data

        self.base_settings = {
            "image": "python_runner",
            "command": "python /app/code.py",
            "network_disabled": True,
            "mem_limit": "100m",
            "cpu_period": 100000,
            "cpu_quota": 50000,
            "detach": True,
        }

        self._tmp_input_file: str | None = None

    def _build_settings(self) -> dict:
        """
        Собираем финальный dict настроек для контейнера,
        подставляя путь к файлу и, при необходимости, input.
        """
        settings = self.base_settings.copy()

        volumes = {
            self.code_path: {
                "bind": "/app/code.py",
                "mode": "ro",
            }
        }

        # Если есть входные данные — кладём их во временный файл и монтируем
        if self.input_data is not None:
            tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8")
            tmp.write(self.input_data)
            tmp.flush()
            tmp.close()
            self._tmp_input_file = tmp.name

            volumes[self._tmp_input_file] = {
                "bind": "/app/input.txt",
                "mode": "ro",
            }

            # python /app/code.py < /app/input.txt
            settings["command"] = "/bin/sh -c 'python /app/code.py < /app/input.txt'"

        settings["volumes"] = volumes
        return settings

    def run(self) -> Tuple[bool, int, str]:
        """
        Запускает контейнер.
        :return: (is_ok, status_code, logs)
        """
        try:
            settings = self._build_settings()

            container = self.client.containers.run(**settings)

            result = container.wait(timeout=self.timeout)
            status_code = result.get("StatusCode", 1)

            logs = container.logs(stdout=True, stderr=True).decode("utf-8", errors="ignore")

            container.remove()

            # чистим временный файл с input (если был)
            if self._tmp_input_file and os.path.exists(self._tmp_input_file):
                os.remove(self._tmp_input_file)

            is_ok = (status_code == 0)
            return is_ok, status_code, logs

        except Exception as e:
            if self._tmp_input_file and os.path.exists(self._tmp_input_file):
                os.remove(self._tmp_input_file)
            return False, -1, str(e)
