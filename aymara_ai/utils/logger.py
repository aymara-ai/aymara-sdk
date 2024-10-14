import logging
import re
import time
from contextlib import contextmanager

from colorama import Fore, Style, init
from IPython import get_ipython
from IPython.display import HTML, display
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
        self.is_notebook = self._is_running_in_notebook()
        if not self.is_notebook:
            init(autoreset=True)  # Initialize colorama

    @staticmethod
    def _is_running_in_notebook():
        try:
            shell = get_ipython().__class__.__name__
            if shell == "ZMQInteractiveShell":
                return True  # Jupyter notebook or qtconsole
            elif shell == "TerminalInteractiveShell":
                return False  # Terminal running IPython
            else:
                return False  # Other type (?)
        except NameError:
            return False  # Probably standard Python interpreter

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
            colour="orange" if self.is_notebook else None,
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
        if self.is_notebook:
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
        status_str = task["status"]

        if not self.is_notebook:
            if task["status"] == Status.FAILED:
                status_str = f"{Fore.RED}{status_str}{Style.RESET_ALL}"
            elif task["status"] == Status.COMPLETED:
                status_str = f"{Fore.GREEN}{status_str}{Style.RESET_ALL}"
            else:
                status_str = f"{Fore.YELLOW}{status_str}{Style.RESET_ALL}"

        return (
            f"{task['test_name']} | "
            f"{task['uuid']} | "
            f"{elapsed_time}s | "
            f"{status_str}"
        )

    def warning(self, msg, *args, **kwargs):
        if self.is_notebook:
            # Detect and create links if in notebook
            link_pattern = r"(https?://\S+)"
            colored_msg = re.sub(
                link_pattern, r'<a href="\1" target="_blank">\1</a>', msg
            )
            colored_msg = f'<span style="color: orange;">{colored_msg}</span>'
            display(HTML(colored_msg))
        else:
            msg = f"{Fore.YELLOW}{msg}{Style.RESET_ALL}"
            super().warning(msg, *args, **kwargs)
