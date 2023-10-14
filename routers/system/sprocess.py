import os
import subprocess
from subprocess import PIPE, Popen
from typing import Literal

from dotenv import load_dotenv
from fastapi import APIRouter

from processes import Process, PopenStore, find_processes

load_dotenv()
DEBUG = os.getenv("DEBUG", False)

router = APIRouter(prefix="/system/subprocess", tags=["subprocess"])

Actions = Literal["run", "popen", "pclose"]


@router.get("/")
async def get_subprocesses():
    return [proc.cmd for proc in PopenStore.processes]


@router.post("/")
async def system_subprocess(action: str, cmd: str, cwd: str = "."):
    if action == "run":
        try:
            result = subprocess.run(cmd, cwd=cwd, stdout=PIPE, stderr=PIPE)
            stdout = result.stdout.decode("windows-1251")
            stderr = result.stderr.decode("windows-1251")
            return {"result": True, "stdout": stdout, "stderr": stderr}
        except Exception as e:
            return {"result": False, "msg": str(e)}
    elif action == "popen":
        try:
            with open(os.devnull, "w") as null:
                if DEBUG:
                    result = Popen(cmd, cwd=cwd)
                else:
                    result = Popen(cmd, cwd=cwd, stdout=null, stderr=null)
            process = Process(cmd, result)
            PopenStore.processes.append(process)
            return {"result": True}
        except Exception as e:
            return {"result": False, "msg": str(e)}
    elif action == "pclose":
        for process in find_processes(cmd):
            process.instance.terminate()
            process.instance.kill()
            PopenStore.processes.remove(process)
        return {"result": True}
