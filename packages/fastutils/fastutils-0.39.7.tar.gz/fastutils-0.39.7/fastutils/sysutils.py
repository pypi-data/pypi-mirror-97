import os
from sys import stdout
import uuid
import psutil
import socket
import subprocess
import threading

from . import fsutils
from . import strutils

def get_worker_id(prefix=None):
    """worker_id = prefix:hostname:process-id:thread-id
    """
    worker_inner_id = "{}:{}:{}".format(socket.gethostname(), os.getpid(), threading.get_ident())
    if prefix:
        return prefix + ":" + worker_inner_id
    else:
        return worker_inner_id


def get_daemon_application_pid(pidfile):
    """Get pid from pidfile if the daemon process is alive. If the daemon process is dead, it will alway returns 0.
    """
    if os.path.exists(pidfile) and os.path.isfile(pidfile):
        with open(pidfile, "r", encoding="utf-8") as fobj:
            pid = int(fobj.read().strip())
        try:
            p = psutil.Process(pid=pid)
            return pid
        except psutil.NoSuchProcess:
            return 0
    else:
        return 0


def get_random_script_name():
    name = str(uuid.uuid4())
    if os.name == "nt":
        name += ".bat"
    return name

def execute_script(script, workspace=None, script_name=None):
    workspace = workspace or fsutils.get_temp_workspace()
    if not os.path.exists(workspace):
        os.makedirs(workspace, exist_ok=True)
    
    script_name = script_name or get_random_script_name()
    script_path = os.path.join(workspace, script_name)
    fsutils.write(script_path, script)
    os.chmod(script_path, 0o755)

    p = subprocess.run(script_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=workspace, shell=True)
    code, stdout, stderr = p.returncode, p.stdout, p.stderr
    stdout = strutils.force_text(stdout)
    stderr = strutils.force_text(stderr)

    return code, stdout, stderr

