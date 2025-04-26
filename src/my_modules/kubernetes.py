from base64 import b64decode
from datetime import datetime
from json import loads
from platform import node
from subprocess import check_output, run
from time import sleep
from typing import Literal

from my_modules.logger import console
from my_modules.misc import wait_in_loop

__all__ = ["Rancher", "pod_running", "get_json"]


class Rancher:
    """Rancher methods. !! Windows only."""

    exe: str = "Rancher Desktop.exe"

    @staticmethod
    def is_running() -> bool:
        """Wait synchronously until kubernetes services are up and running."""
        if Rancher._is_node_live():
            return True
        with console.status("Rancher desktop is booting up. Please wait!") as st:
            started_at = datetime.now()
            while not Rancher._is_app_running():
                wait_in_loop(
                    started_at,
                    wait=(1 * 60),
                    err_msg="Rancher application initialization failed.",
                )
            st.update("Rancher running. Starting node services...")
            while not Rancher._is_node_live():
                wait_in_loop(
                    started_at,
                    wait=(5 * 60),
                    err_msg="Kubernetes node failed to initialize.",
                )
            st.update(
                "Rancher boot up: [green]Complete[/]. Kubernetes services: [cyan]Live[/]."
            )
            sleep(1)
        return True

    @staticmethod
    def _is_node_live() -> bool:
        """Check if kubernetes node status is ready."""
        return (
            "Ready"
            in run(
                f"kubectl get node {node().lower()}", text=True, capture_output=True
            ).stdout
        )

    @staticmethod
    def _is_app_running() -> bool:
        """Check if rancher desktop is running as windows process."""
        return Rancher.exe in check_output("tasklist", text=True)


def pod_running(app: str) -> bool:
    """Check if a kubernetes pod is running with given `app` name."""
    if Rancher.is_running():
        return "Running" in check_output(f"kubectl get pod -l app={app}", text=True)
    return False


def get_json(
    name: str, resource: str | Literal["configmap", "secret"]
) -> dict[str, str]:
    """Get details of a given kubernetes resource in json format."""
    if Rancher.is_running():
        data: dict[str, str] = loads(
            check_output(
                f"kubectl get {resource} {name} -o jsonpath={{.data}}", text=True
            )
        )
        if resource == "secret":
            data = {
                key: b64decode(value.encode()).decode() for key, value in data.items()
            }
        return data
    raise Exception("Rancher desktop is not running.")
