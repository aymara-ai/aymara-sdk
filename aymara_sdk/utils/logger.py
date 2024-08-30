import logging
import time
from contextlib import contextmanager

from tqdm.auto import tqdm

from ..types import Status


class SDKLogger(logging.Logger):
    def __init__(self, name="sdk", level=logging.DEBUG):
        super().__init__(name, level)

        # Set up logging
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.addHandler(handler)

        self.tasks = {}

    @contextmanager
    def progress_bar(self, test_name, uuid, status):
        self.tasks[uuid] = {
            "test_name": test_name,
            "uuid": uuid,
            "status": status,
            "start_time": time.time(),
        }
        desc = self._get_progress_description(uuid)
        with tqdm(
            total=None,
            desc=desc,
            unit="s",
            bar_format="{desc}",
            colour="orange",
        ) as pbar:
            pbar.update()
            self.tasks[uuid]["pbar"] = pbar
            try:
                yield pbar
            finally:
                del self.tasks[uuid]

    def update_progress_bar(self, uuid, status):
        task = self.tasks[uuid]
        task["status"] = status
        task["pbar"].set_description_str(self._get_progress_description(uuid))
        if status == Status.FAILED:
            task["pbar"].colour = "red"
        elif status == Status.COMPLETED:
            task["pbar"].colour = "green"
        else:
            task["pbar"].colour = "orange"
        task["pbar"].update()

    def _get_progress_description(
        self,
        uuid: str,
    ) -> str:
        task = self.tasks[uuid]
        elapsed_time = int(time.time() - task["start_time"])
        return (
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | "
            f"{task['test_name']} | "
            f"{task['uuid']} | "
            f"{elapsed_time}s | "
            f"{task['status']}"
        )
