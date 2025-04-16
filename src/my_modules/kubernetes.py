from base64 import b64decode
from datetime import datetime
from json import loads
from subprocess import check_output, run
from typing import Literal

from my_modules.logger import console
from my_modules.process import wait_in_loop


RANCHER = "Rancher Desktop.exe"


def rancher_running() -> bool:
    """Returns if rancher.exe is running."""
    return RANCHER in check_output("tasklist", shell=True, text=True)


def node_ready() -> bool:
    """Checks if node is ready in K8s."""
    if (
        status := run("kubectl get node", shell=True, text=True, capture_output=True)
    ).returncode == 0:
        return "Ready" in status.stdout
    return False


def rancher_wait() -> None:
    """Keeps the program busy till rancher boots up."""
    if node_ready():
        return
    with console.status("Rancher booting up..."):
        started_at = datetime.now()
        while not (rancher_running() and node_ready()):
            wait_in_loop(
                started_at,
                wait_limit=300,
                err_message="Rancher boot up time limit exceeded.",
            )


def get_json(
    name: str,
    resource: Literal["configmap", "deployment", "pod", "secret", "service"],
    base64decode: bool = False,
) -> dict[str, str]:
    """Get K8s resource data in json format.

    Args:
        name (str): resource name.
        resource (Literal[&quot;configmap&quot;, &quot;deployment&quot;, &quot;pod&quot;, &quot;secret&quot;, &quot;service&quot;]): resource type.
        base64decode (bool, optional): use with secrets. Defaults to False.

    Raises:
        Exception: if respurce not found.

    Returns:
        (dict[str, str]): resource data.
    """    
    rancher_wait()
    if (
        resp := run(
            f"kubectl get {resource} {name} -o jsonpath={{.data}}",
            text=True,
            capture_output=True,
        )
    ).returncode == 0:
        data: dict[str, str] = loads(resp.stdout)
        if base64decode:
            data = {
                key: b64decode(value.encode()).decode() for key, value in data.items()
            }
        return data
    else:
        raise Exception(resp.stderr)
