from datetime import datetime
from subprocess import check_output, run

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
            wait_in_loop(started_at, wait_limit=300, err_message="Rancher boot up time limit exceeded.")
