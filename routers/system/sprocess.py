import logging
import os
from subprocess import PIPE, Popen, run

from fastapi import APIRouter

from envs import DEBUG
from processes import PopenStore, Process, find_processes

router = APIRouter(prefix="/system/subprocess", tags=["subprocess"])


@router.get("/get-subprocesses/")
def system_get_subprocesses() -> list[str]:
    return [proc.cmd for proc in PopenStore.processes]


@router.get("/run/")
def system_subprocess_run(cmd: str, cwd: str = ".") -> dict:
    try:
        result = run(cmd, cwd=cwd, stdout=PIPE, stderr=PIPE, check=False)
        stdout = result.stdout.decode("windows-1251")
        stderr = result.stderr.decode("windows-1251")
        return {"result": True, "stdout": stdout, "stderr": stderr}
    except Exception as e:
        logging.exception(e)
        return {"result": False}


@router.get("/popen/")
def system_subprocess_popen(cmd: str, cwd: str = ".") -> dict:
    try:
        with open(os.devnull, "w", encoding="utf-8") as null:
            std = None if DEBUG else null
            result = Popen(cmd, cwd=cwd, stdout=std, stdin=std, stderr=std)
        process = Process(cmd, result)
        PopenStore.processes.append(process)
        return {"result": True}
    except Exception as e:
        logging.exception(e)
        return {"result": False}


@router.get("/pclose/")
def system_subprocess_pclose(cmd: str) -> dict:
    for process in find_processes(cmd):
        process.instance.terminate()
        process.instance.kill()
        PopenStore.processes.remove(process)
    return {"result": True}
