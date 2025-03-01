from base64 import b64decode
from json import loads
from time import sleep, time
from typing import Literal
from subprocess import check_output, run

from .logger import console


class Kubernetes:
    """All kubenetes related methods."""
    
    @staticmethod
    def get_json(
        name: str,
        resource_type: Literal["configmap", "deployment", "pod", "secret", "service"],
    ) -> dict[str, str | int]:
        """Get data of given k8s resource in a python dictionary."""
        if Kubernetes.is_running():
            data: dict[str, str | int] = loads(
                check_output(
                    f'kubectl get {resource_type} {name} -o jsonpath="{{.data}}"'
                )
            )
            if resource_type == "secret":
                data = {
                    key: b64decode(str(value).encode()).decode()
                    for key, value in data.items()
                }
            return data
        return {}
    
    @staticmethod
    def is_running(timeout: int = 300) -> bool:
        """Check if k8s cluster is running.

        Args:
            timeout (int, optional): Timeout for checking in seconds. Defaults to 300.

        Returns:
            bool: Running or not.
        """

        def app_running() -> bool:
            """Helper function to check if Rancher Desktop.exe is running."""
            return (
                run('tasklist | findstr "Rancher Desktop.exe"', shell=True, capture_output=True).returncode
                == 0
            )

        def node_ready() -> bool:
            """Helper function to check if k8s node is Ready."""
            return (
                "Ready"
                in run("kubectl get node", text=True, capture_output=True).stdout
            )

        # actual checking
        if not app_running():
            raise Exception("Rancher desktop is not running.")
        if node_ready():
            return True
        started = time()
        with console.status("Rancher desktop is initializing..."):
            while not node_ready():
                sleep(5)
                if time() - started >= timeout:
                    raise TimeoutError("Rancher initialization timeout.")
        return True

    @staticmethod
    def pod_running(app: str) -> bool:
        """Check if given `app` pod is running or not."""
        if Kubernetes.is_running():
            return "Running" in check_output(f"kubectl get pod -l app={app}", text=True)
        return False
    